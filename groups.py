import globals
import Calc
import re
import Runtime


# if condition
def if_conditional(code, scope):
    print "Here"
    line = code[0]
    print code[0], "wohoo"
    expr = re.findall(r'^(?s)if\s*\((.*)\)', line)
    if len(expr) != 0:
        flag = Calc.calculate(expr[0], scope, globals.var_table)
        print flag, "I am the FLAGGGGGG!"
        if flag:
            Runtime.execute(code[1], scope + ['1'])
        elif len(code) > 2:
            Runtime.execute(code[3], scope + ['3'])
        return len(code) - 1
    else:
        return 0