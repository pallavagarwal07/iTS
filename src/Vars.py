from globals import print1, print2, print3, is_num
import globals
import Calc
import Runtime
import re
import Exceptions

def get_type(key, scope):
    if type(key) is not tuple:
        n = is_num(key)
        if 'Error' == n:
            k = re.findall('^\s*([a-zA-Z_]+[a-zA-Z0-9_]*)\s*\((.*)\)\s*$', key)
            if k:
                if k[0][0] in globals.predefined_funcs:
                    return 'double'
               #return globals.functions[k[0][0]][0]
                return 'int'
            else:
                key = Runtime.get_key_first(key, scope)
                if type(key) is int:
                    return 'number'
        else:
            return 'number'
    if len(key) != 1:
        t = globals.in_var_table(key[0], key[1])
        if t:
            return globals.var_table[t][1] if globals.var_table[t][2]==0 else 'pointer'
    else:
        if key in globals.memory:
            return globals.memory[key][0].type[0]
        else:
            raise Exceptions.any_user_error("Invalid Memory location", key)


def get_val(key, scope, mul = 1):
    if type(key) is not tuple:
        n = is_num(key)
        if 'Error' == n:
            k = re.findall('^\s*([a-zA-Z_]+[a-zA-Z0-9_]*)\s*\((.*)\)\s*$', key)
            if k:
                if mul != 1:
                    return 0
                val = Calc.pass_to_func(k[0], scope)
                return val
            else:
                if mul == 1:
                    key = Runtime.get_key(key, scope)
                else:
                    key = Runtime.get_key_first(key, scope)
                if type(key) is int:
                    return key
        else:
            return eval(str(key))
    if len(key) != 1:
        t = globals.in_var_table(key[0], key[1])
        if t:
            if mul != 1:
                if globals.var_table[t][0].type[1] != 0:
                    return 0
            return globals.var_table[t][0].v
    else:
        if key in globals.memory:
            if mul != 1:
                if globals.memory[key][0].type[1] != 0:
                    return 0
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
        if key in globals.memory:
            globals.memory[key][0].v = val
        else:
            raise Exceptions.any_user_error("Invalid Memory location set_val", key)
