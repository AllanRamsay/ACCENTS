#!/usr/bin/python
from useful import *

def flac2wav(src, dest):
    makedirs(dest)
    for ifile in os.listdir(src):
        if ifile.endswith(".flac"):
            ofile = "%s.wav"%(ifile[:-5])
            ofile = os.path.join(dest, ofile)
            if not os.path.isfile(ofile): 
                execute("ffmpeg -i %s %s"%(os.path.join(src, ifile), ofile), printing=False, exceptions=".*")

if "flac2wav.py" in sys.argv[0]:
    try:
        flac2wav(getArg("src", sys.argv[1:], False), getArg("dest", sys.argv[1:], False))
    except:
        print "./flac2wav.py src=<SRC> dest=<DEST>"
                 
    
                          
