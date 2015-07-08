from globals import print1, print2, print3, is_num
import globals
import Calc
import Runtime
import re
import Exceptions


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
        else:
            return key
    if len(key) != 1:
        t = globals.in_var_table(key[0], key[1])
        if t:
            return globals.var_table[t][0].v
    else:
        if key in globals.memory:
            return globals.memory[key][0].v
        else:
            raise Exceptions.any_user_error("Invalid Memory location get_val")


def set_val(key, val, scope):
    if type(key) is not tuple:
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
