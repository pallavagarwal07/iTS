from globals import print1, print2, print3
import globals
import Exceptions
import re
import sys
import Calc
import Vars


def handle_input(statement, scope):
    statement = statement.decode('string_escape')
    sep = re.findall(r'(?s)scanf\s*\(\s*\"(.*)\"\s*,(.*,)*(.*)\)', statement)
    if len(sep) == 0:
        return False
    variables = sep[0][1].replace('&', '').split(',')
    variables.append(sep[0][2].replace('&', ''))
    variables.remove('')
    reg = re.sub(r'%(lld|ld|d)', '%d', sep[0][0])
    reg = re.sub(r'%(Lf|lf|f)', '%f', reg)
    reg = reg.replace(' ', r'\s+')
    reg = reg.replace('\n', r'\s+')
    reg = reg.replace('\r', r'\s+')
    reg = reg.replace('%d', r'\s*([-+]?\d+)')
    reg = reg.replace('%f', r'\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?)')
    reg = reg.replace('%c', r'[\n\r]*(.)')
    reg = reg.replace('%s', r'\s*(\S+)')
    reg = '^{0}'.format(reg)
    values = re.findall(reg, globals.inp)
    globals.inp = re.sub(reg, '', globals.inp)
    if len(values) == 0:
        return False
    if type(values[0]) is str:
        values = [[values[0]]]

    if len(values[0]) != len(variables):
        raise Exceptions.any_user_error("Incorrect number of arguments or bug in my interpreter", values, variables)
    else:
        for i in range(0, len(variables)):
            v = variables[i].strip()
            vals = (eval(values[0][i]) if globals.is_num(values[0][i]) != 'Error' else values[0][i])
            key = globals.in_var_table(v, scope)
            Vars.set_val(key, vals)
    return True

def handle_output(line, scope):
    line = line.decode('string_escape')
    sep = re.findall(r'(?s)printf\s*\(\s*\"(.*)\"\s*(,.+)*\s*\)', line)
    if len(sep) == 0:
        return False
    if type(sep[0]) is str:
        sep = [[sep[0]]]
    format_string = sep[0][0]
    if sep[0][1] == '':
        globals.out.write(format_string)
    else:
        format_vars = globals.toplevelsplit(sep[0][1][1:], ',')
        for i in range(0, len(format_vars)):
            if format_vars[i] != '':
                format_vars[i] = Calc.calculate(format_vars[i].strip(), scope, globals.var_table)
        format_string = re.sub(r'%(\d*\.?\d*)(lld|ld|d)', r'%\1d', format_string)
        format_string = re.sub(r'%(\d*\.?\d*)(Lf|lf|f)', r'%\1f', format_string)
        format_string = format_string % tuple(format_vars)
        globals.out.write(format_string)
    return True
