import re

from Globals import print1, print2, print3
from Globals import Value
import Globals
import Calc
import IO
import Groups
import Vars
import Exceptions


def makeMemory(mem, indices, l, type, val, scope):
    mem = (mem, )
    step = Globals._size_of(type if l == 0 else 'pointer')
    Globals.memory[mem][0].v = malloc(indices[0] if indices else 1, step, l, val, scope, type)
    if indices[1:]:
        for i in range(0, indices[0]):
            if val is '':
                makeMemory(Globals.memory[mem][0].v + i*step, indices[1:], l-1, type, '', scope)
            elif i < len(val):
                makeMemory(Globals.memory[mem][0].v + i*step, indices[1:], l-1, type, val[i], scope)
            else:
                makeMemory(Globals.memory[mem][0].v + i*step, indices[1:], l-1, type, [], scope)


dim = []


def malloc(num, step, level, val, scope, cast):
    assert level >= 0
    ret = Globals.curr_mem
    for i in range(0, num):
        if level or val is '':
            Globals.memory[(Globals.curr_mem,)] = [Value('', (cast, level)), step, level + 1]
        else:
            Globals.memory[(Globals.curr_mem,)] = [Value(Calc.calculate(val[i], scope), (cast, level)) if i < len(val) else Value(0, (cast, level)), step, level + 1]
        Globals.curr_mem += step
    return ret


def str_to_mem(str1, scope):
    str_size = len(str1)+1
    mem = Globals.curr_mem
    Globals.curr_mem += Globals._size_of('pointer')
    Globals.memory[( mem, )] = [ Globals.Value(type=('char', 1)), Globals._size_of('pointer'), 2]
    ret_mem = Globals.curr_mem
    makeMemory(mem, [str_size], 0, 'char',
            ["'"+Globals.escape(ch)+"'" for ch in str1] + ["'\000'"], scope)
    return ( mem, )



def decl(var, val, cast, scope, tags):
    pointers = re.findall('\*+', var)
    if pointers:
        level = len(pointers[0])
        var = re.sub('\*', '', var)
        var = re.sub('\s', '', var)
    else:
        level = 0

    if scope.endswith("-invalid-"):
        raise Exceptions.any_user_error("Variable declaration not allowed within switch case")

    data = Globals.get_details(var)
    var, indices = data[0], data[1]

    indices = [Calc.calculate(ind, scope) for ind in indices]
    level += len(indices)
    key = Globals.in_var_table(var, scope)
    if key and key[1] == scope:
        raise Exceptions.any_user_error("Multiple declaration of variable " + var)

    newKey = (var, scope, Globals.curr_mem)
    Globals.var_table[newKey] = [Value(val, (cast, level), tags), cast, level, Globals.curr_mem]

    if level:
        size = Globals._size_of('pointer')
    else:
        size = Globals._size_of(cast)

    Globals.memory[(Globals.curr_mem,)] = [Globals.var_table[newKey][0], size, level+1]

    Globals.gui += "\ndefine_variable('{0}', '{1}', '{2}', '{3}', '{4}')".format(
            cast, '-'.join(scope.split()), var, str(val), Globals.curr_mem )

    if level == 0:
        Globals.curr_mem += Globals._size_of(cast)
    else:
        Globals.curr_mem += Globals._size_of('pointer')

    if indices:
        if val is not '':
            val = val.strip()
            val = split_array_initialization(val[1:-1])
            global dim
            dim = []
            dimension_list(val)
            if indices[0] is 0:
                indices[0] = dim[0]
                #raise Exceptions.any_user_error("Dimensions of array and initialized value don't match")
            # check if input matches with dimension of array, else raise user_error Exception
        makeMemory(Globals.curr_mem - Globals._size_of('pointer'), indices, level - 1, cast, val, scope)


def dimension_list(val):
    global dim
    if type(val) is list:
        dim.append(len(val))
        dimension_list(val[0])


def split_array_initialization(val):
    i = 0
    list = []
    cur_val = ''
    val = Globals.toplevelreplace(val, ' ', '')
    while i < len(val):
        if val[i] is '{':
            temp = get_matching_brace(val, i)
            list.append(split_array_initialization(val[i+1:temp]))
            i = temp
        elif val[i] is ',':
            if cur_val is not '':
                list.append(cur_val)
                cur_val = ''
        else:
            cur_val += val[i]
        i += 1
    if cur_val is not '':
        list.append(cur_val)
    return list


def get_matching_brace(val, i):
    brack = 1
    while brack:
        i += 1
        if val[i] is '{':
            brack += 1
        elif val[i] is '}':
            brack -= 1
    return i



