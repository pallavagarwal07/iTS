from __future__ import print_function 
from tabulate import tabulate
import re
import sys
inp = sys.stdin.read()

genStatement = 'long double df, a=90, f78_gh=\'5\', mn=90;'


def chkDecl(line, scope):
    r = re.findall(r'^(?s)\s*(long\s+double|long\s+long\s+int|long\s+long|long\s+int|long|int|float|double|char)\s+((\s*[a-zA-Z_]+[a-zA-Z0-9_]*)(\s*=\s*(.*?))?\s*,)*((\s*[a-zA-Z_]+[a-zA-Z0-9_]*)(\s*=\s*(.*?))?\s*;)',s)
    if r != []:
        r = r[0]
        cast = r[0]
        a = re.sub(cast, '', line)
        a = re.sub(';', '', a)
        a = a.split(',')
        a = [k.strip().split('=') for k in a]
        for vars in a:
            if len(vars)==1:
                decl(vars[0], '', cast, scope)
            else:
                decl(vars[0], handleNum(vars[1]), cast, scope)
        return True
    else:
        return False


def handleNum(s):
    try:
        m = float(s)
        return eval(str(s))
    except ValueError:
        return s

s=genStatement
chkDecl(s, 'global')


