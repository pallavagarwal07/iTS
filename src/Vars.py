from globals import print1, print2, print3, is_num
import globals
import Calc
import Runtime
import re
import Exceptions

def get_type(key, scope):
    print2("key: ", key)
    if type(key) is not tuple:
        n = is_num(key)
        print2("n: ", n)
        if 'Error' == n:
            k = re.findall('^\s*([a-zA-Z_]+[a-zA-Z0-9_]*)\s*\((.*)\)\s*$', key)
            if k:
                return globals.functions[k[0][0]][0] 
                #hnadle function return types properly
            else:
                key = Runtime.get_key(key, scope)
                if type(key) is int:
                    return 'number'
        else:
            return 'number'
    if len(key) != 1:
        t = globals.in_var_table(key[0], key[1])
        if t:
            return globals.var_table[t][1]
    else:
        if key in globals.memory:
            print2("get_type3:", globals.memory[key][1])
            return globals.memory[key][1]
        else:
            raise Exceptions.any_user_error("Invalid Memory location", key)


def get_val(key, scope):
    print2("key: ", key)
    if type(key) is not tuple:
        n = is_num(key)
        print2("n: ", n)
        if 'Error' == n:
            k = re.findall('^\s*([a-zA-Z_]+[a-zA-Z0-9_]*)\s*\((.*)\)\s*$', key)
            if k:
                val = Calc.pass_to_func(k[0], scope)
                return val
            else:
                key = Runtime.get_key(key, scope)
                if type(key) is int:
                    return key
        else:
            return eval(str(key))
    if len(key) != 1:
        t = globals.in_var_table(key[0], key[1])
        if t:
            return globals.var_table[t][0].v
    else:
        if key in globals.memory:
            return globals.memory[key][0].v
        else:
            raise Exceptions.any_user_error("Invalid Memory location", key)


def set_val(key, val, scope = '-none-'):
    if type(key) is not tuple:
        if scope == '-none-':
            raise Exceptions.any_user_error("Something wrong.")
        if is_num(key) == 'Error':
            key = Runtime.get_key(key, scope)
        else:
            raise Exceptions.any_user_error("Error: Trying to assign value to a non-variable")
    if len(key) != 1:
        globals.gui += "\nupdate_variable(\'"+'-'.join(key[1].split())+ \
            "-"+key[0]+"\',\'"+str(val)+"\');"
        t = globals.in_var_table(key[0], key[1])
        if t:
            globals.var_table[t][0].v = val
    else:
        print3("var_table\n", globals.var_table)
        print3("memory:\n", globals.memory)
        if key in globals.memory:
            globals.memory[key][0].v = val
        else:
            raise Exceptions.any_user_error("Invalid Memory location set_val", key)
