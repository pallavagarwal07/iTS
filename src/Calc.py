import globals
import re
from globals import is_num, print1, print2, print3
from Vars import get_val, set_val
import random
import Runtime
import Exceptions


def pass_to_func(detail, scope):
    name = detail[0]
    l = len(globals.toplevelsplit(detail[1], ','))
    if(detail[1].strip() == ''):
        l = 0
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
        raise Exceptions.unimplemented_error("Request for", size , "Malloc hasn't been handled yet")
    if name not in globals.functions:
        raise Exceptions.any_user_error("Error!! Undeclared Function", name)
    if len(globals.functions[name][3]) != l:
        print1(globals.functions[name][3], l, "HERE")
        raise Exceptions.any_user_error("Error!! Incorrect no. of parameters")
    if globals.functions[name][2] == '':
        raise Exceptions.any_user_error("Error!! The function was declared, but never defined.")
    detail = globals.toplevelsplit(detail[1], ',')
    detail = [calculate(str(k).strip(), scope) for k in detail]

    RandomHash = hex(random.getrandbits(64))[2:-1]
    import Runtime
    globals.gui += "\ncreate_scope(\'global\',\'"+"global-"+name+"\');"
    globals.gui += "\ncreate_scope(\'global-"+name+"\',\'"+"global-"+name+"-"+RandomHash+"\');"
    if l:
        for i, declarations in enumerate(globals.functions[name][1]):
            Runtime.decl(declarations[1], detail[i], declarations[0], "global " + name + " " + RandomHash)
    return Runtime.execute(globals.functions[name][2], "global " + name + " " + RandomHash)


def pre_post_handle(tokens):
    for i, tk in enumerate(tokens):
        if tk == '--':
            if i < len(tokens)-1 and tokens[i+1] not in globals.ops:
                tokens[i] = '---'
        if tk == '++':
            if i < len(tokens)-1 and tokens[i+1] not in globals.ops:
                tokens[i] = '+++'
    return tokens


def sep(expr):
    i = 0
    token = []
    sep_tokens = []

    while i < len(expr) and expr[i] != ';':
        while i < len(expr) and expr[i] == ' ':
            #if token != []:
                #sep_tokens.append(''.join(token))
                #token = []
            i += 1

        checkOps = globals.startDict

        if expr[i] in checkOps:
            for ex in checkOps[expr[i]]:
                if expr.startswith(ex, i):
                    if ex != '(' and ex != '[':
                        if token != []:
                            sep_tokens.append(''.join(token))
                        token = []
                    if ex == '(':
                        if token == []:
                            sep_tokens.append(ex)
                        else:
                            j = i + 1
                            expression = ['(']
                            bracks = 1
                            while bracks > 0:
                                expression.append(expr[j])
                                if expr[j] == '(':
                                    bracks += 1
                                if expr[j] == ')':
                                    bracks -= 1
                                j += 1
                            i += len(expression) - 1
                            token += expression
                    elif ex == '[':
                        j = i + 1
                        expression = ['[']
                        bracks = 1
                        while bracks > 0:
                            expression += expr[j]
                            if expr[j] == '[' and expr[j-1]!="'":
                                bracks += 1;
                            if expr[j] == ']' and expr[j-1]!="'":
                                bracks -= 1;
                            j += 1
                        i += len(expression) - 1
                        token += expression
                    elif ex == '\'':
                        assert token == []
                        j = i + 1
                        expression = ['\'']
                        while expr[j] != "'" or expr[j-1] == '\\':
                            expression += expr[j]
                            j += 1
                        expression += expr[j]
                        i += len(expression) - 1
                        token += expression
                    else:
                        sep_tokens.append(ex)
                    i += len(ex) - 1
                    break
        else:
            token.append(expr[i])
        i += 1
    if token != []:
        sep_tokens.append(''.join(token))
    return sep_tokens


def unary_handle(separated_tokens):
    flag = 1
    for i, token in enumerate(separated_tokens):
        if token in globals.unary_ops and flag:
            separated_tokens[i] = globals.unary_ops[token]
            continue
        if token in globals.bin_ops or token == '(':
            flag = 1
            continue
        flag = 0
    return separated_tokens


def add(arr, token, ctr):
    if type(token) is tuple:
        arr.append(token)
    else:
        if token == '||' or token == '&&':
            arr.append((token, ctr))
        else:
            arr.append((token,))


