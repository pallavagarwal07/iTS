import weave

global var_table
global inp

inp = ''
gui = ""
var_table = {}
vLevel = 0

curr_mem = 1000000000

# priority of operators. Even values are (generally) binary operators and vice versa.
priority = {
    '->': 100, '++': 100, '--': 100,
    '+++': 91, '---': 91, '`+`': 91, '`-`': 91, '!': 91, '~': 91, '#type#': 91, '`*`': 91, '`&`': 91,
    '*': 80, '/': 80, '%': 80,
    '+': 78, '-': 78,
    '>>': 76, '<<': 76,
    '<=': 70, '>=': 70, '>': 70, '<': 70,
    '==': 66, '!=': 66,
    '&': 58, '^': 56, '|': 54, '&&': 52, '||': 50,
    '?':45, ':': 45,
    '=': 41, '+=': 41, '-=': 41, '*=': 41, '/=': 41,
    '%=': 41, '&=': 41, '^=': 41, '|=': 41,
    '>>=': 41, '<<=': 41,
    ',': 10
}

# Operators sorted in order of length. Do not change.
ops = (
    '#type#', '`*`', '`&`', '`-`', '`+`', '---', '? :', '+++', '<<=', '>>=', '*=', '|=', '>=', '>>', '==', '<<',
    '<=', '&=', '!=', '&&', '||', '^=', '++', '--', '/=', '%=', '-=', '->',
    '+=', ',', '>', '|', '^', '!', '%', '&', '+', '*', '-', '/', '=',
    '<', '~', '(', ')', '?', ':'
)

bin_ops = (
    '<<=', '>>=', '*=', '|=', '>=', '>>', '==', '<<', '<=', '&=',
    '!=', '&&', '||', '^=', '/=', '%=', '-=', '->', '+=', ',', '>',
    '|', '^', '%', '&', '+', '*', '-', '/', '=', '<'
)

unary_ops = {
    '+': '`+`', '-': '`-`', '*': '`*`', '&': '`&`'
}

size_of = {}
data_types = [
    'long long int', 'long int', 'long double', 'long long', 'char',
    'int', 'long', 'float', 'double', 'pointer'
]
type_range = {}
memory = {}
functions = {}
startDict = {
'!': ['!=', '!'], '#': ['#type#'], '%': ['%=', '%'], "'": ["'"],
'&': ['&=', '&&', '&'], ')': [')'], '(': ['('], '+': ['+++', '++', '+=', '+'],
'*': ['*=', '*'], '-': ['---', '--', '-=', '->', '-'], ',': [','], '/': ['/=', '/'],
'=': ['==', '='], '<': ['<<=', '<<', '<=', '<'],
'>': ['>>=', '>=', '>>', '>'], '[': ['['], '^': ['^=', '^'],
'`': ['`*`', '`&`', '`-`', '`+`'], '|': ['|=', '||', '|'], '~': ['~'], '?':['?'], ':':[':']
}

predefined_funcs = ['sqrt', 'pow', 'cbrt', 'hypot', 'ceil', 'floor',
 'fmod', 'fabs', 'abs', 'round', 'exp', 'frexp', 'ldexp', 'log', 'log10',
 'log2', 'modf', 'exp2', 'expm1', 'sin', 'asin', 'sinh', 'asinh', 'cos',
 'acos', 'cosh', 'acosh', 'tan', 'atan', 'tanh', 'atanh', 'atan2']


def type_string():
    ret = ''
    for types in data_types:
        if types is not 'pointer':
            ret += t + '|'
    ret = ret[:-1]
    ret = ret.replace(' ', r'\s+')
    return ret


