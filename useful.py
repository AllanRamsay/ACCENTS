import sys
import os
import codecs
import subprocess
import cPickle
import socket
import re
from timeit import timeit
import time
import random

host = socket.gethostname()

def usingMac():
    return sys.platform == "darwin"

from collections import namedtuple

try:
    from openpyxl import Workbook
    from openpyxl.styles import colors, Font, Color
except:
    pass

def toXLSX(lines, xlsxfile="test.xlsx"):
    wb = Workbook()
    ws = wb.active   
    colours = {"RED":colors.RED,
               "BLACK":colors.BLACK,
               "GREEN":"009900",
               "BLUE":colors.BLUE,
               "PURPLE":"bb00bb",
               }
    try:
        lines = lines.split("\n")
    except:
        pass
    for l in lines:
        try:
            l = l.split("\t")
        except:
            pass
        ws.append(l)
    for l1, l2 in zip(ws, lines):
        for c in l1:
            try:
                [value, colour] = c.value.split(":")
                c.font = Font(color=colours[colour])
                c.value = value
            except:
                pass
    wb.save(xlsxfile)

def csv2html(lines, out=sys.stdout):
    maxcols = max(len(line) for line in lines)+1
    with safeout(out) as write:
        write("""
<html>
<table style="width:7in">
""")
        for line in lines:
            write("<tr>")
            td = """<td colspan="%s">"""%(maxcols-len(line))
            for x in line:
                try:
                    [value, colour] = x.split("\t")
                    x = """<span style="color:%s">%s</span>"""%(colour, value)
                except:
                    pass
                write("%s %s</td>"%(td, x))
                td = "<td>"
            write("""
</tr>
""")
        write("""</table>
</html>
""")

class universal:

    def __init__(self):
        pass

    def __contains__(self, x):
        return True

class sink:

    def __init__(self):
        pass

    def write(self, x):
        pass

class safeout:

    def __init__(self, x, mode='w', encoding=False):

        if not x:
            self.writer = namedtuple("writer", "null")
            self.writer.write = x

            def exit(type, value, traceback):
                pass
            
        elif isstring(x):
            if encoding:
                self.writer = codecs.open(x, mode=mode, encoding=encoding)
            else:
                self.writer = open(x, mode=mode)

            def exit(type, value, traceback):
                self.writer.close()

        elif "function" in type(x):
            self.writer = namedtuple("writer", "write")
            self.writer.write = x

            def exit(type, value, traceback):
                pass

        else:
            self.writer = x

            def exit(type, value, traceback):
                pass
            
        self.__enter__ = (lambda: self.writer.write)
        self.__exit__ = exit

class stringwriter:

    def __init__(self):
        self.txt = ""
        
    def write(self, s):
        self.txt += "%s"%(s)
        
def write2file(s, f, encoding=False):
    with safeout(f, encoding=encoding) as out:
        out(s)

def writecsv(rows, out=sys.stdout):
    with safeout(out) as out:
        for r in rows:
            s = ""
            try:
                for x in r:
                    try:
                        s += "%s,"%(str(x).replace("\t", ":"))
                    except:
                        s += "%s,"%(x)
            except:
                s += "%s,"%(r)
            out(s[:-1]+"\n")

def readlines(top):
    if "\n" in top:
        for l in top.split("\n"):
            yield l
    else:
        if os.path.isdir(top):
            for f in os.listdir(top):
                for l in readlines(os.path.join(top, f)):
                    yield l
        else:
            for l in open(top):
                yield l

def solidify(generator, N=sys.maxint):
    solidified = []
    for x in generator:
        solidified.append(x)
        N -= 1
        if N == 0:
            break
    return solidified
            
def underline(string):
    return "%s\n%s"%(string, '*'*(len(string)))
            
def readcsv(ifile):
    SPLIT = re.compile(",|\t")
    return [SPLIT.split(x.strip()) for x in open(ifile)]

def replaceAll(s, r):
    if type(r) == "dict":
        for x in r:
            s = s.replace(x, r[x])
    else:
        for x in r:
            if isinstance(x, str) or isinstance(x, unicode):
                x = [x, ""]
            s = s.replace(x[0], x[1])
    return s

def runprocess(p, input=None, raiseException=False, printing=True):
    if isstring(p):
        p = p.split(" ")
    if printing:
        print "Running %s"%(p)
    x = subprocess.Popen(p, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE).communicate(input)
    if x[1] == '':
        return x[0]
    else:
        if raiseException:
            raise Exception(x[1])
        else:
            return x
        
def execute(command, d=".", args=False, printing=True, timing=False, exceptions=".*SICStus.*"):
    HOME = os.getcwd()

    def home():
        os.chdir(HOME)

    try:
        if isinstance(command, str):
            command = re.compile("\s+").sub(" ", command.strip()).split(' ')
        s = ''
        for x in command:
            s = s+"%s "%(x)
        os.chdir(d)
        if printing or timing:
            print """
Doing %s
in %s
"""%(s, os.getcwd())
        T0 = time.time()
        if args:
            p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            r = p.communicate(args)
        else:
            p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            r = p.communicate()
        if not r[1] == "":
            if exceptions and re.compile(exceptions, re.DOTALL).match(r[1]):
                print "WARNING: %s"%(r[1])
            else:
                home()
                raise Exception(r[1])
        home()
        if timing:
            print """%s took %.1f seconds"""%(s, time.time()-T0)
        return r
    except Exception as e:
        home()
        raise e