def get_key(var, scope):
    var = Globals.get_details(var)
    name = var[0]
    indices = var[1]
    if indices:
        indices = [Calc.calculate(ind, scope) for ind in indices]
        key = Globals.in_var_table(name, scope)
        return resolve(key, indices, scope)
    else:
        name = Globals.unescape(name)
        if re.match(r"^(?s)'.'$", name):
            ret = ord(name[1:-1])
            return ret
        if re.match(r"^(?s)\".*\"$", name):
            ret = str_to_mem(name[1:-1], scope)
            return ret
        ret = Globals.in_var_table(name, scope)
        if ret == 0:
            raise Exceptions.any_user_error("Invalid variable", name, "used")
        return ret


def get_key_first(var, scope):
    var = Globals.get_details(var)
    name = var[0]
    indices = var[1]
    if indices:
        indices = [0 for ind in indices]
        key = Globals.in_var_table(name, scope)
        return resolve(key, indices, scope)
    else:
        name = Globals.unescape(name)
        if re.match(r"'.'", name):
            return ord(name[1:-1])
        return Globals.in_var_table(name, scope)


def resolve(key, indices, scope):
    k = key
    while indices:
        k = (Vars.get_val(k, scope),)
        k = (k[0] + Globals.memory[k][1]*indices[0], )
        indices.pop(0)
    return k


def chk_decl(line, scope):

    r = re.findall(
        r'^(?s)\s*(static\s+)?(const\s+)?(long\s+double|long\s+long\s+int|'
        r'long\s+long|long\s+int|long|int|float|double|char)', line)
    if len(r) != 0:
        line = re.sub(r[0][2], r[0][2] + ' ', line)
    r = re.findall(
        r'^(?s)\s*(static\s+)?(const\s+)?(long\s+double|long\s+long\s+int|'
        r'long\s+long|long\s+int|long|int|float|double|char)\s+'
        r'((\s*\**\s*[a-zA-Z_]+[a-zA-Z0-9_]*(\[.*\])*)(\s*=\s*(.*?))?\s*,)'
        r'*((\s*\**\s*[a-zA-Z_]+[a-zA-Z0-9_]*(\[.*\])*)(\s*=\s*(.*?))?\s*;)',
        line)

    if len(r) != 0:
        r = r[0]
        cast = r[2]
        tags = (r[0], r[1])
        a = re.sub(r'^(?s)\s*(static\s+)?(const\s+)?' + cast, '', line)
        a = re.sub(';', '', a)
        a = Globals.toplevelsplit(a, ',')
        a = [Globals.toplevelsplit(k.strip(), '=') for k in a]
        for variables in a:
            if len(variables) == 1:
                decl(variables[0].strip(), '', cast, scope, tags)
            else:
                decl(variables[0].strip(), Calc.calculate(variables[1], scope,\
                        Globals.var_table), cast, scope, tags)
        return True
    else:
        return False


def is_updation(exp):
    k = re.match(r'^(?s)\s*[a-zA-Z_]+[a-zA-Z0-9_]*\s*=.*;', exp)
    return 1 if k else 0


def garbage_collector(scope):
    Globals.gui += "\ndelete_scope(\'"+'-'.join(scope.split())+"\');"
    keys = Globals.var_table.keys()
    for key in list(keys):
        if key[1] == scope:
            del Globals.var_table[key]
            del Globals.memory[(key[2],)]
    return


def halter(line):
    if re.match(r'^(?s)\s*break\s*;', line):
        raise Exceptions.custom_break;
    if re.match(r'^(?s)\s*continue\s*;', line):
        raise Exceptions.custom_continue;


def run_through(code, num):
    i = num

    while i < len(code):
        line = code[i]
        i += 1
        if type(line) != str:
            continue
        k = re.findall(r'^(?s)\s*(long\s+double|long\s+long\s+int|long\s+long|long\s+int'
                r'|long|int|float|double|char|void)\s+'
                r'([a-zA-Z_]+[a-zA-Z0-9_]*)\s*\((.*)\)\s*$', line)
        if k:
            assert len(k) == 1
            k = k[0]
            params = [a.strip() for a in k[2].split(',')]
            for index, par in enumerate(params):
                params[index] = Globals.separate_def(par)
            if len(params[0]) > 0:
                type_key = tuple([temp[0] for temp in params])
            else:
                type_key = ''
            if k[1] in Globals.functions and Globals.functions[k[1]][2] == '' \
                    and Globals.functions[k[1]][3] == type_key:
                Globals.functions[k[1]] = [k[0], params, code[i], type_key]


