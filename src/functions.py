from globals import is_num, print1, print2, print3, toplevelsplit
import fake_default
import Exceptions
import fake_math
import globals
import re

func = {
        'default': ['sizeof', 'malloc'],

        'math': ['sqrt', 'pow', 'cbrt', 'hypot', 'ceil', 'floor',
            'fmod', 'fabs', 'abs', 'round', 'exp', 'frexp', 'ldexp', 'log', 'log10',
            'log2', 'modf', 'exp2', 'expm1', 'sin', 'asin', 'sinh', 'asinh', 'cos',
            'acos', 'cosh', 'acosh', 'tan', 'atan', 'tanh', 'atanh', 'atan2'],

        'string': ['memchr', 'memcmp', 'memcpy', 'memmove', 'memset', 'strcat',
            'strcat', 'strncat', 'strchr', 'strcmp', 'strncmp', 'strcoll', 'strcpy',
            'strncpy', 'strcspn', 'strerror', 'strlen', 'strpbrk', 'strrchr', 'strspn',
            'strstr', 'strtok', 'strxfrm'],

        'stdio': ['printf', 'scanf', 'getchar', 'gets', 'sprintf', 'sscanf',
            'puts', 'putchar'],

        'user': globals.functions
        }
unique_id = 1


def eval_user_function(name, params, scope):
    import Runtime
    import Calc
    global unique_id

    target = globals.functions[name]

    if len(params) != len(target[3]):
        raise Exceptions.any_user_error("Error! Incorrect number of parameters.")

    if target[2] == '':
        raise Exceptions.any_user_error("Error! Function declaration not found.")

    params = [Calc.calculate(str(k), scope) for k in params]

    # we need a unique scope for every instance of function
    hash = 'inst'+str(unique_id)
    unique_id += 1

    # GUI string
    globals.gui += "\ncreate_scope(\'global\',\'"+"global-"+name+"\');"
    globals.gui += "\ncreate_scope(\'global-"+name+"\',\'"+\
            "global-"+name+"-"+hash+"\');"


    if target[3]:
        for i, d in enumerate(target[1]):
            Runtime.decl(d[1], params[i], d[0], "global " + name + " " + hash, None)

    return Runtime.execute(globals.functions[name][2], \
            "global "+name+" "+hash)


def pass_to_func(detail, scope):
    # detail is like ('pow', 'a, b')
    name = detail[0]
    params = tuple(a.strip() for a in toplevelsplit(detail[1], ','))
    length = len(params) if detail[1].strip() != '' else 0
    if length == 0:
        params = []

    for lib in func:
        arr = func[lib]
        if name in arr:
            if lib == 'default':
                return fake_default.invoke(name, params, scope)
            if lib == 'math':
                return fake_math.invoke(name, params, scope)
            if lib == 'string':
                return fake_string.invoke(name, params, scope)
            if lib == 'stdio':
                return fake_stdio.invoke(name, params, scope)
            if lib == 'user':
                return eval_user_function(name, params, scope)

    raise Exceptions.any_user_error("Error! Undeclared Function", name)



