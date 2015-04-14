import re
import globals
import Utils
import Calc
import io
import groups


def decl(var, val, cast, scope):
    key = globals.in_var_table(var, scope)
    if key and key[1] == scope:
        print("Error")
        return
    globals.var_table[(var, scope)] = [val, cast, scope]


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
                decl(variables[0].strip(), Utils.handle_num(variables[1]), cast, scope)
        return True
    else:
        return False


def update(var, val, scope):
    key = globals.in_var_table(var, scope)
    if key:
        globals.var_table[key][0] = val
    else:
        print('Error')
        return


def is_updation(exp):
    k = re.match(r'^(?s)\s*[a-zA-Z_]+[a-zA-Z0-9_]*\s*=.*;', exp)
    return 1 if k else 0


def garbage_collector(scope):
    keys = globals.var_table.keys()
    # print "Collecting Garbage for Scope :", scope, keys
    scope = " ".join(scope)
    for key in keys:
        if key[1] == scope:
            # print "Found garbage with Key :", key
            del globals.var_table[key]
    return


def execute(code, scope):
    # print "abc", code
    # print "abc", code
    # print globals.var_table
    if type(code) is str:
        execute([code], scope)
        return
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
        if line == 'int':
            continue
        if type(line) is list:
            execute(line, scope + [str(i - 1)])
            continue
        if len(line) < 1:
            continue
        if chk_decl(line, " ".join(scope)):
            continue
        if io.handle_input(line, " ".join(scope)):
            continue
        if io.handle_output(line, " ".join(scope)):
            continue
        # print "Here1"
        if is_updation(line):
            Calc.calculate(line, " ".join(scope), globals.var_table)
            continue

    garbage_collector(scope)