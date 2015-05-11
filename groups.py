import globals
import Calc
import re
import Runtime


# if condition
def if_conditionals(code, scope):
    line = code[0]
    if type(line) is list:
        expr = []
    else:
        expr = re.findall(r'^(?s)if\s*\((.*)\)', line)
    if len(expr) != 0:
        flag = Calc.calculate(expr[0], scope, globals.var_table)
        ret = None
        if flag:
            ret = Runtime.execute(code[1], scope + ['1'])
        elif len(code) > 2:
            ret = Runtime.execute(code[3], scope + ['3'])
        return ret
    else:
        return "NO"


def if_for(code, scope):
    line = code[0]
    if type(line) is list:
        expr = []
    else:
        expr = re.findall(r'^(?s)for\s*\((.*);(.*);(.*)\)', line)
    if len(expr) != 0:
        Calc.calculate(expr[0][0], scope, globals.var_table)
        flag = Calc.calculate(expr[0][1], scope, globals.var_table)
        ret = None
        while flag:
            ret = Runtime.execute(code[1], scope + ['1'])
            if ret is not None:
                return ret
            Calc.calculate(expr[0][2], scope, globals.var_table)
            flag = Calc.calculate(expr[0][1], scope, globals.var_table)
        return ret
    else:
        return "NO"


def if_while(code, scope):
    line = code[0]
    if type(line) is list:
        expr = []
    else:
        expr = re.findall(r'^(?s)while\s*\((.*)\)', line)
    if len(expr) != 0:
        ret = None
        flag = Calc.calculate(expr[0], scope, globals.var_table)
        while flag:
            ret = Runtime.execute(code[1], scope + ['1'])
            if ret is not None:
                return ret
            flag = Calc.calculate(expr[0], scope, globals.var_table)
        return ret
    else:
        return "NO"


def if_do_while(code, scope):
    line = code[0]
    if type(line) is list:
        expr = []
    else:
        expr = re.findall(r'^(?s)do', line)
    if len(expr) != 0:
        condition = re.findall(r'^(?s)while\s*\((.*)\)\s*;', code[2]);
        if len(condition) == 0:
            print "Error"
            exit(0)
        else:
            ret = None
            flag = 1
            while flag:
                ret = Runtime.execute(code[1], scope + ['1'])
                if ret is not None:
                    return ret
                flag = Calc.calculate(condition[0], scope, globals.var_table)
            return ret
    else:
        return "NO"
