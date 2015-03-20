from tabulate import tabulate
import re
import sys

priority = {
        '.':100, '->':100, '++':100, '--':100, 
        '+++':91, '---':91, '+':91, '-':91, '!':91, '~':91, '#type#':91,  
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
        '+=', ',', '>','|', '^', '!', '%', '&', '+', '*', '-', '/', '.', '=', '<', '~', '(', ')')

def calc(expr, scope):
    postfix = []
    token=""
    stack = []
    i = 0
    while i < len(expr) and expr[i]!=';':
        for ex in ops:
            if expr.startswith(ex, i):
                if ex is not '(':
                    postfix.append(token)
                    token = ""
                print "length of stack is : %d"%len(stack)
                if len(stack) is 0 or stack[len(stack)-1] is '(':
                    stack.append(ex)
                elif ex is '(':
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
        print "-------"
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
    print " ".join(postfix)




calc('1+1', 'global')