def decl_func(line):
    k = re.findall(r'^(?s)\s*(long\s+double|long\s+long\s+int|long\s+long|long\s+int'
            r'|long|int|float|double|char|void)\s+'
            r'([a-zA-Z_]+[a-zA-Z0-9_]*)\s*\((.*)\)\s*;\s*$', line)
    if k:
        assert len(k) == 1
        k = k[0]
        params = [a.strip() for a in Globals.toplevelsplit(k[2], ',')]
        for index, par in enumerate(params):
            params[index] = Globals.separate_def(par)
        if len(params[0]) > 0:
            type_key = tuple([temp[0] for temp in params])
        else:
            type_key = ''
        if k[1] in Globals.functions:
            raise Exceptions.any_user_error("Error!! Multiple declaration of function\n")
        else:
            Globals.functions[k[1]] = [k[0], params, '', type_key]
        return 1
    else:
        return 0


def def_func(line, code, num):
    k = re.findall(r'^(?s)\s*(long\s+double|long\s+long\s+int|long\s+long'
                   r'|long\s+int|long|int|float|double|char|void)\s+'
                   r'([a-zA-Z_]+[a-zA-Z0-9_]*)\s*\((.*)\)\s*$', line)
    if k:
        assert len(k) == 1
        k = k[0]
        params = [a.strip() for a in Globals.toplevelsplit(k[2], ',')]
        for index, par in enumerate(params):
            params[index] = Globals.separate_def(par)
        if len(params[0]) > 0:
            type_key = tuple([temp[0] for temp in params])
        else:
            type_key = ''
        if k[1] == 'main':
            run_through(code, num + 1)
            execute(code[num], 'global main')
            raise Exceptions.main_executed(Globals.gui)
        if k[1] in Globals.functions and (Globals.functions[k[1]][2] != '' or Globals.functions[k[1]][3] != type_key):
            raise Exceptions.any_user_error("Error! Multiple declaration of function")
        else:
            Globals.functions[k[1]] = [k[0], params, code[num], type_key]
        return 1
    elif decl_func(line):
        return 1
    else:
        return 0


def traverse(code, scope):
    Globals.gui += "create_scope('simulation', 'global');"
    i = 0
    while i < len(code):
        line = code[i]
        i += 1
        if type(line) is not str:
            continue
        if len(line) < 1:
            continue
        if chk_decl(line, scope):
            continue
        if is_updation(line):
            Calc.calculate(line, scope, Globals.var_table)
            continue
        if decl_func(line):
            continue
        if def_func(line, code, i):
            continue
        print("Unrecognized something", line)
        exit(0)


def execute(code, scope):
    if code == []:
        return

    gui_parent = '-'.join(scope.split()[:-1]) \
            if '-'.join(scope.split()[:-1]) else 'simulation'
    gui_str = "\ncreate_scope('{0}', '{1}')".format(gui_parent, '-'.join(scope.split()))

    if not Globals.gui.endswith(gui_str):
        Globals.gui += gui_str
    if type(code) is str:
        r = execute([code], scope)
        if r is not None:
            garbage_collector(scope)
            return r
    i = 0

    r = Groups.if_conditionals(code, scope)
    if r is not "NO":
        return r

    r = Groups.if_for(code, scope)
    if r is not "NO":
        return r

    r = Groups.if_while(code, scope)
    if r is not "NO":
        return r

    r = Groups.if_do_while(code, scope)
    if r is not "NO":
        return r

    r = Groups.if_switch(code, scope)
    if r is not "NO":
        return r

    while i < len(code):
        line = code[i]
        i += 1
        if type(line) is list:
            r = execute(line, scope + " " + str(i - 1))
            if r is not None:
                garbage_collector(scope)
                return r
            continue
        if len(line) < 1:
            continue

        code[i-1] = "__ITS_FLAG__"+code[i-1]
        diff_index = str(Globals.code).find("__ITS_FLAG__")
        from StringDiff import getIndex
        diff_index = getIndex(str(Globals.code), Globals.raw_code, diff_index)
        code[i-1] = code[i-1].replace("__ITS_FLAG__", '')
        line_number = Globals.raw_code.count("\n", 0, diff_index)
        Globals.gui += "\nhighlight_line("+str(line_number)+")"
        inp = IO.handle_input(line, scope)
        if inp:
            Globals.gui+="\nstdin_write("+str(inp)+")"
            continue
        if chk_decl(line, scope):
            continue
        if is_updation(line):
            Calc.calculate(line, scope, Globals.var_table)
            continue
        if halter(line):
            continue
        ret = re.findall(r'^\s*return(?:\s+(.*)\s*)?;\s*$', line);
        if ret:
            ret = Calc.calculate(ret[0], scope)
            garbage_collector(scope)
            return ret
        Calc.calculate(line, scope, Globals.var_table)
    garbage_collector(scope)