def makedirs(d, printing=True):
    try:
        os.makedirs(d)
    except:
        if printing:
            print "%s already exists"%(d)
         
def type(x):
    return x.__class__.__name__

def isstring(x):
    return type(x) == 'str'

def islist(x):
    return type(x) == 'list'

def istuple(x):
    return type(x) == 'tuple'

def istable(x):
    return x.__class__.__name__ == 'dict'

def printall(l):
    for x in l:
        print x

def printtable(l, format='%s %s'):
    for x in l:
        print format%(x, l[x])

def printsortedtable(l, format='%s %s'):
    for x in l:
        print format%(x, sortTable(l[x]))

def pretty(x, indent='', maxwidth=40):
    s = ''
    if type(x) == 'list' and not x == [] and len(str(x)+indent) > maxwidth:
        s += '['
        if len(x) > 0:
            indent1 = indent+' '
            indent2 = ''
            for y in x:
                s += '%s%s, \n'%(indent2, pretty(y, indent1, maxwidth))
                indent2 = indent1
        s = s[:-3] + ']'
    else:
        s = str(x)
    if indent == '':
        print s
    else:
        return s
    
def treepr(x, indent='', maxwidth=40):
    s = ''
    if type(x) == 'list' and not x == [] and len(str(x)+indent) > maxwidth:
        hd = str(x[0])
        s += '[%s, '%(hd)
        indent1 = indent+' '*(len(s))
        indent2 = ''
        for y in x[1:]:
                s += '%s%s, \n'%(indent2, treepr(y, indent1, maxwidth))
                indent2 = indent1
        s = s[:-3] + ']'
    else:
        s = str(x)
    if indent == '':
        print s
    else:
        return s
    
def sigfig(l, sf=2):
    try:
        return float(('%%.%sf'%(sf))%(l))
    except:
        if islist(l):
            return [sigfig(x, sf) for x in l]
        elif istuple(l):
            return tuple([sigfig(x, sf) for x in l])
        else:
            return l
        
def incTable(x, t, n=1):
    try:
        t[x] += n
    except KeyError:
        t[x] = n

def incTable2(x, y, t):
    if not x in t:
        t[x] = {}
    incTable(y, t[x])

def incTableN(x, t, n=1):
    k = x[0]
    if len(x) == 1:
        incTable(k, t, n)
    else:
        if not k in t:
            t[k] = {}
        incTableN(x[1:], t[k], n=n)

def extendTable(x, v, t):
    try:
        t[x].append(v)
    except KeyError:
        t[x] = [v]

def mergeTables(t1, t2):
    t = {}
    for k in t1:
        t[k] = t1[k]
    for k in t2:
        incTable(k, t, t2[k])
    return t

def sortTable(t, key=lambda i:i, rev=True):
    l = [(t[x], x) for x in t]
    l.sort(key=key)
    if rev:
        l.reverse()
    l = [(x[1], x[0]) for x in l]
    return l

def leaves(t):
    try:
        return sum(leaves(x) for x in t.values())
    except:
        return 1

def getBest(t):
    return sortTable(t)[0]

def getWorst(t):
    return sortTable(t)[-1]

def choosebest(table):
    n = -1
    best = None
    for x in table:
        j = table[x]
        if isinstance(j, int):
            if j > n:
                best = x
                n = j
            elif j == n:
                best = None
    return best

def normalise(d0):
    t = float(sum(d0.values()))
    for x in d0:
        d0[x] = d0[x]/t
    return d0

def normalised(x0):
    t = float(sum(x0.values()))
    return {k: x0[k]/t for k in x0}

def normalise2(d):
    for x in d:
        d[x] = normalise(d[x])

def normalised2(d):
    return {k: normalised(d[k]) for k in d}

def normaliseN(d):
    try:
        t = float(sum(d.values()))
        for x in d:
            d[x] = d[x]/t
    except:
        for x in d:
            normaliseN(d[x])

def memofn(x, f, d):
    if not x in d:
        d[x] = f(x)
    return d[x]

def makememofn(f):
    d = {}
    return lambda x: memofn(x, f, d)

def invertTable(d0):
    d1 = {}
    for k in d0:
        v = d0[k]
        if v in d1:
            raise Exception("Cannot create inverse table for %s because %v is already in the inverted table"%(d1, v))
        else:
            d1[v] = k
    return d1

def softmax(d):
    if d == {}:
        return d
    elif isinstance(d.values()[0], dict):
        return {x: softmax(d[x]) for x in d}
    else:
        t = sum(log(x+1) for x in d.values())
        return {k: log(d[k]+1)/t for k in d}

def openOut(out):
    if not out == sys.stdout:
        out = open(out, 'w')
    return out

def closeOut(out):
    if not out == sys.stdout:
        out.close()
        
