from globals import print1, print2, print3
import globals
import Exceptions
import re
import sys
import Calc
import Vars


def get_input_value(val, cast):
    if cast in ['int', 'long', 'long int', 'long long', 'long long int']:
        return int(val)
    if cast in ['float', 'double', 'long double']:
        return float(val)
    if cast == 'char':
        assert len(val) == 1
        return ord(val)
    if cast == 'string':
        return val

def var_types(s):
    arr = []
    var_arr = []
    flag = 0
    for i, ch in enumerate(s):
        if flag > 0:
            flag -= 1
        elif ch in [' ', '\n', '\t', '\f']:
            arr.append(('whitespace', '\s*', 999999))
        elif ch == '%':
            if s[i+1] == '%':
                arr.append(('literal', re.escape(ch), 1, ch))
                flag = 1
            else:
                k = re.findall(r'^(%(\d*\.?\d*)d)', s[i:])
                if k:
                    arr.append(('int', '\s*([-+]?\d+)',
                        int(k[0][1]) if k[0][1] else 999999))
                    var_arr.append(arr[-1])
                    flag = len(k[0][0]) - 1
                    continue
                k = re.findall(r'^(%(\d*\.?\d*)f)', s[i:])
                if k:
                    arr.append(('float',
                        '\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)',
                        int(k[0][1]) if k[0][1] else 999999))
                    var_arr.append(arr[-1])
                    flag = len(k[0][0]) - 1
                    continue
                k = re.findall(r'^(%(\d*\.?\d*)ld)', s[i:])
                if k:
                    arr.append(('long', '\s*([-+]?\d+)',
                        int(k[0][1]) if k[0][1] else 999999))
                    var_arr.append(arr[-1])
                    flag = len(k[0][0]) - 1
                    continue
                k = re.findall(r'^(%(\d*\.?\d*)lf)', s[i:])
                if k:
                    arr.append(('double',
                        '\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)',
                        int(k[0][1]) if k[0][1] else 999999))
                    var_arr.append(arr[-1])
                    flag = len(k[0][0]) - 1
                    continue
                k = re.findall(r'^(%(\d*\.?\d*)lld)', s[i:])
                if k:
                    arr.append(('long long', '\s*([-+]?\d+)',
                        int(k[0][1]) if k[0][1] else 999999))
                    var_arr.append(arr[-1])
                    flag = len(k[0][0]) - 1
                    continue
                k = re.findall(r'^(%(\d*\.?\d*)Lf)', s[i:])
                if k:
                    arr.append(('long double',
                        '\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)',
                        int(k[0][1]) if k[0][1] else 999999))
                    var_arr.append(arr[-1])
                    flag = len(k[0][0]) - 1
                    continue
                k = re.findall(r'^(%(\d*\.?\d*)c)', s[i:])
                if k:
                    arr.append(('char', '[\n\r]*(.)', int(k[0][1])
                        if k[0][1] else 999999))
                    var_arr.append(arr[-1])
                    flag = len(k[0][0]) - 1
                    continue
                k = re.findall(r'^(%(\d*\.?\d*)s)', s[i:])
                if k:
                    arr.append(('string', '\s*(\S+)', int(k[0][1])
                        if k[0][1] else 999999))
                    var_arr.append(arr[-1])
                    flag = len(k[0][0]) - 1
                    continue
        else:
            arr.append(('literal', re.escape(ch), 1, ch))
    return var_arr, arr


def is_same(str1, str2):
    arr1 = ['long', 'long int']
    arr2 = ['long long', 'long long int']
    arr3 = ['string', 'char']
    if str1 in arr1 and str2 in arr1:
        return True
    if str1 in arr2 and str2 in arr2:
        return True
    if str1 in arr3 and str2 in arr3:
        return True
    if str1 == str2:
        return True


def extract(regex_arr, type_arr):
    values = []
    for tup in regex_arr:
        reg = '^' + tup[1]
        num = tup[2]
        k = re.findall(reg, globals.inp[:num])
        if not k:
            raise Exceptions.any_user_error("Incorrect Input (probably)")

        if tup not in type_arr:
            k = re.sub(reg, '', globals.inp[:num])
            globals.inp = k + globals.inp[num:]
        else:
            globals.inp = re.sub(reg, '', globals.inp[:num]) + globals.inp[num:]
            values.append(k[0])

    print2("INPUT EXTRACTED the following values: ", values)
    return values


def handle_input(statement, scope):
    # statement is something like scanf("%d %c\n%lld", &a, &b, &c)
    statement = statement.decode('string_escape')
    print2("STATEMENT TO INPUT: ", statement, "WITH SCOPE: ", scope)
    # sep = [('%d %c\n%lld', ' &a, &b,', ' &c')]
    sep = re.findall(r'(?s)scanf\s*\(\s*\"(.*)\"\s*,(.*,)*(.*)\)', statement)
    print2("sep: ", sep)

    if len(sep) == 0:
        return False
    elif len(sep) > 1:
        return Exceptions.any_user_error("I think you might be missing a semicolon")

    type_arr, regex_arr = var_types(sep[0][0])


    print2("Reached here in handle_input")
    variables = globals.toplevelsplit(sep[0][1], ',')
    variables = variables[:-1]
    variables.append(sep[0][2])
    # now, variables = ['&a', '&b', '&c']

    values = extract(regex_arr, type_arr)

    assert len(type_arr) == len(values)
    print2("type array: ", type_arr)
    if len(values) != len(variables):
        raise Exceptions.any_user_error("Incorrect number of \
                arguments or bug in my interpreter", values, variables)
    else:
        print2("variables: ", variables)
        for i in range(0, len(variables)):
            v = (Calc.calculate(variables[i], scope),)
            dst_type = globals.memory[v][0].type[0] \
                    if globals.memory[v][0].type[1] == 0 else 'pointer'
            src_type = type_arr[i][0]
            print1("Type: ", dst_type, src_type, "memory: ", v)
            if not is_same(dst_type, src_type):
                raise Exceptions.any_user_error("Variable Type not same as input!!")

            print2("memory: ", globals.memory[v])
            vals = get_input_value(values[i], src_type)
            print2("vals", vals)
            if src_type == 'string':
                for i in range(0, len(vals)):
                    print3(v, globals.memory[v][1])
                    Vars.set_val((v[0]+i*globals.memory[v][1],), ord(vals[i]))
                Vars.set_val((v[0]+len(vals)*globals.memory[v][1],), 0)
            else:
                Vars.set_val(v, vals)
    return True


def handle_output(line, scope):
    line = line.decode('string_escape')
    sep = re.findall(r'(?s)printf\s*\(\s*\"(.*)\"\s*(,.+)*\s*\)', line)
    # sep = [('Hello %d %lf', ', 45, 67')]


    if len(sep) == 0:
        return False
    if type(sep[0]) is str:
        sep = [[sep[0]]]

    type_arr, regex_arr = var_types(sep[0][0])

    if sep[0][1] == '':
        globals.out.write(format_string)
    else:
        format_vars = globals.toplevelsplit(sep[0][1][1:], ',')
        for i in range(0, len(format_vars)):
            if format_vars[i] != '':
                format_vars[i] = Calc.calculate(format_vars[i].strip(), scope, globals.var_table)
        format_string = re.sub(r'%(\d*\.?\d*)(lld|ld|d)', r'%\1d', format_string)
        format_string = re.sub(r'%(\d*\.?\d*)(Lf|lf|f)', r'%\1f', format_string)
        format_string = format_string % tuple(format_vars)
        globals.out.write(format_string)
    return True
