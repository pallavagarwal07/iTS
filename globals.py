global var_table
global inp
import weave
inp = ''
var_table = {}

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
    'long long int', 'long int', 'long double', 'long long', 'char', 'int', 'long', 'float', 'double', 'pointer'
]

type_range = {}

functions = {}


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


def in_var_table(var, scope):
    if type(scope) is str:
        scope = scope.split(' ')
    else:
        scope = scope[:]
    while len(scope) > 0:
        for v in var_table:
            if v[0] == var and v[1] == ' '.join(scope):
                return v
        scope.pop()
    return 0


def find_by_mem(mem):
    for v in var_table:
        if v[2] == mem:
            return v
    return 0


def toplevelsplit(var_str, delimiter):
    illegal_delimiters = ['(', ')' , '{', '}', '[', ']', '"', "'"]
    if delimiter in illegal_delimiters:
        print "Sorry, that delimiter is not allowed"
        exit(0)
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
                dbl_q = 0
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
    illegal_delimiters = ['(', ')' , '{', '}', '[', ']', '"', "'"]
    if orig in illegal_delimiters:
        print "Sorry, that replacement is not allowed"
        exit(0)
    cur_tk = []
    paren = 0
    sq_brace = 0
    curly_brace = 0
    dbl_q = 0
    sing_q = 0
    i = 0
    while i < len(var_str):
        ch = var_str[i]
        if ch not in illegal_delimiters:
            if paren or sq_brace or curly_brace or dbl_q or sing_q:
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
                dbl_q = 0
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
        i += 1
    return "".join(cur_tk)