def to_postfix(tokens):
    stack = []
    postfix = []
    ctr = 0
    i = 0
    while i < len(tokens):
        tk = tokens[i]
        if tk in globals.ops:
            if tk == '(':
                add(stack, tk, ctr)
            elif tk == ')':
                while stack[-1][0] != '(':
                    add(postfix, stack.pop(), ctr)
                stack.pop()
            elif len(stack) == 0 or stack[-1][0] == '(':
                add(stack, tk, ctr)
            else:
                if globals.priority[tk] < globals.priority[stack[-1][0]]:
                    add(postfix, stack.pop(), ctr)
                    continue
                if globals.priority[tk] > globals.priority[stack[-1][0]]:
                    add(stack, tk, ctr)
                elif globals.priority[tk] == globals.priority[stack[-1][0]]:
                    if globals.priority[tk] % 2 == 0:
                        add(postfix, stack.pop(), ctr)
                        add(stack, tk, ctr)
                    else:
                        add(stack, tk, ctr)
            if tk == '&&':
                add(postfix, ('&0', ctr), ctr)
                ctr += 1
            elif tk == '||':
                add(postfix, ('|1', ctr), ctr)
                ctr += 1
        else:
            tag = 0
            for types in globals.data_types:
                if tk.startswith(types):
                    stack.pop()
                    add(stack, ('#type#', tk), ctr)
                    i += 1
                    tag = 1
            if tag == 0:
                add(postfix, tk, ctr)
        i += 1
    while len(stack) > 0:
        add(postfix, stack.pop(), ctr)
    return postfix


