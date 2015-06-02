import globals
import re
from globals import is_num
from Vars import get_val, set_val
import random
import Runtime


def sep(expr):
    print "Sep takes in ", expr, "and gives ",
    expr = expr.split()
    tokens = []
    for token in expr:
        tk = ''
        i = 0
        while i < len(token) and token[i] != ';':
            for ex in globals.ops:
                if token.startswith(ex, i):
                    if tk.strip():
                        tokens.append(tk)
                    tk = ''
                    tokens.append(ex)
                    i += len(ex) - 1
                    break
            else:
                tk += token[i]
            i += 1
        if tk.strip():
            tokens.append(tk)
    print tokens
    return tokens


def pass_to_func(detail, scope):
    name = detail[0]
    l = len(globals.toplevelsplit(detail[1], ','))
    if name == 'sizeof':
        t = re.findall(r'\*', detail[1])
        if t:
            return globals.size_of['pointer']
        else:
            detail = globals.toplevelsplit(detail[1], ',')
            assert len(detail) == 1
            return globals.size_of[detail[0].strip()]
    elif name == 'malloc':
        size = calculate(detail[1].strip(), scope)
        print "Request for", size
        exit(0)
    if name not in globals.functions:
        print "Error!! Undeclared Function", name
        exit(0)
    if len(globals.functions[name][3]) != l:
        print "Error!! Incorrect no. of parameters"
        exit(0)
    if globals.functions[name][2] == '':
        print "Error!! The function was declared, but never defined."
        exit(0)
    detail = globals.toplevelsplit(detail[1], ',')
    detail = [calculate(str(k).strip(), scope) for k in detail]

    RandomHash = hex(random.getrandbits(64))[2:-1]
    for i, declarations in enumerate(globals.functions[name][1]):
        import Runtime
        Runtime.decl(declarations[1], detail[i], declarations[0], "global " + name + " " + RandomHash)
    return Runtime.execute(globals.functions[name][2], "global " + name + " " + RandomHash)


