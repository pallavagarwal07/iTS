import re

from . import IO
from . import Calc
from . import Globals
from . import Exceptions

def printf(params, scope):
    params = [Calc.calculate(k, scope) for k in params]
    fmt = Globals.get_str(params[0])
    type_arr, regex_arr = IO.var_types(fmt)
    format_vars, format_string = params[1:], ''
    j = 0
    for i, ch in enumerate(regex_arr):
        if ch[0] in ['literal', 'whitespace']:
            format_string += ch[3]
        else:
            while format_vars[j] == '':
                j += 1

            v = format_vars[j]
            if ch[0] is 'char':
                format_string +=  chr(v)
            elif ch[0] is 'string':
                step = Globals.memory[(v,)][1]
                c = 0;
                while Globals.memory[(v + c*step,)][0].v is not 0:
                    format_string += chr(Globals.memory[(v+c*step,)][0].v)
                    c += 1
            else:
                st = '%' + str(ch[2])
                if ch[0] in ['int', 'long', 'long long']:
                    st += 'd'
                else:
                    st += 'f'
                format_string += st % v
            j += 1
    Globals.out.write(format_string)

    gui_out = Globals.b64encode(format_string)
    Globals.gui += "\nstdout_print('"+gui_out+"');"

    return True

def scanf(params, scope):
    return True

fnx = {
    'scanf': scanf, 'printf': printf
    }

def invoke(name, params, scope):
    if name == 'sizeof':
        if len(params) != 1:
            raise Exceptions.any_user_error("Incorrect number of parameters.")
        params = [ Globals.get_str(params[0]) ]
        t = re.findall(r'\*', params[0])
        if t:
            return Globals.sizeof['pointer']
        else:
            return Globals.sizeof[params[0].strip()]
    if name == 'malloc':
        raise Exceptions.any_user_error("Malloc hasn't been implemented yet.")

    if name in fnx:
        return fnx[name](params, scope)
