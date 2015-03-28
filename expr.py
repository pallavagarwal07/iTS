from __future__ import print_function 
from tabulate import tabulate
import re
import sys
inp = sys.stdin.read()

priority = {
        '->':100, '++':100, '--':100, 
        '+++':91, '---':91, '#':91, '_':91, '!':91, '~':91, '#type#':91,  
        '*': 80, '/':80, '%':80,
        '+':78, '-':78,
        '>>':76, '<<':76,
        '<=':70, '>=':70, '>':70, '<':70, 
        '==':66, '!=':66,
        '&':58, '^':56, '|':54, '&&':52, '||':50,
        '? :':45, 
        '=':41, '+=':41, '-=':41, '*=':41, '/=':41,
        '%=':41, '&=':41, '^=':41, '|=':41, 
        '>>=':41, '<<=':41,
        ',':10
      }
ops = (
        '#type#', '---', '? :', '+++', '<<=', '>>=', '*=', '|=', '>=', '>>', '==', '<<',
        '<=', '&=', '!=', '&&', '||', '^=', '++', '--', '/=', '%=', '-=', '->',
        '+=', ',', '>','|', '^', '!', '%', '&', '+', '#','_', '*', '-', '/',  '=',
        '<', '~', '(', ')'
      )


varTable = {}

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


def matchingBrack(code, num):
    i = num
    start = 0
    for k in range(i, len(code)):
        line = code[k]
        if line=='{':
            start += 1
        if line=='}':
            start -= 1
        if start == 0:
            return k
    return i