def noCopies(l0):
    l1 = []
    for x in l0:
        if not x in l1:
            l1.append(x)
    return l1

def getArg(flag, args, default=False):
    for i, kv in enumerate(args):
        try:
            key, value = kv.split("=")
            if flag.lower().startswith(key.lower()):
                del args[i]
                return value
        except:
            pass
    if default is "None":
        raise Exception("You must specify a value for '%s'"%(flag))
    return default

def latexsafe(s):
    return replaceAll(s, [("$", r"\$"), ("{", r"\{"), ("}", r"\}"), ("%", r"\%"), ("&", r"\&")])

"""
Stuff for printing results out in a LaTeX-friendly way
"""
VERBATIM = r"""
\begin{Verbatim}[commandchars=\\\{\}]
%s
\end{Verbatim}
"""
  
def verbatim(s, latex=False, underline=False, silent=False):
    if silent:
        return "xx"
    if latex:
        return VERBATIM%(s)
    else:
        if underline:
            s = ('*'*(len(s)+2))+'\n*'+s+'*\n'+('*'*(len(s)+2))
        return s

def delete(x, l):
    return [y for y in l if not y == x]

def join(l, sep):
    return sep.join([str(x) for x in l])

def reverse(s0):
    s1 = ""
    for c in s0:
        s1 = c+s1
    return s1

def rotate(l):
    return l[1:]+l[:1]

def pstree(l, indent=' ', lsep=60, tsep=50, nsep=5):
    if indent==' ':
        params = "[levelsep=%spt, treesep=%spt, nodesep=%spt]"%(lsep, tsep, nsep)
    else:
        params = ""
    if type(l) == "str":
        return "\\pstree%s{\TR{%s}}{}"%(params, l)
    s = "\\pstree%s{\TR{%s}}{"%(params, l[0])
    nl = "\n%s"%(indent)
    for d in l[1:]:
        s += "%s%s"%(nl, pstree(d, lsep=lsep, tsep=tsep, nsep=nsep, indent=indent+' '))
    return s+"}"

def doc(s):
    return r"""
\documentclass[11pt]{article}
\usepackage{defns}
\usepackage{examples}
\usepackage{lscape}
\usepackage{pstricks, pst-node, pst-tree}
\begin{document}
%s
\end{document}
"""%(s)

def dump(x, f):
    f = open(f, 'w')
    cPickle.dump(x, f)
    f.close()

def load(f):
    return cPickle.load(open(f))

import json

def jdump(x, f):
    f = open(f, 'w')
    json.dump(x, f)
    f.close()
    
def jload(f):
    return json.load(open(f))

def average(l):
    return float(sum(l))/len(l)

from math import sqrt, log

def stats(l):
    m = average(l)
    s = sqrt(average([(x-m)**2 for x in l]))
    return m, s

def sendmail(recip, subject, content, actuallySend=False):
    args = """"From: Allan.Ramsay@manchester.ac.uk
Subject: %s
Bcc: Allan.Ramsay@manchester.ac.uk
Reply-to: Allan.Ramsay@manchester.ac.uk
"""%(subject)+content
    print recip, args
    if actuallySend:
        print execute(["sendmail", "-t", recip], args=args)

def ss(msg):
    print msg
    sys.stdin.readline()

def depth(tree):
    m = 0
    if type(tree) == "list":
        for x in tree[1:]:
            m = max(m, depth(x))
    return m+1

import datetime
def now():
    return datetime.datetime.now()

def timediff(t1, t0):
    return (t1-t0).total_seconds()

def timeSince(t):
    return timediff(now(), t)

def timeGoal(g, n=1):
    t0 = now()
    for i in range(n):
        g()
    e = timeSince(t0)
    return e, float(e)/n

def copytable(t0):
    t1 = {}
    for x in t0:
        t1[x] = t0[x]
    return t1

def runlatex(s, packages=[], outfile="temp.tex"):
    packages = "\n".join([r"""\usepackage{%s}"""%(p) for p in packages])
    src = r"""
\documentclass[12pt]{article}
\usepackage{pstricks, pst-node, pst-tree}
\usepackage{defns}
%s
\begin{document}
%s
\end{document}
"""%(packages, s)
    with safeout(outfile) as out:
        out(src)
    if isinstance(outfile, str):
        if outfile[-4:] == ".tex":
            outfile = outfile[:-4]
        print outfile
        latex = ("latex %s"%(outfile)).split(" ")
        print latex
        subprocess.Popen(latex).wait()
        dvipdf = ("dvipdf %s"%(outfile)).split(" ")
        print dvipdf
        subprocess.Popen(dvipdf).wait()
        print "done"
        
def checkArgs(t, args, default=False):
    for a in args:
        try:
            k, v = a.split("=")
            if t.startswith(k):
                return v
        except:
            pass
    if default:
        return default
    else:
        raise Exception("%s not found in %s"%(t, args))

def transpose(a1):
    a2 = [[] for x in a1[0]]
    for r in a1:
        for i, x in enumerate(r):
            a2[i].append(x)
    return a2

def shuffled(l, shuffle=True):
    l = [x for x in l]
    if shuffle:
        random.shuffle(l)
    return l
