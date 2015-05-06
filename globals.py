global var_table
global inp
import weave
inp = ''
var_table = {}
mem_space = {}

curr_mem = 1000000000


priority = {
    '->': 100, '++': 100, '--': 100,
    '+++': 91, '---': 91, '#': 91, '_': 91, '!': 91, '~': 91, '#type#': 91, '`*`': 91, '`&`': 91,
    '*': 80, '/': 80, '%': 80,
    '+': 78, '-': 78,
    '>>': 76, '<<': 76,
    '<=': 70, '>=': 70, '>': 70, '<': 70,
    '==': 66, '!=': 66,
    '&': 58, '^': 56, '|': 54, '&&': 52, '||': 50,
    '? :': 45,
    '=': 41, '+=': 41, '-=': 41, '*=': 41, '/=': 41,
    '%=': 41, '&=': 41, '^=': 41, '|=': 41,
    '>>=': 41, '<<=': 41,
    ',': 10
}

ops = (
    '#type#', '`*`', '`&`', '---', '? :', '+++', '<<=', '>>=', '*=', '|=', '>=', '>>', '==', '<<',
    '<=', '&=', '!=', '&&', '||', '^=', '++', '--', '/=', '%=', '-=', '->',
    '+=', ',', '>', '|', '^', '!', '%', '&', '+', '#', '_', '*', '-', '/', '=',
    '<', '~', '(', ')'
)

bin_ops = (
    '<<=', '>>=', '*=', '|=', '>=', '>>', '==', '<<', '<=', '&=',
    '!=', '&&', '||', '^=', '/=', '%=', '-=', '->', '+=', ',', '>',
    '|', '^', '%', '&', '+', '*', '-', '/', '=', '<'
)

unary_ops = {
    '+': '#', '-': '_', '*': '`*`', '&': '`&`'
}

size_of = {}

data_types = [
    'long long int', 'long int', 'long double', 'long long', 'char', 'int', 'long', 'float', 'double',
]

type_range = {}

functions = {}


def setup():
    code = r"""
    py::tuple res(9);
    res[0] = (int)sizeof(long long int);
    res[1] = (int)sizeof(long int);
    res[2] = (int)sizeof(long double);
    res[3] = (int)sizeof(long long);
    res[4] = (int)sizeof(char);
    res[5] = (int)sizeof(int);
    res[6] = (int)sizeof(long);
    res[7] = (int)sizeof(float);
    res[8] = (int)sizeof(double);
    return_val = res;
    """
    result = weave.inline(code, [])
    i = 0
    for types in data_types:
        size_of[types] = result[i]
        i += 1

    for types in ['char', 'int', 'long', 'long long', 'long long int']:
        temp = 1 << ((8 * size_of[types])-1)
        type_range[types] = (-temp, temp-1)


def in_var_table(var, scope):
    if type(scope) is str:
        scope = scope.split(' ')
    else:
        scope = scope[:]
    while len(scope) > 0:
        if (var, " ".join(scope)) in var_table:
            return var, " ".join(scope)
        scope.pop()
    return 0
