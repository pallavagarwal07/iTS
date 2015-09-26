import re
import i_o
import Calc
import globals
import Exceptions

def printf(params, scope):
    params = [Calc.calculate(k, scope) for k in params]
    fmt = globals.get_str(params[0])
    type_arr, regex_arr = i_o.var_types(fmt)
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
                step = globals.memory[(v,)][1]
                c = 0;
                while globals.memory[(v + c*step,)][0].v is not 0:
                    format_string += chr(globals.memory[(v+c*step,)][0].v)
                    c += 1
            else:
                st = '%' + str(ch[2])
                if ch[0] in ['int', 'long', 'long long']:
                    st += 'd'
                else:
                    st += 'f'
                format_string += st % v
            j += 1
    globals.out.write(format_string)

    import base64
    gui_out = base64.b64encode(format_string)
    globals.gui += "\nstdout_print('"+gui_out+"');"

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
        params = [ globals.get_str(params[0]) ]
        t = re.findall(r'\*', params[0])
        if t:
            return globals.sizeof['pointer']
        else:
            return globals.sizeof[params[0].strip()]
    if name == 'malloc':
        raise Exceptions.any_user_error("Malloc hasn't been implemented yet.")

    if name in fnx:
        return fnx[name](params, scope)