# Run a c code to determine the sizeof() values
def setup():
    code = r"""
    py::tuple res(10);
    res[0] = (int)sizeof(long long int);
    res[1] = (int)sizeof(long int);
    res[2] = (int)sizeof(long double);
    res[3] = (int)sizeof(long long);
    res[4] = (int)sizeof(char);
    res[5] = (int)sizeof(int);
    res[6] = (int)sizeof(long);
    res[7] = (int)sizeof(float);
    res[8] = (int)sizeof(double);
    res[9] = (int)sizeof(int*);
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


# Get key tuple from variable name and scope
def in_var_table(var, scope):
    if type(scope) is list:
        scope = " ".join(scope)
    probables = []
    for v in var_table:
        if v[0] == var and v[1] == scope:
            return v
        elif v[0] == var and scope.startswith(v[1] + ' '):
            probables.append(v)
    if len(probables) == 0:
        return 0
    return max(probables, key=lambda v: len(v[1]))


# Get value of variable from memory only
def find_by_mem(mem):
    if mem in memory:
        return memory[mem].v


# Class to store all types of values of variables
class Value(object):
    def __init__(self, v=None):
        self.v = v
    def __str__(self):
        return "Value: "+str(self.v)
    def __repr__(self):
        return "Value: "+str(self.v)


def get_details(var):
    name = ''
    indices = []
    flag = 1
    first = 0
    bracks = 0
    for i, ch in enumerate(var):
        if flag and ch!='[':
            continue;
        if flag:
            name = var[:i]
            flag = not flag
            bracks += 1
            if bracks == 1:
                first = i
            continue
        if ch == ']':
            bracks -= 1
            if bracks == 0:
                indices.append(var[first+1:i])
            continue
        if ch == '[':
            bracks += 1
            if bracks == 1:
                first = i
            continue
    if flag:
        name = var[:i+1]
    assert bracks == 0
    return name, indices



def toplevelsplit(var_str, delimiter):
    illegal_delimiters = ['(', ')' , '{', '}', '[', ']', '"', "'"]
    if delimiter in illegal_delimiters:
        raise Exceptions.coding_bug("Sorry, that delimiter is not allowed")
    tokens = []
    cur_tk = []
    paren = 0
    sq_brace = 0
    curly_brace = 0
    dbl_q = 0
    sing_q = 0
    for i, ch in enumerate(var_str):
        if ch not in illegal_delimiters:
            if paren or sq_brace or curly_brace or dbl_q or sing_q:
                cur_tk.append(ch)
            elif ch == delimiter:
                tokens.append("".join(cur_tk))
                cur_tk = []
            else:
                cur_tk.append(ch)
        elif dbl_q:
            if ch=='"' and var_str[i-1]!='\\':
                dbl_q = 0
                cur_tk.append(ch)
            else:
                cur_tk.append(ch)
        elif sing_q:
            if ch=="'" and var_str[i-1]!='\\':
                sing_q = 0
                cur_tk.append(ch)
            else:
                cur_tk.append(ch)
        else:
            if ch == '(':
                paren += 1
            elif ch == ')':
                paren -= 1
            elif ch == '[':
                sq_brace += 1
            elif ch ==']':
                sq_brace -= 1
            elif ch == '{':
                curly_brace += 1
            elif ch == '}':
                curly_brace -= 1
            elif ch == '"':
                dbl_q = 1
            elif ch == "'":
                sing_q = 1
            cur_tk.append(ch)
    tokens.append("".join(cur_tk))
    return tokens


def toplevelreplace(var_str, orig, repl):
    illegal_delimiters = ['"', "'"]
    cur_tk = []
    dbl_q = 0
    sing_q = 0
    i = 0
    while i < len(var_str):
        ch = var_str[i]
        if ch not in illegal_delimiters:
            if dbl_q or sing_q:
                cur_tk.append(ch)
            elif var_str.startswith(orig, i):
                cur_tk.append(repl)
                i += (len(orig)-1)
            else:
                cur_tk.append(ch)
        elif dbl_q:
            if ch=='"' and var_str[i-1]!='\\':
                dbl_q = 0
                cur_tk.append(ch)
            else:
                cur_tk.append(ch)
        elif sing_q:
            if ch=="'" and var_str[i-1]!='\\':
                sing_q = 0
                cur_tk.append(ch)
            else:
                cur_tk.append(ch)
        else:
            if ch == '"':
                dbl_q = 1
            elif ch == "'":
                sing_q = 1
            cur_tk.append(ch)
        i += 1
    return "".join(cur_tk)


def print1(*args):
    if(vLevel):
        for arg in args:
            print arg,
        print ''


def print2(*args):
    if(vLevel>1):
        for arg in args:
            print arg,
        print ''


def print3(*args):
    if(vLevel>2):
        for arg in args:
            print arg,
        print ''


def is_num(s):
    try:
        float(s)
        return eval(str(s))
    except ValueError:
        return 'Error'
