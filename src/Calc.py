import re

import Globals
from Functions import pass_to_func
from Globals import is_num, print1, print2, print3
from Vars import get_val, set_val, get_type
import Runtime
import Exceptions
import FakeMath

# Differentate between postfix and prefix increment operators.
def pre_post_handle(tokens):
    for i, tk in enumerate(tokens):
        if tk == '--':
            if i < len(tokens)-1 and tokens[i+1] not in Globals.ops:
                tokens[i] = '---'
        if tk == '++':
            if i < len(tokens)-1 and tokens[i+1] not in Globals.ops:
                tokens[i] = '+++'
    return tokens


# Separate out the tokens from an expression. i.e something like
# '5 + 4' would become ['5', '+', '4']
def sep(expr):
    print(expr)
    i, token, sep_tokens = 0, [], []

    while i < len(expr) and expr[i] != ';' :

        while i < len(expr) and expr[i] == ' ' :
            if token:
                sep_tokens.append(''.join(token))
                token = []
            i += 1

        checkOps = Globals.startDict

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
                    elif ex == '\"':
                        assert token == []
                        j = i + 1
                        expression = ['\"']
                        while expr[j] != '\"' or expr[j-1] == '\\':
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

    print("Returning", sep_tokens)
    return sep_tokens


# Convert operators like '+' which have overloaded binary and unary
# functions into differentiated unary counterparts, '`+`' for example.
def unary_handle(separated_tokens):
    flag = 1
    for i, token in enumerate(separated_tokens):

        if token in Globals.unary_ops and flag:
            separated_tokens[i] = Globals.unary_ops[token]
            continue

        if token in Globals.bin_ops or token == '(':
            flag = 1
            continue
        flag = 0

    return separated_tokens


# Add token to stack, taking extra care of && and || shortcircuiting
# operators. (Using &0 , counter substitution). Also appends type
# information wherever known.
def add(arr, token, ctr, scope):
    if type(token) is tuple:
        arr.append(token)
    else:
        if token == '||' or token == '&&':
            arr.append((token, ctr))
        elif token in Globals.ops + ('&0', '|1'):
            arr.append((token,))
        else:
            arr.append((token, get_type(token, scope)))


# Convert separated token list to postfix token list.
# Example: ['4', '+', '5'] to ['4', '5', '+']
def to_postfix(tokens, scope):
    stack, postfix, ctr, i = [], [], 0, 0

    while i < len(tokens):
        tk = tokens[i]
        if tk in Globals.ops:
            if tk == '(':
                add(stack, tk, ctr, scope)

            elif tk == ')':
                tmptypes = []
                if stack[-1][0] == '#type#':
                    while stack[-1][0] != '(':
                        tmptypes.append(stack.pop())
                    stack.pop()
                    tmptypes.reverse()
                    add(stack, ('#type#', " ".join(k[1] for k in tmptypes)), ctr, scope)
                else:
                    while stack[-1][0] != '(':
                        add(postfix, stack.pop(), ctr, scope)
                    stack.pop()
            elif len(stack) == 0 or stack[-1][0] == '(':
                add(stack, tk, ctr, scope)

            else:
                if Globals.priority[tk] < Globals.priority[stack[-1][0]]:
                    add(postfix, stack.pop(), ctr, scope)
                    continue

                if Globals.priority[tk] > Globals.priority[stack[-1][0]]:
                    add(stack, tk, ctr, scope)

                elif Globals.priority[tk] == Globals.priority[stack[-1][0]]:
                    if Globals.priority[tk] % 2 == 0:
                        add(postfix, stack.pop(), ctr, scope)
                        add(stack, tk, ctr, scope)
                    else:
                        add(stack, tk, ctr, scope)

            if tk == '&&':
                add(postfix, ('&0', ctr), ctr, scope)
                ctr += 1
            elif tk == '||':
                add(postfix, ('|1', ctr), ctr, scope)
                ctr += 1
        else:
            tag = 0
            for types in Globals.data_types:
                if tk.startswith(types):
                    add(stack, ('#type#', tk), ctr, scope)
                    tag = 1
                    break
            if tag == 0:
                add(postfix, tk, ctr, scope)
        i += 1
    while len(stack) > 0:
        add(postfix, stack.pop(), ctr, scope)
    return postfix



