from globals import print1, print2, print3
import globals
import Calc
import re
import Runtime
import Exceptions


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
            ret = Runtime.execute(code[1], scope + ' 1')
        elif len(code) > 2:
            ret = Runtime.execute(code[3], scope + ' 3')
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
            try:
                ret = Runtime.execute(code[1], scope + ' 1')
            except Exceptions.custom_break:
                Runtime.garbage_collector(scope + ' 1')
                return ret
            except Exceptions.custom_continue:
                Runtime.garbage_collector(scope + ' 1')
            if ret is not None:
                return ret
            Calc.calculate(expr[0][2], scope, globals.var_table)
            flag = Calc.calculate(expr[0][1], scope, globals.var_table)
        return ret
    else:
        return "NO"


def if_switch(code, scope):
    line = code[0]
    if type(line) is list:
        expr = []
    else:
        expr = re.findall(r'^(?s)switch\s*\((.*)\)', line)


    if len(expr) != 0:
        print2("if_switch got: ", code[0], scope)
        switch_val = Calc.calculate(expr[0][0], scope)
        ret = None

        fall = None
        index_default = None
        for i, tup in enumerate(code[1]):
            if tup[0] == '-default-':
                index_default = i
            elif tup[0] == None:
                continue
            else:
                cal = Calc.calculate(tup[0], scope)
                if switch_val == cal:
                    fall = i
                    break
        if fall == None:
            fall = index_default
        if fall != None:
            i = fall
            try:
                while i < len(code[1]):
                    ret = Runtime.execute(code[1][i][1], scope + ' -invalid-')
                    if ret is not None:
                        return ret
                    i += 1
            except Exceptions.custom_break:
                Runtime.garbage_collector(scope + ' -invalid-')
                return ret
            except Exceptions.custom_continue:
                Runtime.garbage_collector(scope + ' -invalid-')
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
            try:
                ret = Runtime.execute(code[1], scope + ' 1')
            except Exceptions.custom_break:
                Runtime.garbage_collector(scope + ' 1')
                return ret
            except Exceptions.custom_continue:
                Runtime.garbage_collector(scope + ' 1')
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
            raise Exceptions.any_user_error("Error: do_while has no condition.")
        else:
            ret = None
            flag = 1
            while flag:
                try:
                    ret = Runtime.execute(code[1], scope + ' 1')
                except Exceptions.custom_break:
                    Runtime.garbage_collector(scope + ' 1')
                    return ret
                except Exceptions.custom_continue:
                    Runtime.garbage_collector(scope + ' 1')
                if ret is not None:
                    return ret
                flag = Calc.calculate(condition[0], scope, globals.var_table)
            return ret
    else:
        return "NO"