def calculate(expr, scope, vartable=globals.var_table):
    print2("calculate in Calc.py got:\n", expr, scope, "\nThat's all--")
    if re.match(r"^(?s)\s*$", expr):
        return 0
    # If string has nothing, return 0. This will be removed
    # later when uninitialised vars are handled
    if re.match(r"^(?s)\s*{\s*", expr):
        return expr
    separated_tokens = sep(expr) # Separate out all tokens
    print2(separated_tokens)
    separated_tokens = unary_handle(separated_tokens) # Fix unary operators
    print2(separated_tokens)
    separated_tokens = pre_post_handle(separated_tokens) # Replace pre increment ++ and --
    print2(separated_tokens)
    postfix = to_postfix(separated_tokens)
    print1("postfix")
    print1(postfix)
    stack = []
    for k in postfix:
        if 'Error' == is_num(k[0]):
            if k:
                stack.append(k)
        else:
            m = is_num(k[0])
            stack.append((m,))
    postfix = stack
    var_stack = []
    l = lambda: len(var_stack) - 1
    idx = 0
    for i, tk in enumerate(postfix):
        token = tk[0]
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
                    raise Exceptions.any_user_error("Error: Trying to assign value to a non-variable.")
                set_val(var_stack[l()], get_val(var_stack[l()]) - 1)
            elif token == '+++':
                if type(var_stack[l()]) is not tuple:
                    raise Exceptions.any_user_error("Error: Trying to assign value to a non-variable.")
                set_val(var_stack[l()], get_val(var_stack[l()]) + 1)
            elif token == '`*`':
                var_stack[l()] = (get_val(var_stack[l()]),) # Do not remove the comma. It forces formation of a tuple
            elif token == '`&`':
                var_stack[l()] = vartable[var_stack[l()]][3]
            elif token == '<<=':
                if type(var_stack[l() - 1]) is not tuple:
                    raise Exceptions.any_user_error("Error: Trying to assign value to a non-variable.")
                set_val(var_stack[l() - 1], get_val(var_stack[l() - 1]) << get_val(var_stack[l()]))
                var_stack.pop()
            elif token == '>>=':
                if type(var_stack[l() - 1]) is not tuple:
                    raise Exceptions.any_user_error("Error: Trying to assign value to a non-variable.")
                set_val(var_stack[l() - 1], get_val(var_stack[l() - 1]) >> get_val(var_stack[l()]))
                var_stack.pop()
            elif token == '|1':
                if get_val(var_stack[l()]):
                    var_stack[l()] = 1
                    idx = ('||', tk[1])
            elif token == '&0':
                if not get_val(var_stack[l()]):
                    var_stack[l()] = 0
                    idx = ('&&', tk[1])
            elif token == '*=':
                if type(var_stack[l() - 1]) is not tuple:
                    raise Exceptions.any_user_error("Error: Trying to assign value to a non-variable.")
                set_val(var_stack[l() - 1], get_val(var_stack[l() - 1]) * get_val(var_stack[l()]))
                var_stack.pop()
            elif token == '|=':
                if type(var_stack[l() - 1]) is not tuple:
                    raise Exceptions.any_user_error("Error: Trying to assign value to a non-variable.")
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
                    raise Exceptions.any_user_error("Error: Trying to assign value to a non-variable.")
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
                    raise Exceptions.any_user_error("Error: Trying to assign value to a non-variable.")
                set_val(var_stack[l() - 1], get_val(var_stack[l() - 1]) ^ get_val(var_stack[l()]))
                var_stack.pop()
            elif token == '++':
                if type(var_stack[l()]) is not tuple:
                    raise Exceptions.any_user_error("Error: Trying to assign value to a non-variable.")
                set_val(var_stack[l()], get_val(var_stack[l()]) + 1)
                var_stack[l()] =  get_val(var_stack[l()]) - 1
            elif token == '--':
                if type(var_stack[l()]) is not tuple:
                    raise Exceptions.any_user_error("Error: Trying to assign value to a non-variable.")
                set_val(var_stack[l()], get_val(var_stack[l()]) - 1)
                var_stack[l()] =  get_val(var_stack[l()]) + 1
            elif token == '/=':
                if type(var_stack[l() - 1]) is not tuple:
                    raise Exceptions.any_user_error("Error: Trying to assign value to a non-variable.")
                elif get_val(var_stack[l()]) == 0:
                    raise Exceptions.any_user_error("Error: Division by 0 not permitted.")
                set_val(var_stack[l() - 1], get_val(var_stack[l() - 1]) / get_val(var_stack[l()]))
                var_stack.pop()
            elif token == '%=':
                if type(var_stack[l() - 1]) is not tuple:
                    raise Exceptions.any_user_error("Error: Trying to assign value to a non-variable.")
                set_val(var_stack[l() - 1], get_val(var_stack[l() - 1]) % get_val(var_stack[l()]))
                var_stack.pop()
            elif token == '-=':
                if type(var_stack[l() - 1]) is not tuple:
                    raise Exceptions.any_user_error("Error: Trying to assign value to a non-variable.")
                set_val(var_stack[l() - 1], get_val(var_stack[l() - 1]) - get_val(var_stack[l()]))
                var_stack.pop()
            elif token == '+=':
                if type(var_stack[l() - 1]) is not tuple:
                    raise Exceptions.any_user_error("Error: Trying to assign value to a non-variable.")
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
                if type(var_stack[l() - 1]) is not tuple:
                    raise Exceptions.any_user_error("Error: Trying to assign value to a non-variable.")
                elif get_val(var_stack[l()]) == 0:
                    raise Exceptions.any_user_error("Error: Division by 0 not permitted.")
                var_stack[l() - 1] = get_val(var_stack[l() - 1]) / get_val(var_stack[l()])
                var_stack.pop()
            elif token == '#':
                var_stack[l()] = var_stack[l()]
            elif token == '_':
                var_stack[l()] = 0 - get_val(var_stack[l()])
            elif token == '=':
                if type(var_stack[l() - 1]) is not tuple:
                    raise Exceptions.any_user_error("Error: Trying to assign value to a non-variable.")
                set_val(var_stack[l() - 1], get_val(var_stack[l()]))
                var_stack.pop()
            elif token == '<':
                var_stack[l() - 1] = (1 if get_val(var_stack[l() - 1]) < get_val(var_stack[l()]) else 0)
                var_stack.pop()
            elif token == '~':
                var_stack[l()] = ~get_val(var_stack[l()])
            elif token == ':':
                assert postfix[i+1][0] == '?'
            elif token == '?':
                assert postfix[i-1][0] == ':'
                if get_val(var_stack[l()-2]):
                    var_stack[l()-2] = get_val(var_stack[l()-1])
                else:
                    var_stack[l()-2] = get_val(var_stack[l()])
                var_stack.pop() # pop twice
                var_stack.pop()

            elif token == "#type#":
                new_type = tk[1]
                if new_type in ['float', 'double', 'long double']:
                    if type(var_stack[l()]) is 'str':
                        raise Exceptions.any_user_error("Trying to convert string to float.")
                    else:
                        set_val(var_stack[l()], float(get_val(var_stack[l()])))
                elif new_type in ['int', 'long', 'long int', 'long long int', 'long long']:
                    if type(var_stack[l()]) is 'str':
                        set_val(var_stack[l()], ord(get_val(var_stack[l()])))
                    else:
                        set_val(var_stack[l()], int(get_val(var_stack[l()])))
                elif new_type is 'char':
                    if type(var_stack[l()]) in ['float', 'double', 'long double']:
                        raise Exceptions.any_user_error("Trying to convert float to string.")
                    else:
                        set_val(var_stack[l()], chr(get_val(var_stack[l()])))
    r = get_val(var_stack.pop())
    print2("calculate in Calc.py returned:\n", r, "\nThat's all--")
    return r