def calculate(expr, scope, vartable=globals.var_table):
    print "Calculate has ", expr
    if re.match(r"^(?s)\s*$", expr):
        return 0
    postfix = []
    stack = []
    expr = expr.strip()
    k = list(set(re.findall(r'--\s*[a-zA-Z_]+[a-zA-Z0-9_]*', expr)))
    k2 = []
    for i in range(0, len(k)):
        k2.append(k[i].replace('--', '---'))
        expr = globals.toplevelreplace(expr, k[i], k2[i])
    k = list(set(re.findall(r'\+\+\s*[a-zA-Z_]+[a-zA-Z0-9_]*', expr)))
    k2 = []
    for i in range(0, len(k)):
        k2.append(k[i].replace('++', '+++'))
        expr = globals.toplevelreplace(expr, k[i], k2[i])
    seperated_tokens = sep(expr)
    flag = 1
    for i, token in enumerate(seperated_tokens):
        if token in globals.unary_ops and flag:
            seperated_tokens[i] = globals.unary_ops[token]
            continue
        if token in globals.bin_ops or token == '(':
            flag = 1
            continue
        flag = 0
    expr = " ".join(seperated_tokens)
    token = ''
    i = 0
    print "Calcuate step2 ", expr
    while i < len(expr) and expr[i] != ';':
        while i < len(expr) and expr[i] == ' ':
            i += 1
        for ex in globals.ops + ('[',"'"):
            if expr.startswith(ex, i):
                if ex != '(' and ex != '[':
                    postfix.append(token)
                    token = ''
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
                elif ex == '[':
                    j = i + 1
                    expression = "["
                    bracks = 1
                    while bracks > 0:
                        expression += expr[j]
                        if expr[j] == '[' and expr[j-1]!="'":
                            bracks += 1;
                        if expr[j] == ']' and expr[j-1]!="'":
                            bracks -= 1;
                        j+=1
                    i += len(expression) - 1
                    token += expression
                elif ex == '\'':
                    assert token == ""
                    j = i + 1
                    expression = "'"
                    while expr[j] != "'" or expr[j-1] == '\\':
                        expression += expr[j]
                        print "I added '"+expr[j]+"'", expr
                        j += 1
                    expression += expr[j]
                    i += len(expression) - 1
                    token += expression
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
                if ex == '&&':
                    postfix.append('&0')
                elif ex == '||':
                    postfix.append('|1')
                i += len(ex) - 1
                break
        else:
            token += expr[i]
            if token not in expr:
                print('Error 102: Did you miss the operator between'
                      ' two values/variables?\n' + token + '\n' + expr + '\n')
                # exit(0)
        i += 1
    if len(token) > 0:
        postfix.append(token)
    while len(stack) > 0:
        postfix.append(stack.pop())
    stack = []
    for k in postfix:
        if 'Error' == is_num(k):
            if k:
                stack.append(k)
        else:
            m = is_num(k)
            stack.append(m)
    postfix = stack
    print "POST", postfix

    var_stack = []
    l = lambda: len(var_stack) - 1
    idx = 0
    for i, token in enumerate(postfix):
        if idx and postfix[i-1] != idx:
            continue
        idx = 0
        if token not in globals.ops + ('&0', '|1'):
            n = is_num(token)
            if 'Error' == n:
                k = re.findall('^\s*([a-zA-Z_]+[a-zA-Z0-9_]*)\s*\((.*)\)\s*$', token)
                if k:
                    val = pass_to_func(k[0], scope)
                    var_stack.append(val)
                else:
                    t = Runtime.get_key(token, scope)
                    var_stack.append(t)
            else:
                var_stack.append(token)
        else:
            if token == '---':
                if type(var_stack[l()]) is not tuple:
                    print "Error: Lvalue required"
                    exit(0)
                set_val(var_stack[l()], get_val(var_stack[l()]) - 1)
            elif token == '+++':
                if type(var_stack[l()]) is not tuple:
                    print "Error: Lvalue required"
                    exit(0)
                set_val(var_stack[l()], get_val(var_stack[l()]) + 1)
            elif token == '`*`':
                var_stack[l()] = (get_val(var_stack[l()]),) # Do not remove the comma. It forces formation of a tuple
            elif token == '`&`':
                var_stack[l()] = vartable[var_stack[l()]][3]
            elif token == '<<=':
                if type(var_stack[l() - 1]) is not tuple:
                    print "Error: Lvalue required"
                    exit(0)
                set_val(var_stack[l() - 1], get_val(var_stack[l() - 1]) << get_val(var_stack[l()]))
                var_stack.pop()
            elif token == '>>=':
                if type(var_stack[l() - 1]) is not tuple:
                    print "Error: Lvalue required"
                    exit(0)
                set_val(var_stack[l() - 1], get_val(var_stack[l() - 1]) >> get_val(var_stack[l()]))
                var_stack.pop()
            elif token == '|1':
                if get_val(var_stack[l()]):
                    var_stack[l()] = 1
                    idx = '||'
            elif token == '&0':
                if not get_val(var_stack[l()]):
                    var_stack[l()] = 0
                    idx = '&&'
            elif token == '*=':
                if type(var_stack[l() - 1]) is not tuple:
                    print "Error: Lvalue required"
                    exit(0)
                set_val(var_stack[l() - 1], get_val(var_stack[l() - 1]) * get_val(var_stack[l()]))
                var_stack.pop()
            elif token == '|=':
                if type(var_stack[l() - 1]) is not tuple:
                    print "Error: Lvalue required"
                    exit(0)
                set_val(var_stack[l() - 1], get_val(var_stack[l() - 1]) | get_val(var_stack[l()]))
                var_stack.pop()
            elif token == '>=':
                var_stack[l() - 1] = (1 if get_val(var_stack[l() - 1]) >= get_val(var_stack[l()]) else 0)
                var_stack.pop()
            elif token == '>>':
                var_stack[l() - 1] = (get_val(var_stack[l() - 1]) >> get_val(var_stack[l()]))
                var_stack.pop()
            elif token == '==':
                var_stack[l() - 1] = (1 if (get_val(var_stack[l() - 1]) == get_val(var_stack[l()])) else 0)
                var_stack.pop()
            elif token == '<<':
                var_stack[l() - 1] = (get_val(var_stack[l() - 1]) << get_val(var_stack[l()]))
                var_stack.pop()
            elif token == '<=':
                var_stack[l() - 1] = (1 if get_val(var_stack[l() - 1]) <= get_val(var_stack[l()]) else 0)
                var_stack.pop()
            elif token == '&=':
                if type(var_stack[l() - 1]) is not tuple:
                    print "Error: Lvalue required"
                    exit(0)
                set_val(var_stack[l() - 1], get_val(var_stack[l() - 1]) & get_val(var_stack[l()]))
                var_stack.pop()
            elif token == '!=':
                var_stack[l() - 1] = (1 if get_val(var_stack[l() - 1]) != get_val(var_stack[l()]) else 0)
                var_stack.pop()
            elif token == '&&':
                var_stack[l() - 1] = (1 if get_val(var_stack[l() - 1]) and get_val(var_stack[l()]) else 0)
                var_stack.pop()
            elif token == '||':
                var_stack[l() - 1] = (1 if get_val(var_stack[l() - 1]) or get_val(var_stack[l()]) else 0)
                var_stack.pop()
            elif token == '^=':
                if type(var_stack[l() - 1]) is not tuple:
                    print "Error: Lvalue required"
                    exit(0)
                set_val(var_stack[l() - 1], get_val(var_stack[l() - 1]) ^ get_val(var_stack[l()]))
                var_stack.pop()
            elif token == '++':
                if type(var_stack[l()]) is not tuple:
                    print "Error: Lvalue required"
                    exit(0)
                set_val(var_stack[l()], get_val(var_stack[l()]) + 1)
            elif token == '--':
                if type(var_stack[l()]) is not tuple:
                    print "Error: Lvalue required"
                    exit(0)
                set_val(var_stack[l()], get_val(var_stack[l()]) - 1)
            elif token == '/=':
                if type(var_stack[l() - 1]) is not tuple:
                    print "Error: Lvalue required"
                    exit(0)
                if get_val(var_stack[l()]) == 0:
                    print "Division by 0 not permitted"
                    exit(0)
                set_val(var_stack[l() - 1], get_val(var_stack[l() - 1]) / get_val(var_stack[l()]))
                var_stack.pop()
            elif token == '%=':
                if type(var_stack[l() - 1]) is not tuple:
                    print "Error: Lvalue required"
                    exit(0)
                set_val(var_stack[l() - 1], get_val(var_stack[l() - 1]) % get_val(var_stack[l()]))
                var_stack.pop()
            elif token == '-=':
                if type(var_stack[l() - 1]) is not tuple:
                    print "Error: Lvalue required"
                    exit(0)
                set_val(var_stack[l() - 1], get_val(var_stack[l() - 1]) - get_val(var_stack[l()]))
                var_stack.pop()
            elif token == '+=':
                if type(var_stack[l() - 1]) is not tuple:
                    print "Error: Lvalue required"
                    exit(0)
                set_val(var_stack[l() - 1], get_val(var_stack[l() - 1]) + get_val(var_stack[l()]))
                var_stack.pop()
            elif token == ',':
                var_stack[l() - 1] = var_stack[l()]
                var_stack.pop()
            elif token == '>':
                var_stack[l() - 1] = (1 if get_val(var_stack[l() - 1]) > get_val(var_stack[l()]) else 0)
                var_stack.pop()
            elif token == '|':
                var_stack[l() - 1] = get_val(var_stack[l() - 1]) | get_val(var_stack[l()])
                var_stack.pop()
            elif token == '^':
                var_stack[l() - 1] = get_val(var_stack[l() - 1]) ^ get_val(var_stack[l()])
                var_stack.pop()
            elif token == '!':
                var_stack[l()] = (0 if get_val(var_stack[l()]) else 1)
            elif token == '%':
                var_stack[l() - 1] = get_val(var_stack[l() - 1]) % get_val(var_stack[l()])
                var_stack.pop()
            elif token == '&':
                var_stack[l() - 1] = get_val(var_stack[l() - 1]) & get_val(var_stack[l()])
                var_stack.pop()
            elif token == '+':
                var_stack[l() - 1] = get_val(var_stack[l() - 1]) + get_val(var_stack[l()])
                var_stack.pop()
            elif token == '*':
                var_stack[l() - 1] = get_val(var_stack[l() - 1]) * get_val(var_stack[l()])
                var_stack.pop()
            elif token == '-':
                var_stack[l() - 1] = get_val(var_stack[l() - 1]) - get_val(var_stack[l()])
                var_stack.pop()
            elif token == '/':
                if get_val(var_stack[l()]) == 0:
                    print "Division by 0 not permitted"
                    exit(0)
                var_stack[l() - 1] = get_val(var_stack[l() - 1]) / get_val(var_stack[l()])
                var_stack.pop()
            elif token == '#':
                var_stack[l()] = var_stack[l()]
            elif token == '_':
                var_stack[l()] = 0 - get_val(var_stack[l()])
            elif token == '=':
                if type(var_stack[l() - 1]) is not tuple:
                    print "Error: Lvalue required", type(var_stack[l() - 1])
                    exit(0)
                set_val(var_stack[l() - 1], get_val(var_stack[l()]))
                var_stack.pop()
            elif token == '<':
                var_stack[l() - 1] = (1 if get_val(var_stack[l() - 1]) < get_val(var_stack[l()]) else 0)
                var_stack.pop()
            elif token == '~':
                var_stack[l()] = ~get_val(var_stack[l()])
    r = get_val(var_stack.pop())
    return r
