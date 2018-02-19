from Globals import print1, print2, print3, is_num
import Globals
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
                if k[0][0] in Globals.predefined_funcs:
                    return 'double'
               #return Globals.functions[k[0][0]][0]
                return 'int'
            else:
                key = Runtime.get_key_first(key, scope)
                if type(key) is int:
                    return 'number'
        else:
            return 'number'
    if len(key) != 1:
        t = Globals.in_var_table(key[0], scope)
        if t:
            return Globals.var_table[t][1] if Globals.var_table[t][2]==0 else 'pointer'
    else:
        if key in Globals.memory:
            return Globals.memory[key][0].type[0]
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
        t = Globals.in_var_table(key[0], scope)
        if t:
            if mul != 1:
                if Globals.var_table[t][0].type[1] != 0:
                    return 0
            ret = Globals.var_table[t][0].v
            if ret == '':
                raise Exceptions.any_user_error("Variable " + key[0] + " used "
                        "without initialisation in current line.")
            return Globals.var_table[t][0].v
        else:
            raise Exceptions.any_user_error("Invalid variable used in current line.")
    else:
        if key in Globals.memory:
            if mul != 1:
                if Globals.memory[key][0].type[1] != 0:
                    return 0
            return Globals.memory[key][0].v
        else:
            raise Exceptions.any_user_error("Invalid Memory location", key)


def set_val(key, val, scope = '-none-'):

    if type(key) is not tuple:
        if scope == '-none-':
            raise Exceptions.any_user_error("Something wrong.")
        if is_num(key) == 'Error':
            key = Runtime.get_key(key, scope)
        else:
            raise Exceptions.any_user_error("Trying to assign value to a non-variable")

    if len(key) != 1:
        Globals.gui += "\nupdate_variable(\'"+'-'.join(key[1].split())+ \
            "-"+key[0]+"\',\'"+str(val)+"\');"

        t = Globals.in_var_table(key[0], scope)
        if t:
            Globals.var_table[t][0].v = val
    else:
        Globals.gui += "\nupdate_variable(\'"+str(key[0])+"\',\'"+str(val)+"\');"

        if key in Globals.memory:
            Globals.memory[key][0].v = val
        else:
            raise Exceptions.any_user_error("Invalid Memory location set_val", key)
