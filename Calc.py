import globals
from Utils import is_num


def calculate(expr, scope, vartable):
    postfix = []
    token = ""
    stack = []
    i = 0
    expr = expr.strip()
    while i < len(expr) and expr[i] != ';':
        while i < len(expr) and expr[i] == ' ':
            i += 1
        for ex in globals.ops:
            if expr.startswith(ex, i):
                if ex != '(':
                    postfix.append(token)
                    token = ""
                if ex == '(':
                    if token == "":
                        stack.append(ex)
                    else:
                        j = i + 1
                        expression = "("
                        bracks = 1
                        while bracks > 0:
                            expression += expr[j]
                            if expr[j] == '(':
                                bracks += 1
                            if expr[j] == ')':
                                bracks -= 1
                            j += 1
                        i += len(expression) - 1
                        token += expression
                elif ex == ')':
                    while stack[len(stack) - 1] != '(':
                        postfix.append(stack.pop())
                    stack.pop()
                elif len(stack) == 0 or stack[len(stack) - 1] == '(':
                    stack.append(ex)
                else:
                    if globals.priority[ex] < globals.priority[stack[len(stack) - 1]]:
                        postfix.append(stack.pop())
                        i -= 1
                        break
                    if globals.priority[ex] > globals.priority[stack[len(stack) - 1]]:
                        stack.append(ex)
                    elif globals.priority[ex] == globals.priority[stack[len(stack) - 1]]:
                        if globals.priority[ex] % 2 == 0:
                            postfix.append(stack.pop())
                            stack.append(ex)
                        else:
                            stack.append(ex)
                i += len(ex) - 1
                break
        else:
            token += expr[i]
        i += 1
    if len(token) > 0:
        postfix.append(token)
    while len(stack) > 0:
        postfix.append(stack.pop())
    postfix = (" ".join(postfix)).split()
    stack = []
    for k in postfix:
        if 'Error' == is_num(k):
            stack.append(k)
        else:
            m = is_num(k)
            stack.append(m)
    postfix = stack

    stack = []
    var_stack = []
    l = lambda: len(stack) - 1
    # print "Postfix is:", postfix
    for token in postfix:
        if token not in globals.ops:
            n = is_num(token)
            if 'Error' == n:
                t = globals.in_var_table(token, scope)
                val = vartable[t][0]
                stack.append(val)
                var_stack.append(token)
            else:
                stack.append(token)
                var_stack.append(token)
        else:
            if token == '---':
                vartable[globals.in_var_table(var_stack[l()], scope)][0] -= 1
                stack[l()] -= 1
            elif token == '+++':
                vartable[globals.in_var_table(var_stack[l()], scope)][0] += 1
                stack[l()] += 1
            elif token == '<<=':
                vartable[globals.in_var_table(var_stack[l() - 1], scope)][0] <<= stack[l()]
                stack[l() - 1] <<= stack[l()]
                stack.pop()
                var_stack.pop()
            elif token == '>>=':
                vartable[globals.in_var_table(var_stack[l() - 1], scope)][0] >>= stack[l()]
                stack[l() - 1] >>= stack[l()]
                stack.pop()
                var_stack.pop()
            elif token == '*=':
                vartable[globals.in_var_table(var_stack[l() - 1], scope)][0] *= stack[l()]
                stack[l() - 1] *= stack[l()]
                stack.pop()
                var_stack.pop()
            elif token == '|=':
                vartable[globals.in_var_table(var_stack[l() - 1], scope)][0] |= stack[l()]
                stack[l() - 1] |= stack[l()]
                stack.pop()
                var_stack.pop()
            elif token == '>=':
                stack[l() - 1] = (1 if stack[l() - 1] >= stack[l()] else 0)
                stack.pop()
                var_stack.pop()
            elif token == '>>':
                stack[l() - 1] = (stack[l() - 1] >> stack[l()])
                stack.pop()
                var_stack.pop()
            elif token == '==':
                stack[l() - 1] = (1 if (stack[l() - 1] == stack[l()]) else 0)
                stack.pop()
                var_stack.pop()
            elif token == '<<':
                stack[l() - 1] = (stack[l() - 1] << stack[l()])
                stack.pop()
                var_stack.pop()
            elif token == '<=':
                stack[l() - 1] = (1 if stack[l() - 1] <= stack[l()] else 0)
                stack.pop()
                var_stack.pop()
            elif token == '&=':
                vartable[globals.in_var_table(var_stack[l() - 1], scope)][0] &= stack[l()]
                stack[l() - 1] &= stack[l()]
                stack.pop()
                var_stack.pop()
            elif token == '!=':
                stack[l() - 1] = (1 if stack[l() - 1] != stack[l()] else 0)
                stack.pop()
                var_stack.pop()
            elif token == '&&':
                stack[l() - 1] = (1 if stack[l() - 1] and stack[l()] else 0)
                stack.pop()
                var_stack.pop()
            elif token == '||':
                stack[l() - 1] = (1 if stack[l() - 1] or stack[l()] else 0)
                stack.pop()
                var_stack.pop()
            elif token == '^=':
                vartable[globals.in_var_table(var_stack[l() - 1], scope)][0] ^= stack[l()]
                stack[l() - 1] ^= stack[l()]
                stack.pop()
                var_stack.pop()
            elif token == '++':
                vartable[globals.in_var_table(var_stack[l()], scope)][0] += 1
            elif token == '--':
                vartable[globals.in_var_table(var_stack[l()], scope)][0] -= 1
            elif token == '/=':
                vartable[globals.in_var_table(var_stack[l() - 1], scope)][0] /= stack[l()]
                stack[l() - 1] /= stack[l()]
                stack.pop()
                var_stack.pop()
            elif token == '%=':
                vartable[globals.in_var_table(var_stack[l() - 1], scope)][0] %= stack[l()]
                stack[l() - 1] %= stack[l()]
                stack.pop()
                var_stack.pop()
            elif token == '-=':
                vartable[globals.in_var_table(var_stack[l() - 1], scope)][0] -= stack[l()]
                stack[l() - 1] -= stack[l()]
                stack.pop()
                var_stack.pop()
            elif token == '+=':
                vartable[globals.in_var_table(var_stack[l() - 1], scope)][0] += stack[l()]
                stack[l() - 1] += stack[l()]
                stack.pop()
                var_stack.pop()
            elif token == ',':
                stack[l() - 1] = stack[l()]
                stack.pop()
                var_stack.pop()
            elif token == '>':
                stack[l() - 1] = (1 if stack[l() - 1] > stack[l()] else 0)
                stack.pop()
                var_stack.pop()
            elif token == '|':
                stack[l() - 1] = (stack[l() - 1]) | (stack[l()])
                stack.pop()
                var_stack.pop()
            elif token == '^':
                stack[l() - 1] = (stack[l() - 1]) ^ (stack[l()])
                stack.pop()
                var_stack.pop()
            elif token == '!':
                stack[l()] = (0 if (stack[l()]) else 1)
            elif token == '%':
                stack[l() - 1] = stack[l() - 1] % stack[l()]
                stack.pop()
                var_stack.pop()
            elif token == '&':
                stack[l() - 1] = (stack[l() - 1]) & (stack[l()])
                stack.pop()
                var_stack.pop()
            elif token == '+':
                stack[l() - 1] = stack[l() - 1] + stack[l()]
                stack.pop()
                var_stack.pop()
            elif token == '*':
                stack[l() - 1] = stack[l() - 1] * stack[l()]
                stack.pop()
                var_stack.pop()
            elif token == '-':
                stack[l() - 1] = stack[l() - 1] - stack[l()]
                stack.pop()
                var_stack.pop()
            elif token == '/':
                stack[l() - 1] = stack[l() - 1] / stack[l()]
                stack.pop()
                var_stack.pop()
            elif token == '#':
                stack[l()] = stack[l()]
            elif token == '_':
                stack[l()] = -stack[l()]
            elif token == '=':
                vartable[globals.in_var_table(var_stack[l() - 1], scope)][0] = stack[l()]
                stack[l() - 1] = stack[l()]
                stack.pop()
                var_stack.pop()
            elif token == '<':
                stack[l() - 1] = (1 if stack[l() - 1] < stack[l()] else 0)
                stack.pop()
                var_stack.pop()
            elif token == '~':
                stack[l()] = ~stack[l()]
    return stack.pop()