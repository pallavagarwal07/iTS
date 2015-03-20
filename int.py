from __future__ import print_function
from math import *
from tabulate import tabulate
import sys
import re
inp = sys.stdin.read()

def handleOutput(line, scope):
    line = line.decode('string_escape')
    sep = re.findall(r'(?s)printf\s*\(\s*\"(.*)\"\s*(,.+)*\s*\)', line)
    formatString = sep[0][0]
    if sep[0][1] is '':
        printString = formatString
    formatVars = sep[0][1][1:].split(',')
    for i in range(0, len(formatVars)):
        if formatVars[i] is not '':
            formatVars[i] = calculate(formatVars[i].strip(), scope)
    formatString = re.sub(r'%(lld|ld|d)', '%d', formatString)
    formatString = re.sub(r'%(Lf|lf|f)', '%f', formatString)
    if sep[0][1] is not '':
        printString = formatString % tuple(formatVars)

    print ("I am printing :\n"+printString)

def handleInput(statement, inp, scope):
    statement = statement.decode('string_escape')
    sep = re.findall(r'(?s)scanf\s*\(\s*\"(.*)\"\s*,(.*,)*(.*)\)', statement)
    types = re.findall(r'%(lld|Lf|lf|ld|d|c|s|f)', sep[0][0])
    vars = sep[0][1].replace('&', '').split(',')
    vars.append(sep[0][2].replace('&', ''))
    vars.remove('')
    reg = re.sub(r'%(lld|ld|d)','%d', sep[0][0])
    reg = re.sub(r'%(Lf|lf|f)', '%f', reg)
    reg = reg.replace(' ', r'\s+')
    reg = reg.replace('\n', r'\s+')
    reg = reg.replace('\r', r'\s+')
    reg = reg.replace('%d', r'\s*([-+]?\d+)')
    reg = reg.replace('%f', r'\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)')
    reg = reg.replace('%c', r'[\n\r]*(.)')
    reg = reg.replace('%s', r'\s*(\S+)')
    reg = '^'+reg
    values = re.findall(reg, inp)
    inp = re.sub(reg, '', inp)
    print(values)
    print(vars)
    print(inp)
    if len(values[0]) is not len(vars):
        print("Incorrect number of arguments or bug in my interpreter")
    else:
        for i in range(0, len(vars)):
            v = vars[i].strip()
            vals = values[0][i]
            update(v, vals, " ".join(Access))

def pow(a, b):
    return a**b

varTable = {}

def split(exp):
    exp.replace(' ','')
    line = list(exp)
    br = 0
    for i in range(0, len(line)):
        ch = line[i]
        if br is 0 and isSymbol(ch):
            line[i]=';;-;;'+line[i]+';;-;;'
        if ch is '(':
            br+=1
        if ch is ')':
            br-=1
    tokens = "".join(line).split(';;-;;')
    return tokens


def isSymbol(ch):
    symbols = ['+', '-', '/', '*', '|', '&', '^', '&&', '||']
    if ch in symbols:
        return 1
    return 0

def inVarTable(var, scope):
    scope = scope.split()
    while len(scope)>0:
        if (var, " ".join(scope)) in varTable:
            return (var, " ".join(scope))
        scope.pop()
    return 0


def isUpdation(line, scope):
    if line.count('==')==2*line.count('='):
        return 0
    line = line.replace('=', ' = ').replace(';', ' ').split()
    if '=' in line[1]:
        update(line[0], calculate(" ".join(line[2:]), " ".join(Access)), " ".join(Access))
        return 1
    return 0


def calculate(exp, scope):
    if isUpdation(exp, scope):
        return
    tokens = split(exp)
    for i in range(0, len(tokens)):
        tk = tokens[i]
        if isSymbol(tk):
            continue
        if 'Error' not in isNum(tk):
            continue
        t = inVarTable(tk, scope)
        print(varTable)
        if t:
            tokens[i] = str(varTable[t][0])
            continue
        if tk.strip()[0]=='(':
            word = list(tk.strip())
            word[0]=''
            if word[-1]==')':
                word[-1]=''
            else:
                print("Error")
                return
            tokens[i]=str(calculate(''.join(word), scope))
    return eval("".join(tokens))




def checkDecl(line):
    if re.match('^\s*(long double|long long int|long long|int|float|double|char)\s+(.*?);', line):
        a = re.findall('^\s*(long double|long long int|long long|int|float|double|char)\s+(.*?);', line)
        return a[0][0]
    return 0

def isNum(s):
    try:
        float(s)
        return s
    except ValueError:
        return 'Error'


def val(token):
    k = isNum(token)
    if k not in 'Error':
        return k
    if k in varTable:
        return varTable[k][0]
    j_unusedVar = eval(token)
    return j_unusedVar

def decl(var, val, cast, scope):
    key = inVarTable(var, scope)
    if key and key[1]==scope:
        print("Error")
        return
    varTable[(var, scope)] = [val, cast, scope]

def update(var, val, scope):
    key = inVarTable(var, scope)
    if key:
        varTable[key][0] = val
    else:
        print('Error')
        return

# Preprocessing does not ignore double quoted things yet

file = open('newTest.c')
filenew = open('buffer.c', 'w')

for line in file:
    line = line.replace('{', '\n{\n').replace('}', '\n}\n').replace(';', ';\n')
    if '//' in line:
        line.replace('//', '\n//')
    print(line , file=filenew)


filenew.close()
file = open('buffer.c')
str1=''
filenew = open('corrected.c', 'w')
for line in file:
    line = " ".join(line.split());
    if len(line.split()) < 1:
        continue
    if '//' in line:
        continue
    str1+=(line+'\n')
str1 = re.sub(r'(?s)\/\*.*?\*\/', '', str1)
print(str1, file=filenew)

filenew.close()

def allow(a):
    print('Importing '+a)

def printVT(varTable):
    print(tabulate(varTable))
# The file has been preprocessed and extra spaces, tabs, 
#empty lines have been (hopefully) removed from the source code.

file = open('corrected.c')
Access = ['global']
code = []
for line in file:
    code.append(line.strip())


for i in range(0, len(code)):
    line = code[i]
    if len(line)<1:
        continue
    if '#include' in line and Access is 'global':
        imp = line.replace(' ', '').replace('<', ' ').replace('>', ' ').replace('.', ' ').split(' ')[1]
        allow(imp)
    if Access is 'global' and line[-1] is ';':
        print(Access+' definition')
    if '{' in line:
        Access.append("%d"%i)
    if '}' in line:
        Access.pop()
    k=checkDecl(line)
    if line == 'DEBUGMODE':
        handleInput('scanf("%d %d %f", &a, &b, &k);', inp, " ".join(Access))
        print(varTable)
    if k:
        packs = line.replace(k, ' ').replace(';', ' ').strip()
        packs = packs.split(',');
        for dec in packs:
            dec = dec.strip().split('=')
            ran = range(-len(dec), -1)
            ran.reverse()
            for j in ran:
                if j is -len(dec):
                    decl(dec[j].strip(), calculate(dec[-1], " ".join(Access)), k, " ".join(Access))
                else:
                    update(dec[j].strip(), calculate(dec[-1], " ".join(Access)), " ".join(Access))
        continue
    if '=' in line and '==' not in line:
        dec = line.replace(';', ' ').strip().split('=')
        ran = range(-len(dec), -1)
        ran.reverse()
        for j in ran:
            update(dec[j].strip(), calculate(dec[-1], " ".join(Access)), " ".join(Access))
    if re.match(r'(?s)printf\s*\(\s*\"(.*)\"(,.+)*\s*\)', line):
        handleOutput(line, " ".join(Access))