def calculate(expr, scope):
    postfix = []
    token=""
    stack = []
    i = 0
    expr = expr.strip()
    while i < len(expr) and expr[i]!=';':
        while i<len(expr) and expr[i] == ' ':
            i += 1
        for ex in ops:
            if expr.startswith(ex, i):
                if ex != '(':
                    postfix.append(token)
                    token = ""
                if ex == '(':
                    if token == "":
                        stack.append(ex)
                    else:
                        j=i+1;
                        str="("
                        bracks = 1
                        while bracks>0:
                            str+=expr[j]
                            if expr[j]=='(':
                                bracks += 1
                            if expr[j]==')':
                                bracks -= 1
                            j += 1
                        i += len(str)-1
                        token += str
                elif ex == ')':
                    while stack[len(stack)-1] != '(':
                        postfix.append(stack.pop())
                    stack.pop()
                elif len(stack) == 0 or stack[len(stack)-1] == '(':
                    stack.append(ex)
                else:
                    if priority[ex] < priority[stack[len(stack)-1]]:
                        postfix.append(stack.pop())
                        i-=1
                        break;
                    if priority[ex] > priority[stack[len(stack)-1]]:
                        stack.append(ex)
                    elif priority[ex] == priority[stack[len(stack)-1]]:
                        if priority[ex]%2==0:
                            postfix.append(stack.pop())
                            stack.append(ex)
                        else:
                            stack.append(ex)
                i+=len(ex)-1
                break
        else:
            token+=expr[i]
        i+=1
    if len(token)>0:
        postfix.append(token)
    while len(stack)>0:
        postfix.append(stack.pop())
    postfix = (" ".join(postfix)).split()
    stack=[]
    for k in postfix:
        if 'Error' == isNum(k):
            stack.append(k)
        else:
            m = isNum(k)
            stack.append(m)
    postfix = stack

    stack = []
    varStack = []
    l = lambda : len(stack)-1
    for token in postfix:
        if token not in ops:
            n = isNum(token)
            if 'Error' == n:
                t = inVarTable(token, scope)
                val = varTable[t][0]
                stack.append(val)
                varStack.append(token)
            else:
                stack.append(token)
                varStack.append(token)
        else:
            if token == '---':
                varTable[inVarTable(varStack[l()],scope)][0] -= 1
                stack[l()] -= 1
            elif token == '+++':
                varTable[inVarTable(varStack[l()],scope)][0] += 1
                stack[l()] += 1
            elif token == '<<=':
                varTable[inVarTable(varStack[l()-1],scope)][0] <<= stack[l()]
                stack[l()-1] <<= stack[l()]
                stack.pop()
                varStack.pop()
            elif token == '>>=':
                varTable[inVarTable(varStack[l()-1],scope)][0] >>= stack[l()]
                stack[l()-1] >>= stack[l()]
                stack.pop()
                varStack.pop()
            elif token == '*=':
                varTable[inVarTable(varStack[l()-1],scope)][0] *= stack[l()]
                stack[l()-1] *= stack[l()]
                stack.pop()
                varStack.pop()
            elif token == '|=':
                varTable[inVarTable(varStack[l()-1],scope)][0] |= stack[l()]
                stack[l()-1] |= stack[l()]
                stack.pop()
                varStack.pop()
            elif token == '>=':
                stack[l()-1] = (1 if stack[l()-1] >= stack[l()] else 0)
                stack.pop()
                varStack.pop()
            elif token == '>>':
                stack[l()-1] = (stack[l()-1]>>stack[l()])
                stack.pop()
                varStack.pop()
            elif token == '==':
                stack[l()-1] = (1 if (stack[l()-1] == stack[l()]) else 0)
                stack.pop()
                varStack.pop()
            elif token == '<<':
                stack[l()-1] = (stack[l()-1]<<stack[l()])
                stack.pop()
                varStack.pop()
            elif token == '<=':
                stack[l()-1] = (1 if stack[l()-1] <= stack[l()] else 0)
                stack.pop()
                varStack.pop()
            elif token == '&=':
                varTable[inVarTable(varStack[l()-1],scope)][0] &= stack[l()]
                stack[l()-1] &= stack[l()]
                stack.pop()
                varStack.pop()
            elif token == '!=':
                stack[l()-1] = (1 if stack[l()-1] != stack[l()] else 0)
                stack.pop()
                varStack.pop()
            elif token == '&&':
                stack[l()-1] = (1 if stack[l()-1] and stack[l()] else 0)
                stack.pop()
                varStack.pop()
            elif token == '||':
                stack[l()-1] = (1 if stack[l()-1] or stack[l()] else 0)
                stack.pop()
                varStack.pop()
            elif token == '^=':
                varTable[inVarTable(varStack[l()-1],scope)][0] ^= stack[l()]
                stack[l()-1] ^= stack[l()]
                stack.pop()
                varStack.pop()
            elif token == '++':
                varTable[inVarTable(varStack[l()],scope)][0] += 1
            elif token == '--':
                varTable[inVarTable(varStack[l()],scope)][0] -= 1
            elif token == '/=':
                varTable[inVarTable(varStack[l()-1],scope)][0] /= stack[l()]
                stack[l()-1] /= stack[l()]
                stack.pop()
                varStack.pop()
            elif token == '%=':
                varTable[inVarTable(varStack[l()-1],scope)][0] %= stack[l()]
                stack[l()-1] %= stack[l()]
                stack.pop()
                varStack.pop()
            elif token == '-=':
                varTable[inVarTable(varStack[l()-1],scope)][0] -= stack[l()]
                stack[l()-1] -= stack[l()]
                stack.pop()
                varStack.pop()
            elif token == '+=':
                varTable[inVarTable(varStack[l()-1],scope)][0] += stack[l()]
                stack[l()-1] += stack[l()]
                stack.pop()
                varStack.pop()
            elif token == ',':
                stack[l()-1] = stack[l()]
                stack.pop()
                varStack.pop()
            elif token == '>':
                stack[l()-1] = (1 if stack[l()-1] > stack[l()] else 0)
                stack.pop()
                varStack.pop()
            elif token == '|':
                stack[l()-1] = (stack[l()-1]) | (stack[l()])
                stack.pop()
                varStack.pop()
            elif token == '^':
                stack[l()-1] = (stack[l()-1]) ^ (stack[l()])
                stack.pop()
                varStack.pop()
            elif token == '!':
                stack[l()] = (0 if (stack[l()]) else 1)
            elif token == '%':
                stack[l()-1] = stack[l()-1] % stack[l()]
                stack.pop()
                varStack.pop()
            elif token == '&':
                stack[l()-1] = (stack[l()-1]) & (stack[l()])
                stack.pop()
                varStack.pop()
            elif token == '+':
                stack[l()-1] = stack[l()-1] + stack[l()]
                stack.pop()
                varStack.pop()
            elif token == '*':
                stack[l()-1] = stack[l()-1] * stack[l()]
                stack.pop()
                varStack.pop()
            elif token == '-':
                stack[l()-1] = stack[l()-1] - stack[l()]
                stack.pop()
                varStack.pop()
            elif token == '/':
                stack[l()-1] = stack[l()-1] / stack[l()]
                stack.pop()
                varStack.pop()
            elif token == '#':
                stack[l()] = stack[l()]
            elif token == '_':
                stack[l()] = -stack[l()]
            elif token == '=':
                varTable[inVarTable(varStack[l()-1],scope)][0] = stack[l()]
                stack[l()-1] = stack[l()]
                stack.pop()
                varStack.pop()
            elif token == '<':
                stack[l()-1] = (1 if stack[l()-1] < stack[l()] else 0)
                stack.pop()
                varStack.pop()
            elif token == '~':
                stack[l()] = ~stack[l()]
    return stack.pop()



