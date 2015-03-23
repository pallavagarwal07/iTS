from __future__ import print_function 
from tabulate import tabulate
import re
import sys
inp = sys.stdin.read()

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
file = open('corrected.c')
Access = ['global']
code = []
for line in file:
    code.append(line.strip())

def initDecl(line, scope):
    flag = re.findall(r'^(?s)\s*(long\s+double|long\s+long\s+int|long\s+long|long\s+int|long|int|float|double|char)\s+([a-zA-Z_]+[a-zA-Z0-9_]*)\s*=\s*(.*?);', line)
    if flag==[]:
        return False
    else:
        decl(flag[0][1], calculate(flag[0][2]), flag[0][0], scope)
        return True


#for i in range(0, len(code)):
    #line = code[i]
    #if Access[len(Access)-1]=='global':

        #if re.match(r'^#include', line):
            #print("Something included :P")
            #continue
        #if initDecl(line, " ".join(Access)):
            #continue
        #if unInitDecl(line, " ".join(Access)):
            #continue

