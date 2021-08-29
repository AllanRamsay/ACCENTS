from useful import *
import wave
import struct
from numpy.fft import rfft, irfft
try:
    import pylab
except:
    print "You won't be able to plot graphs, but the other stuff will work"
    import numpy as pylab
import math 

from play import play

"""
Represent the content of a .wav file as an object: the frames is a
string of 8-bit ASCII characters. That's horrible to work with, so we
convert it to an array of int-8s when we read it in, which we keep in
the signal, and then setframes will convert this array of ints back
into an ASCII string. You should do all your work on the signal, and
only convert it back to a string when you're about to save it (or play
it).
"""
class SOUND():

    def __init__(self, signal=None, name="sound", frames=None, params=None, start=None, end=None):
        if not signal is None:
            self.signal = signal
        self.name = name
        if not frames is None:
            self.frames = frames
        else:
            self.setframes(0, len(self.signal))
        if params is None:
            self.params = [1, 2, 44100, len(self.frames), 'NONE', 'not compressed']
        else:
            self.params = params
        if not start is None and not end is None:
            start = int(start*self.params[2])
            end = int(end*self.params[2])
            self.setframes(start, end)
            
    def __repr__(self):
        return "SOUND(%s, %s)"%(self.name, self.signal)

    def normalise(self, n=60, dtype="int8"):
        signal = pylab.array(self.signal)-(pylab.ones(len(self.signal))*min(self.signal))
        mx = max(signal)
        return pylab.array(map(lambda x: n*x/float(mx), signal), dtype=dtype)

    def setframes(self, start, end):
        self.frames = struct.pack("%sh"%(end-start), *(self.signal[start:end]))
        
    def save(self, wavfile="temp.wav", start=None, end=None):
        # self.params[3] = len(self.signal)/2
        w = wave.open(wavfile, "w")
        w.setparams(self.params)
        # w.setnchannels(1)
        if not self.frames:
            if start is None:
                start = 0
            if end is None:
                end = len(self.signal)
            self.setframes(start, min(end, len(self.signal)))
        w.writeframes(self.frames)
        w.close()

    def play(self):
        self.save("%s.wav"%(self.name))
        play("%s.wav"%(self.name))
        
    def plot(self, show=True, save=False, N=False):
        signal = self.normalise(n=255, dtype="float")
        if N:
            signal = signal[:N]
            print signal[:N]
        ymin, ymax = min(signal), max(signal)
        pylab.ylim(min(ymin-1, int(-0.1*ymin)), max(ymax+1, int(1.1*ymax)))
        pylab.plot(pylab.linspace(0, len(signal), len(signal)), signal)
        if save:
            pylab.savefig("%s.eps"%(self.name))
        if show:
            pylab.show()

def readsound(wavfile="sound1.wav", start=None, end=None):
    w = wave.open(wavfile, "r")
    params = list(w.getparams())
    f = w.readframes(w.getnframes())
    w.close()
    s = SOUND(pylab.array(struct.unpack('h'*(len(f)/2), f)), 
              frames=f, 
              name=wavfile,
              params=params,
              start=start,
              end=end)
    return s

"""
The signal best matches itself at 400 frames. A frame is 1/44100 seconds, so it matches itself at 400/44100 seconds = 0.009 seconds so pitch is 110Hz.
"""
def localmaximum(l):
    try:
        return max([(x, i) for i, x in enumerate(l[1:-1]) if x > 500 and i > 300 and l[i] < x and l[i+2] < x])
    except:
        return 0

def autocorr(signal):
    result = pylab.correlate(signal, signal, mode='full')
    return [x/1000000 for x in result[result.size/2:]]

def latexautocorr(l, out=sys.stdout):
    with safeout(out) as write:
        write(r"""
\begin{Verbatim}
""")
        for x in l:
            write("%4d"%(x))
        write("\n")
        for i in range(1, len(l)):
            k1 = ["    "]*i+l[:-i]
            for x in k1:
                try:
                    write("%4d"%(x))
                except:
                    write(x)
            write(r"""
\textcolor{lightgray}{""")
            for x, y in zip(l, k1):
                try:
                    write("%4d"%(abs(x-y)))
                except:
                    write("    ")
            write("}\n")
        write(r"""
\end{Verbatim}
""")

def localpitch(i, x):
    return localmaximum(autocorr(x[i:i+1000]))
    
def pitch(x):
    return [localpitch(i, x) for i in range(0, len(x)-1000, 100)]

"""
0.844014   180.680300
0.854014   181.916582
0.864014   180.753369
0.874014   193.796518
0.884014   202.034519
0.894014   201.161372
0.904014   191.750252

0.864127   162.798500
0.874127   172.712761
0.884127   177.480083
0.894127   182.036643
0.904127   180.446923
0.914127   172.204149
"""
def raisepitch(l0, r=10):
    return [x for i, x in enumerate(l0) if i%r > 0]

def lowerpitch(l0, r=10):
    l1 = []
    for i in range(len(l0)):
        l1.append(l0[i])
        if i%r == 0:
            l1.append((l0[i-1]+l0[i])/2)
    return l1

def stretch(l0, r=100, stretching=True):
    l0 = list(l0)
    l1 = []
    i = 0
    n = 0
    while i < len(l0):
        p = localpitch(i, l0)
        try:
            j = p[1]
        except:
            j = 10
        n += 1
        if stretching:
            l1 += l0[i:i+j]
            if n%r == 0:
                l1 += l0[i:i+j]
        else:
            if n%r > 0:
                l1 += l0[i:i+j]
        i += j
    return l1

def toPicture(fft, out=sys.stdout, maxheight=False):
    I = len(fft)
    J = len(fft[0])
    if maxheight == False:
        maxheight = J
    a = []
    best = 0
    for i in range(I):
        r = []
        for j in range(maxheight):
            try:
                p = fft[i][j]
                v = math.sqrt(p.real**2+p.imag**2)
                v = abs(p.real)
            except:
                v = 0
            if v > best:
                best = v
            r.append(v)
        a.append(r)
    for r in a:
        for j in range(len(r)):
            r[j] = 255-int(255*r[j]/best)
    a = pylab.array(a)
    pylab.imshow(a, "gray")
    pylab.show()

def showWav(wav):
    best = 0
    for x in wav:
        if x > best:
            best = x
    wav = [float(10*x)/float(best) for x in wav]
    pylab.plot(wav)
    pylab.show()

def plotpoints(points):
    img = pylab.zeros((512, 512, 1), pylab.uint8)
    for i in range(1, len(points)):
        p0 = int(points[i-1])+200
        p1 = int(points[i])+200
        cv2.line(img, (i-1, p0), (i, p1), 255,1)
    cv2.imshow('image', img)
    return img

                