# Return the type with highest priority in coersion.
# Eg. Lf>lf>f>lld>ld>d etc.
def max_type(t1, t2='number', t3='number'):

    p_t = Globals.priority_type

    if(p_t[t1] >= p_t[t2] and p_t[t1] >= p_t[t3]):
        return t1

    elif(p_t[t2] >= p_t[t1] and p_t[t2] >= p_t[t3]):
        return t2

    elif(p_t[t3] >= p_t[t1] and p_t[t3] >= p_t[t2]):
        return t3


# Debugging only function. Slows down code considerably.
def caller_name():
    import inspect
    frame=inspect.currentframe()
    frame=frame.f_back.f_back
    code=frame.f_code
    return code.co_filename




# Backbone function of the whole project. Evaluates any
# expression, assigns variables, looks up memory addresses,
# everything. Can get input like '5+(a=4)+(a==4)?1:2'.

def calculate(expr, scope, vartable=Globals.var_table):

    if re.match(r'^(?s)\s*$', expr):
        return 0
    # If string has nothing, return 0. *TODO: Fix this "tape"

    if re.match(r'^(?s)\s*{\s*', expr):
        return expr
    # Not sure what this did. *TODO: Ask Kapila

    separated_tokens = sep(expr.strip())
    # Separate out all tokens

    separated_tokens = unary_handle(separated_tokens)
    # Fix unary operators like +, - etc.

    separated_tokens = pre_post_handle(separated_tokens)
    # Replace pre increment ++ and --
    postfix = to_postfix(separated_tokens, scope)
    # Convert to postfix

    stack, var_stack = [], []
    l = lambda: len(var_stack) - 1
    idx = 0
    for i, tk in enumerate(postfix):
        token = tk[0]
        if idx and postfix[i-1] != idx:
            continue
        idx = 0
        if token not in Globals.ops + ('&0', '|1'):
            var_stack.append(tk)
        else:
            if token in Globals.bin_ops:
                t1 = var_stack[l()][1]
                var_stack[l()] = var_stack[l()][0]
                t2 = var_stack[l()-1][1]
                var_stack[l()-1] = var_stack[l()-1][0]
            elif token in Globals.un_ops + ('&0', '|1'):
                t1 = var_stack[l()][1]
                var_stack[l()] = var_stack[l()][0]
            elif token == '?':
                t1 = var_stack[l()][1]
                var_stack[l()] = var_stack[l()][0]
                t2 = var_stack[l()-1][1]
                var_stack[l()-1] = var_stack[l()-1][0]
                t3 = var_stack[l()-2][1]
                var_stack[l()-2] = var_stack[l()-2][0]
            if token == '---':
                key = Runtime.get_key(var_stack[l()], scope)
                val = get_val(key, scope) - 1
                set_val(key, val, scope)
                var_stack[l()] = (val, max_type(t1))
            elif token == '+++':
                key = Runtime.get_key(var_stack[l()], scope)
                val = get_val(key, scope) + 1
                set_val(key, val, scope)
                var_stack[l()] = (val, max_type(t1))
            elif token == '`*`':
                var_stack[l()] = ((get_val(var_stack[l()], scope), ), get_type(var_stack[l()], scope)) # Do not remove the comma. It forces formation of a tuple
            elif token == '`&`':
                key = Runtime.get_key(var_stack[l()], scope)
                if type(key) is not tuple:
                    raise Exceptions.any_user_error("Something Wrong in the interpreter. Bug report filed.")
                elif len(key) == 1:
                    mem = key[0]
                else:
                    mem = vartable[key][3]
                var_stack[l()] = (mem, 'number')
            elif token == '`+`':
                var_stack[l()] = (var_stack[l()], max_type(t1))
            elif token == '`-`':
                var_stack[l()] = (0 - get_val(var_stack[l()], scope), max_type(t1))
            elif token == '<<=':
                key = Runtime.get_key(var_stack[l()-1], scope)
                set_val(key, get_val(key, scope) << get_val(var_stack[l()], scope), scope)
                var_stack[l()-1] = (get_val(key, scope), max_type(t2))
                var_stack.pop()
            elif token == '>>=':
                key = Runtime.get_key(var_stack[l()-1], scope)
                set_val(key, get_val(key, scope) >> get_val(var_stack[l()], scope), scope)
                var_stack[l()-1] = (get_val(key, scope), max_type(t2))
                var_stack.pop()
            elif token == '|1':
                if get_val(var_stack[l()], scope):
                    var_stack[l()] = (1, 'number')
                    idx = ('||', tk[1])
                else:
                    var_stack[l()] = (get_val(var_stack[l()], scope), max_type(t1))
            elif token == '&0':
                if not get_val(var_stack[l()], scope):
                    var_stack[l()] = (0, 'number')
                    idx = ('&&', tk[1])
                else:
                    var_stack[l()] = (get_val(var_stack[l()], scope), max_type(t1))
            elif token == '*=':
                key = Runtime.get_key(var_stack[l()-1], scope)
                val = get_val(key, scope) * get_val(var_stack[l()], scope)
                set_val(key, val, scope)
                var_stack[l()-1] = (val, max_type(t2))
                var_stack.pop()
            elif token == '|=':
                key = Runtime.get_key(var_stack[l()-1], scope)
                val = get_val(key, scope) | get_val(var_stack[l()], scope)
                set_val(key, val, scope)
                var_stack[l()-1] = (val, max_type(t2))
                var_stack.pop()
            elif token == '>=':
                var_stack[l() - 1] = ((1, 'number') if get_val(var_stack[l() - 1], scope) >= get_val(var_stack[l()], scope) else (0, 'number'))
                var_stack.pop()
            elif token == '>>':
                var_stack[l() - 1] = (get_val(var_stack[l() - 1], scope) >> get_val(var_stack[l()], scope), max_type(t1, t2))
                var_stack.pop()
            elif token == '==':
                var_stack[l() - 1] = ((1, 'number') if (get_val(var_stack[l() - 1], scope) == get_val(var_stack[l()], scope)) else (0, 'number'))
                var_stack.pop()
            elif token == '<<':
                var_stack[l() - 1] = (get_val(var_stack[l() - 1], scope) << get_val(var_stack[l()], scope), max_type(t1, t2))
                var_stack.pop()
            elif token == '<=':
                var_stack[l() - 1] = ((1, 'number') if get_val(var_stack[l() - 1], scope) <= get_val(var_stack[l()], scope) else (0, 'number'))
                var_stack.pop()
            elif token == '&=':
                key = Runtime.get_key(var_stack[l()-1], scope)
                val = get_val(key, scope) & get_val(var_stack[l()], scope)
                set_val(key, val, scope)
                var_stack[l()-1] = (val, max_type(t2))
                var_stack.pop()
            elif token == '!=':
                var_stack[l() - 1] = ((1, 'number') if get_val(var_stack[l() - 1], scope) != get_val(var_stack[l()], scope) else (0, 'number'))
                var_stack.pop()
            elif token == '&&':
                var_stack[l() - 1] = ((1, 'number') if get_val(var_stack[l() - 1], scope) and get_val(var_stack[l()], scope) else (0, 'number'))
                var_stack.pop()
            elif token == '||':
                var_stack[l() - 1] = ((1, 'number') if get_val(var_stack[l() - 1], scope) or get_val(var_stack[l()], scope) else (0, 'number'))
                var_stack.pop()
            elif token == '^=':
                key = Runtime.get_key(var_stack[l()-1], scope)
                val = get_val(key, scope) ^ get_val(var_stack[l()], scope)
                set_val(key, val, scope)
                var_stack[l()-1] = (val, max_type(t2))
                var_stack.pop()
            elif token == '++':
                key = Runtime.get_key(var_stack[l()], scope)
                val = get_val(key, scope) + 1
                set_val(key, val, scope)
                var_stack[l()] = (val - 1, max_type(t1))
            elif token == '--':
                key = Runtime.get_key(var_stack[l()], scope)
                val = get_val(key, scope) - 1
                set_val(key, val, scope)
                var_stack[l()] = (val + 1, max_type(t1))
            elif token == '/=':
                key = Runtime.get_key(var_stack[l()-1], scope)
                if get_val(var_stack[l()], scope) is 0:
                    raise Exceptions.any_user_error("Division by 0 not allowed!")

                val = get_val(key, scope) / get_val(var_stack[l()], scope)
                max_t = max_type(t2)
                if max_t in "number long long int":
                    val = int(val)

                set_val(key, val, scope)
                var_stack[l()-1] = (val, max_t)
                var_stack.pop()
            elif token == '%=':
                if t1 in ['float', 'double', 'long double', 'longdouble'] or t2 in ['float', 'double', 'long double', 'longdouble']:
                    raise Exceptions.any_user_error("Modulo operation not allowed with floating point numbers.")
                key = Runtime.get_key(var_stack[l()-1], scope)
                if get_val(var_stack[l()], scope) is 0:
                    raise Exceptions.any_user_error("Modulo by 0 not allowed!")
                val = get_val(key, scope) % get_val(var_stack[l()], scope)
                set_val(key, val, scope)
                var_stack[l()-1] = (val, max_type(t2))
                var_stack.pop()
            elif token == '-=':
                key = Runtime.get_key(var_stack[l()-1], scope)
                val = get_val(key, scope) - get_val(var_stack[l()], scope)
                set_val(key, val, scope)
                var_stack[l()-1] = (val, max_type(t2))
                var_stack.pop()
            elif token == '+=':
                key = Runtime.get_key(var_stack[l()-1], scope)
                val = get_val(key, scope) + get_val(var_stack[l()], scope)
                set_val(key, val, scope)
                var_stack[l()-1] = (val, max_type(t2))
                var_stack.pop()
            elif token == ',':
                var_stack[l() - 1] = (var_stack[l()], max_type(t1, t2))
                var_stack.pop()
            elif token == '>':
                var_stack[l() - 1] = ((1, 'number') if get_val(var_stack[l() - 1], scope) > get_val(var_stack[l()], scope) else (0, 'number'))
                var_stack.pop()
            elif token == '|':
                var_stack[l() - 1] = (get_val(var_stack[l() - 1], scope) | get_val(var_stack[l()], scope), max_type(t1, t2))
                var_stack.pop()
            elif token == '^':
                var_stack[l() - 1] = (get_val(var_stack[l() - 1], scope) ^ get_val(var_stack[l()], scope), max_type(t1, t2))
                var_stack.pop()
            elif token == '!':
                var_stack[l()] = ((0, max_type(t1)) if get_val(var_stack[l()], scope) else (1, max_type(t1)))
            elif token == '%':
                if get_val(var_stack[l()], scope) == 0:
                    raise Exceptions.any_user_error("Modulo by 0 not allowed!")
                var_stack[l() - 1] = (get_val(var_stack[l() - 1], scope) % get_val(var_stack[l()], scope), max_type(t1, t2))
                var_stack.pop()
            elif token == '&':
                var_stack[l() - 1] = (get_val(var_stack[l() - 1], scope) & get_val(var_stack[l()], scope), max_type(t1, t2))
                var_stack.pop()
            elif token == '+':
                var_stack[l() - 1] = (get_val(var_stack[l() - 1], scope) + get_val(var_stack[l()], scope), max_type(t1, t2))
                var_stack.pop()
            elif token == '*':
                var_stack[l() - 1] = (get_val(var_stack[l() - 1], scope) * get_val(var_stack[l()], scope), max_type(t1, t2))
                var_stack.pop()
            elif token == '-':
                var_stack[l() - 1] = (get_val(var_stack[l() - 1], scope) - get_val(var_stack[l()], scope), max_type(t1, t2))
                var_stack.pop()
            elif token == '/':
                if get_val(var_stack[l()], scope) == 0:
                    raise Exceptions.any_user_error("Division by 0 not allowed!")
                v1 = get_val(var_stack[l() - 1], scope)
                v2 = get_val(var_stack[l()], scope)
                var_stack[l() - 1] = (v1/v2, max_type(t1, t2))
                if var_stack[l()-1][1] in "number long long int":
                    var_stack[l()-1] = (int(var_stack[l()-1][0]), var_stack[l()-1][1])
                var_stack.pop()
            elif token == '=':
                key = Runtime.get_key(var_stack[l()-1], scope)
                val = get_val(var_stack[l()], scope)
                set_val(key, val, scope)
                var_stack[l()-1] = (val, max_type(t1))
                var_stack.pop()
            elif token == '<':
                var_stack[l() - 1] = ((1, 'number') if get_val(var_stack[l() - 1], scope) < get_val(var_stack[l()], scope) else (0, 'number'))
                var_stack.pop()
            elif token == '~':
                var_stack[l()] = (~get_val(var_stack[l()], scope), max_type(t1))
            elif token == ':':
                assert postfix[i+1][0] == '?'
            elif token == '?':
                assert postfix[i-1][0] == ':'
                if get_val(var_stack[l()-2], scope):
                    var_stack[l()-2] = (get_val(var_stack[l()-1], scope), max_type(t2))
                else:
                    var_stack[l()-2] = (get_val(var_stack[l()], scope), max_type(t1))
                var_stack.pop() # pop twice
                var_stack.pop()

            elif token == "#type#":
                new_type = tk[1]
                if new_type == 'longlong':
                    new_type = 'long long'
                elif new_type == 'longint':
                    new_type = 'long int'
                elif new_type == 'longlongint':
                    new_type = 'long long int'
                elif new_type == 'longdouble':
                    new_type = 'long double'
                if new_type in ['float', 'double', 'long double']:
                    if type(var_stack[l()]) is 'str':
                        raise Exceptions.any_user_error("User trying to convert", get_val(var_stack[l()], scope),"to float.")
                    else:
                        var_stack[l()] =  (float(get_val(var_stack[l()], scope)), new_type)
                elif new_type in ['int', 'long', 'long int', 'long long int', 'long long']:
                    if type(var_stack[l()]) is 'char':
                        var_stack[l()] =  (ord(get_val(var_stack[l()], scope)), new_type)
                    else:
                        var_stack[l()] = (int(get_val(var_stack[l()], scope)), new_type)
                elif new_type is 'char':
                    if type(var_stack[l()]) in ['float', 'double', 'long double']:
                        raise Exceptions.any_user_error("User trying to convert", get_val(var_stack[l()], scope) ,"to string.")
                    else:
                        var_stack[l()] = (chr(get_val(var_stack[l()], scope)), new_type)
        temp = var_stack[l()]
        if temp[1] not in ['number', 'void']:
            type_check = temp[1]
            m1 = Globals.type_range[temp[1]][0]
            m2 = Globals.type_range[temp[1]][1]
            if type(temp[0]) is int:
                temp = temp[0]
            else:
                temp = 0
            if not (temp == '' or temp is None or (m1 <= temp and temp <= m2)):
                raise Exceptions.any_user_error("Value", temp, "out of bounds of the type", type_check, "which can store values from", m1, "to", m2,".")
    ret = var_stack.pop()
    if var_stack:
        raise Exceptions.any_user_error("I don't think the expression in current line makes any sense.")
    r = get_val(ret[0], scope)
    Globals.calc_type = ret[1]
    return r
