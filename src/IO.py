import re

from Globals import print1, print2, print3
import Globals
import Exceptions
import Calc
import Vars
import Runtime


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
            arr.append(('whitespace', '\s*', '', ch))
        elif ch == '%':
            if s[i+1] == '%':
                arr.append(('literal', re.escape(ch), 1, ch))
                flag = 1
            else:
                k = re.findall(r'^(%(\d*\.?\d*)d)', s[i:])
                if k:
                    arr.append(('int', '\s*([-+]?\d+)',
                        eval(k[0][1]) if k[0][1] else ''))
                    var_arr.append(arr[-1])
                    flag = len(k[0][0]) - 1
                    continue
                k = re.findall(r'^(%(\d*\.?\d*)f)', s[i:])
                if k:
                    arr.append(('float',
                        '\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)',
                        eval(k[0][1]) if k[0][1] else ''))
                    var_arr.append(arr[-1])
                    flag = len(k[0][0]) - 1
                    continue
                k = re.findall(r'^(%(\d*\.?\d*)ld)', s[i:])
                if k:
                    arr.append(('long', '\s*([-+]?\d+)',
                        eval(k[0][1]) if k[0][1] else ''))
                    var_arr.append(arr[-1])
                    flag = len(k[0][0]) - 1
                    continue
                k = re.findall(r'^(%(\d*\.?\d*)lf)', s[i:])
                if k:
                    arr.append(('double',
                        '\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)',
                        eval(k[0][1]) if k[0][1] else ''))
                    var_arr.append(arr[-1])
                    flag = len(k[0][0]) - 1
                    continue
                k = re.findall(r'^(%(\d*\.?\d*)lld)', s[i:])
                if k:
                    arr.append(('long long', '\s*([-+]?\d+)',
                        eval(k[0][1]) if k[0][1] else ''))
                    var_arr.append(arr[-1])
                    flag = len(k[0][0]) - 1
                    continue
                k = re.findall(r'^(%(\d*\.?\d*)Lf)', s[i:])
                if k:
                    arr.append(('long double',
                        '\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)',
                        eval(k[0][1]) if k[0][1] else ''))
                    var_arr.append(arr[-1])
                    flag = len(k[0][0]) - 1
                    continue
                k = re.findall(r'^(%(\d*\.?\d*)c)', s[i:])
                if k:
                    arr.append(('char', '[\n\r]*(.)', eval(k[0][1])
                        if k[0][1] else ''))
                    var_arr.append(arr[-1])
                    flag = len(k[0][0]) - 1
                    continue
                k = re.findall(r'^(%(\d*\.?\d*)s)', s[i:])
                if k:
                    arr.append(('string', '\s*(\S+)', eval(k[0][1])
                        if k[0][1] else ''))
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
    l = 0
    for tup in regex_arr:
        reg = '^' + tup[1]
        num = tup[2] if tup[2] else 999999
        k = re.findall(reg, Globals.inp[:num])
        if not k:
            raise Exceptions.any_user_error("Incorrect Input (probably)", reg, Globals.inp[:num], num)

        l1 = len(Globals.inp)
        if tup not in type_arr:
            k = re.sub(reg, '', Globals.inp[:num])
            Globals.inp = k + Globals.inp[num:]
        else:
            Globals.inp = re.sub(reg, '', Globals.inp[:num]) + Globals.inp[num:]
            values.append(k[0])
        l +=  (l1 - len(Globals.inp))
    return values, l


def handle_input(statement, scope):
    # statement is something like scanf("%d %c\n%lld", &a, &b, &c)
    statement = Globals.unescape(statement)

    # sep = [('%d %c\n%lld', ' &a, &b,', ' &c')]
    sep = re.findall(r'(?s)scanf\s*\(\s*\"(.*)\"\s*,(.*,)*(.*)\)', statement)

    if len(sep) == 0:
        return 0
    elif len(sep) > 1:
        return Exceptions.any_user_error("I think you might be missing a semicolon")

    type_arr, regex_arr = var_types(sep[0][0])


    variables = Globals.toplevelsplit(sep[0][1], ',')
    variables = variables[:-1]
    variables.append(sep[0][2])
    # now, variables = ['&a', '&b', '&c']

    values, len_inp = extract(regex_arr, type_arr)

    assert len(type_arr) == len(values)

    if len(values) != len(variables):
        raise Exceptions.any_user_error("Incorrect number of argument in ", statement)
    else:

        for i in range(0, len(variables)):
            v = (Calc.calculate(variables[i], scope),)
            dst_type = Globals.memory[v][0].type[0] \
                    if Globals.memory[v][0].type[1] == 0 else 'pointer'
            src_type = type_arr[i][0]

            if not is_same(dst_type, src_type):
                raise Exceptions.any_user_error("Variable Type not same as input!!")

            vals = get_input_value(values[i], src_type)

            if src_type == 'string':
                for i in range(0, len(vals)):
                    Vars.set_val((v[0]+i*Globals.memory[v][1],), ord(vals[i]))
                Vars.set_val((v[0]+len(vals)*Globals.memory[v][1],), 0)
            else:
                Vars.set_val(v, vals)

    return len_inp
