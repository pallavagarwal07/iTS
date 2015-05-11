import re
import globals
import Calc
import i_o
import groups
import sys


def decl(var, val, cast, scope):
    key = globals.in_var_table(var, scope)
    if key and key[1] == scope:
        print("Error 101: Multiple declaration of variable " + var + "\n")
        return
    globals.var_table[(var, scope)] = [val, cast, scope, globals.curr_mem]
    globals.mem_space[globals.curr_mem] = (var, scope)
    globals.curr_mem += globals.size_of[cast]


def chk_decl(line, scope):
    r = re.findall(
        r'^(?s)\s*(long\s+double|long\s+long\s+int|long\s+long|long\s+int|long|int|float|double|char)\s+'
        '((\s*[a-zA-Z_]+[a-zA-Z0-9_]*)(\s*=\s*(.*?))?\s*,)*((\s*[a-zA-Z_]+[a-zA-Z0-9_]*)(\s*=\s*(.*?))?\s*;)',
        line)
    if len(r) != 0:
        r = r[0]
        cast = r[0]
        a = re.sub(cast, '', line)
        a = re.sub(';', '', a)
        a = a.split(',')
        a = [k.strip().split('=') for k in a]
        for variables in a:
            if len(variables) == 1:
                decl(variables[0].strip(), '', cast, scope)
            else:
                decl(variables[0].strip(), Calc.calculate(variables[1], scope, globals.var_table), cast, scope)
        return True
    else:
        return False


def update(var, val, scope):
    key = globals.in_var_table(var, scope)
    if key:
        globals.var_table[key][0] = val
    else:
        print('Error 103: ' + var + "not declared \n")
        return


def is_updation(exp):
    k = re.match(r'^(?s)\s*[a-zA-Z_]+[a-zA-Z0-9_]*\s*=.*;', exp)
    return 1 if k else 0


def garbage_collector(scope):
    keys = globals.var_table.keys()
    scope = " ".join(scope)
    for key in keys:
        if key[1] == scope:
            del globals.var_table[key]
    return


def run_through(code, num):
    i = num
    while i < len(code):
        line = code[i]
        i += 1
        if type(line) != str:
            continue
        k = re.findall(r'^(?s)\s*(long\s+double|long\s+long\s+int|long\s+long|long\s+int|long|int|float|double|char)\s+'
                       '([a-zA-Z_]+[a-zA-Z0-9_]*)\s*\((.*)\)\s*$', line)
        if k:
            assert len(k) == 1
            k = k[0]
            params = [a.strip() for a in k[2].split(',')]
            for index, par in enumerate(params):
                for data_type in globals.data_types:
                    if par.startswith(data_type):
                        rep = re.sub(data_type + r'\s*', '', par)
                        params[index] = (data_type, rep)
                        break
            if len(params[0]) > 0:
                type_key = tuple([temp[0] for temp in params])
            else:
                type_key = ''
            if k[1] in globals.functions and globals.functions[k[1]][2] == '' \
                    and globals.functions[k[1]][3] == type_key:
                globals.functions[k[1]] = [k[0], params, code[i], type_key]


def decl_func(line):
    k = re.findall(r'^(?s)\s*(long\s+double|long\s+long\s+int|long\s+long|long\s+int|long|int|float|double|char)\s+'
                   '([a-zA-Z_]+[a-zA-Z0-9_]*)\s*\((.*)\)\s*;\s*$', line)
    if k:
        assert len(k) == 1
        k = k[0]
        params = [a.strip() for a in k[2].split(',')]
        for index, par in enumerate(params):
            for data_type in globals.data_types:
                if par.startswith(data_type):
                    rep = re.sub(data_type + r'\s*', '', par)
                    params[index] = (data_type, rep)
                    break
        if len(params[0]) > 0:
            type_key = tuple([temp[0] for temp in params])
        else:
            type_key = ''
        if k[1] in globals.functions:
            print "Error!! Multiple declaration of function\n"
        else:
            globals.functions[k[1]] = [k[0], params, '', type_key]
        return 1
    else:
        return 0


def def_func(line, code, num):
    k = re.findall(r'^(?s)\s*(long\s+double|long\s+long\s+int|long\s+long|long\s+int|long|int|float|double|char)\s+'
                   '([a-zA-Z_]+[a-zA-Z0-9_]*)\s*\((.*)\)\s*$', line)
    if k:
        assert len(k) == 1
        k = k[0]
        params = [a.strip() for a in k[2].split(',')]
        for index, par in enumerate(params):
            for data_type in globals.data_types:
                if par.startswith(data_type):
                    rep = re.sub(data_type + r'\s*', '', par)
                    params[index] = (data_type, rep)
                    break
        if len(params[0]) > 0:
            type_key = tuple([temp[0] for temp in params])
        else:
            type_key = ''
        if k[1] == 'main':
            run_through(code, num + 1)
            execute(code[num], ['global'])
            exit(0)
        if k[1] in globals.functions and (globals.functions[k[1]][2] != '' or globals.functions[k[1]][3] != type_key):
            print "Error!! Multiple declaration of function"
            exit(0)
        else:
            globals.functions[k[1]] = [k[0], params, code[num], type_key]
        return 1
    elif decl_func(line):
        return 1
    else:
        return 0


def traverse(code, scope):
    i = 0
    while i < len(code):
        line = code[i]
        i += 1
        if type(line) is not str:
            continue
        if len(line) < 1:
            continue
        if chk_decl(line, " ".join(scope)):
            continue
        if is_updation(line):
            Calc.calculate(line, " ".join(scope), globals.var_table)
            continue
        if def_func(line, code, i):
            continue


def execute(code, scope):
    if type(code) is str:
        r = execute([code], scope)
        if r is not None:
            garbage_collector(scope)
            return r
    i = 0
    if groups.if_conditionals(code, scope[:]):
        return
    if groups.if_for(code, scope[:]):
        return
    if groups.if_while(code, scope[:]):
        return
    if groups.if_do_while(code, scope[:]):
        return
    while i < len(code):
        line = code[i]
        i += 1
        if type(line) is list:
            r = execute(line, scope + [str(i - 1)])
            if r is not None:
                garbage_collector(scope)
                return r
            continue
        if len(line) < 1:
            continue
        if chk_decl(line, " ".join(scope)):
            continue
        if i_o.handle_input(line, " ".join(scope)):
            continue
        if i_o.handle_output(line, " ".join(scope)):
            continue
        if is_updation(line):
            Calc.calculate(line, " ".join(scope), globals.var_table)
            continue
        ret = re.findall(r'^\s*return\s+(.*)\s*;\s*$', line);
        if ret:
            ret = Calc.calculate(ret[0], scope)
            garbage_collector(scope)
            return ret 
        try:
            Calc.calculate(line, scope, globals.var_table)
        except Exception:
            pass
    garbage_collector(scope)
