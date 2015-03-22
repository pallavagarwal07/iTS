from tabulate import tabulate
import re
import sys
    
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
ops = ('#type#', '---', '? :', '+++', '<<=', '>>=', '*=', '|=', '>=', '>>', '==', '<<',
        '<=', '&=', '!=', '&&', '||', '^=', '++', '--', '/=', '%=', '-=', '->',
        '+=', ',', '>','|', '^', '!', '%', '&', '+', '#','_', '*', '-', '/',  '=',
        '<', '~', '(', ')')

def isNum(s):
    try:
        m = float(s)
        return eval(str(s))
    except ValueError:
        return 'Error'
   
def calc(expr, scope):
    postfix = []
    token=""
    stack = []
    i = 0
    expr = expr.strip()
    while i < len(expr) and expr[i]!=';':
        while i<len(expr) and expr[i] is ' ':
            i += 1
        for ex in ops:
            if expr.startswith(ex, i):
                if ex is not '(':
                    postfix.append(token)
                    token = ""
                print "length of stack is : %d"%len(stack)
                if ex is '(':
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
                elif ex is ')':
                    while stack[len(stack)-1] is not '(':
                        postfix.append(stack.pop())
                    stack.pop()
                elif len(stack) is 0 or stack[len(stack)-1] is '(':
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
        print "--------"
        print stack
        print postfix
        print expr
        print token
        print i
        print "########"
        i+=1
    if len(token)>0:
        postfix.append(token)
    for tk in stack:
        postfix.append(stack.pop())
    postfix = (" ".join(postfix)).split()
    stack=[]
    for k in postfix:
        if 'Error' is isNum(k):
            print "Here",k,"appended"
            stack.append(k)
        else:
            m = isNum(k)
            stack.append(m)
            print stack
    print "stack is ", stack
    postfix = stack
    print postfix

    stack = []
    varStack = []
    l = lambda : len(stack)-1
    for token in postfix:
        if token not in ops:
            n = isNum(token)
            if 'Error' is n:
                t = inVarTable(token, scope)
                val = varTable[t][0]
                stack.append(val)
                varStack.append(token)
            else:
                stack.append(token)
                varStack.append(token)
        else:
            if token is '---':
                varTable[inVarTable(varStack[l()],scope)][0] -= 1
                stack[l()] -= 1
            elif token is '+++':
                varTable[inVarTable(varStack[l()],scope)][0] += 1
                stack[l()] += 1
            elif token is '<<=':
                varTable[inVarTable(varStack[l()-1],scope)][0] <<= stack[l()]
                stack[l()-1] <<= stack[l()]
                stack.pop()
            elif token is '>>=':
                varTable[inVarTable(varStack[l()-1],scope)][0] >>= stack[l()]
                stack[l()-1] >>= stack[l()]
                stack.pop()
            elif token is '*=':
                varTable[inVarTable(varStack[l()-1],scope)][0] *= stack[l()]
                stack[l()-1] *= stack[l()]
                stack.pop()
            elif token is '|=':
                varTable[inVarTable(varStack[l()-1],scope)][0] |= stack[l()]
                stack[l()-1] |= stack[l()]
                stack.pop()
            elif token is '>=':
                stack[l()-1] = (1 if stack[l()-1] >= stack[l()] else 0)
                stack.pop()
            elif token is '>>':
                stack[l()-1] = (stack[l()-1]>>stack[l()])
                stack.pop()
            elif token is '==':
                stack[l()-1] = (1 if stack[l()-1] == stack[l()] else 0)
                stack.pop()
            elif token is '<<':
                stack[l()-1] = (stack[l()-1]<<stack[l()])
                stack.pop()
            elif token is '<=':
                stack[l()-1] = (1 if stack[l()-1] <= stack[l()] else 0)
                stack.pop()
            elif token is '&=':
                varTable[inVarTable(varStack[l()-1],scope)][0] &= stack[l()]
                stack[l()-1] &= stack[l()]
                stack.pop()
            elif token is '!=':
                stack[l()-1] = (1 if stack[l()-1] != stack[l()] else 0)
                stack.pop()
            elif token is '&&':
                stack[l()-1] = (1 if stack[l()-1] and stack[l()] else 0)
                stack.pop()
            elif token is '||':
                stack[l()-1] = (1 if stack[l()-1] or stack[l()] else 0)
                stack.pop()
            elif token is '^=':
                varTable[inVarTable(varStack[l()-1],scope)][0] ^= stack[l()]
                stack[l()-1] ^= stack[l()]
                stack.pop()
            elif token is '++':
                varTable[inVarTable(varStack[l()],scope)][0] += 1
            elif token is '--':
                varTable[inVarTable(varStack[l()],scope)][0] -= 1
            elif token is '/=':
                varTable[inVarTable(varStack[l()-1],scope)][0] /= stack[l()]
                stack[l()-1] /= stack[l()]
                stack.pop()
            elif token is '%=':
                varTable[inVarTable(varStack[l()-1],scope)][0] %= stack[l()]
                stack[l()-1] %= stack[l()]
                stack.pop()
            elif token is '-=':
                varTable[inVarTable(varStack[l()-1],scope)][0] -= stack[l()]
                stack[l()-1] -= stack[l()]
                stack.pop()
            elif token is '+=':
                varTable[inVarTable(varStack[l()-1],scope)][0] += stack[l()]
                stack[l()-1] += stack[l()]
                stack.pop()
            elif token is ',':
                stack[l()-1] = stack[l()]
                stack.pop()
            elif token is '>':
                stack[l()-1] = (1 if stack[l()-1] > stack[l()] else 0)
                stack.pop()
            elif token is '|':
                stack[l()-1] = (stack[l()-1]) | (stack[l()])
                stack.pop()
            elif token is '^':
                stack[l()-1] = (stack[l()-1]) ^ (stack[l()])
                stack.pop()
            elif token is '!':
                stack[l()] = (0 if (stack[l()]) else 1)
            elif token is '%':
                stack[l()-1] = stack[l()-1] % stack[l()]
                stack.pop()
            elif token is '&':
                stack[l()-1] = (stack[l()-1]) & (stack[l()])
                stack.pop()
            elif token is '+':
                stack[l()-1] = stack[l()-1] + stack[l()]
                stack.pop()
            elif token is '*':
                stack[l()-1] = stack[l()-1] * stack[l()]
                stack.pop()
            elif token is '-':
                stack[l()-1] = stack[l()-1] - stack[l()]
                stack.pop()
            elif token is '/':
                stack[l()-1] = stack[l()-1] / stack[l()]
                stack.pop()
            elif token is '#':
                stack[l()] = stack[l()]
            elif token is '_':
                stack[l()] = -stack[l()]
            elif token is '=':
                varTable[inVarTable(varStack[l()-1],scope)][0] = stack[l()]
                stack[l()-1] = stack[l()]
                stack.pop()
            elif token is '<':
                stack[l()-1] = (1 if stack[l()-1] < stack[l()] else 0)
                stack.pop()
            elif token is '~':
                stack[l()] = ~stack[l()]
    print stack








    
    
    
calc( '7/8.0', 'global')