def conditional(line):
    cnd = re.findall(r'^\s*if\s*\((.*)\)', line)
    if cnd==[]:
        return 0
    else:
        return cnd

def update(var, val, scope):
    key = inVarTable(var, scope)
    if key:
        varTable[key][0] = val
    else:
        print('Error')
        return


def isNum(s):
    try:
        m = float(s)
        return eval(str(s))
    except ValueError:
        return 'Error'
 
def chkDecl(line, scope):
    r = re.findall(r'^(?s)\s*(long\s+double|long\s+long\s+int|long\s+long|long\s+int|long|int|float|double|char)\s+((\s*[a-zA-Z_]+[a-zA-Z0-9_]*)(\s*=\s*(.*?))?\s*,)*((\s*[a-zA-Z_]+[a-zA-Z0-9_]*)(\s*=\s*(.*?))?\s*;)', line)
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

def handleOutput(line, scope):
    line = line.decode('string_escape')
    sep = re.findall(r'(?s)printf\s*\(\s*\"(.*)\"\s*(,.+)*\s*\)', line)
    if len(sep)==0:
        return False
    formatString = sep[0][0]
    if sep[0][1] == '':
        printString = formatString
    formatVars = sep[0][1][1:].split(',')
    for i in range(0, len(formatVars)):
        if formatVars[i] != '':
            formatVars[i] = calculate(formatVars[i].strip(), scope)
            #print(type(formatVars[i]))
    formatString = re.sub(r'%(lld|ld|d)', '%d', formatString)
    formatString = re.sub(r'%(Lf|lf|f)', '%f', formatString)
    if sep[0][1] != '':
        printString = formatString % tuple(formatVars)
    sys.stdout.write(printString)
    return True



def inVarTable(var, scope):
    if type(scope) is str:
        scope = scope.split(' ')
    else:
        scope = scope[:]
    while len(scope)>0:
        if (var, " ".join(scope)) in varTable:
            return (var, " ".join(scope))
        scope.pop()
    return 0

def handleInput(statement, scope):
    global inp
    statement = statement.decode('string_escape')
    sep = re.findall(r'(?s)scanf\s*\(\s*\"(.*)\"\s*,(.*,)*(.*)\)', statement)
    if len(sep)==0:
        return False
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
    #print(values)
    #print(vars)
    #print(inp)
    if len(values[0]) != len(vars):
        print("Incorrect number of arguments or bug in my interpreter")
    else:
        for i in range(0, len(vars)):
            v = vars[i].strip()
            vals = (eval(values[0][i]) if isNum(values[0][i]) != 'Error' else values[0][i])
            print(v, vals, " ".join(Access))
            update(v, vals, " ".join(Access))
    return True


def decl(var, val, cast, scope):
    key = inVarTable(var, scope)
    if key and key[1]==scope:
        print("Error")
        return
    varTable[(var, scope)] = [val, cast, scope]

def handleNum(s):
    try:
        m = float(s)
        return eval(str(s))
    except ValueError:
        return s


conditional('if(c==1 && (k!=4))')

def nest(code):
    bracks = []
    i=0
    while i<len(code):
        if code[i]=='{':
            bracks.append(i)
        elif code[i]=='}':
            match = bracks.pop()
            code = code[:match] + [code[match+1:i]] + code[i+1:]
            i = match+1
        i += 1

    return code

def isUpdation(exp):
    k = re.match(r'^(?s)\s*[a-zA-Z_]+[a-zA-Z0-9_]*\s*=.*;', exp)
    return (1 if k else 0)

def execute(code, scope):
    print(code)
    if type(code) is str:
        exec([code], scope)
        return
    for i in range(0, len(code)):
        print(varTable)
        line = code[i]
        try:
            if type(line) is list:
                execute(line, scope+[str(i)])
                continue
            if len(line)<1:
                continue
            if chkDecl(line, " ".join(scope)):
                continue
            if handleInput(line, " ".join(scope)):
                continue
            if handleOutput(line, " ".join(scope)):
                continue
            if isUpdation(line):
                calculate(line, " ".join(Access))
                continue
        except Exception:
            print('Exception caught!! : ', line)
            exit(0)



code = nest(code)
execute(code, ['global'])
