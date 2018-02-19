import re

from .Globals import print1, print2, print3
from . import Globals
from . import Calc
from . import Runtime
from . import Exceptions


# if condition
def if_conditionals(code, scope):
    line = code[0]
    if type(line) is list:
        expr = []
    else:
        expr = re.findall(r'^(?s)if\s*\((.*)\)', line)
    if len(expr) != 0:

        # Try to get line number
        code[0] = "__ITS_FLAG__"+code[0]
        diff_index = str(Globals.code).find("__ITS_FLAG__")
        from .StringDiff import getIndex
        diff_index = getIndex(str(Globals.code), Globals.raw_code, diff_index)
        code[0] = code[0].replace("__ITS_FLAG__", '')
        line_number = Globals.raw_code.count("\n", 0, diff_index)
        Globals.gui += "\nhighlight_line("+str(line_number)+")"

        flag = Calc.calculate(expr[0], scope, Globals.var_table)
        ret = None
        if flag:
            Globals.gui += "\ncustom_highlight("+str(line_number)+", green)"
            ret = Runtime.execute(code[1], scope + ' 1')
        else:
            Globals.gui += "\ncustom_highlight("+str(line_number)+", red)"
            if len(code) > 2:
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

        # Try to get line number
        code[0] = "__ITS_FLAG__"+code[0]
        diff_index = str(Globals.code).find("__ITS_FLAG__")
        from .StringDiff import getIndex
        diff_index = getIndex(str(Globals.code), Globals.raw_code, diff_index)
        code[0] = code[0].replace("__ITS_FLAG__", '')
        line_number = Globals.raw_code.count("\n", 0, diff_index)
        Globals.gui += "\nhighlight_line("+str(line_number)+")"

        Calc.calculate(expr[0][0], scope, Globals.var_table)
        flag = Calc.calculate(expr[0][1], scope, Globals.var_table)
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
            Calc.calculate(expr[0][2], scope, Globals.var_table)
            flag = Calc.calculate(expr[0][1], scope, Globals.var_table)
        return ret
    else:
        return "NO"


def if_switch(code, scope):
    line = code[0]
    if type(line) is list:
        expr = []
    else:
        expr = re.findall(r'^(?s)switch\s*\((.+)\)', line)

    if len(expr) != 0:

        # Try to get line number
        code[0] = "__ITS_FLAG__"+code[0]
        diff_index = str(Globals.code).find("__ITS_FLAG__")
        from .StringDiff import getIndex
        diff_index = getIndex(str(Globals.code), Globals.raw_code, diff_index)
        code[0] = code[0].replace("__ITS_FLAG__", '')
        line_number = Globals.raw_code.count("\n", 0, diff_index)
        Globals.gui += "\nhighlight_line("+str(line_number)+")"

        print2("if_switch got: ", code[0], scope, expr[0])
        switch_val = Calc.calculate(expr[0], scope)
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
                print1("CAL = " , cal, type(cal), switch_val, type(switch_val))
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

        # Try to get line number
        code[0] = "__ITS_FLAG__"+code[0]
        diff_index = str(Globals.code).find("__ITS_FLAG__")
        from .StringDiff import getIndex
        diff_index = getIndex(str(Globals.code), Globals.raw_code, diff_index)
        code[0] = code[0].replace("__ITS_FLAG__", '')
        line_number = Globals.raw_code.count("\n", 0, diff_index)
        Globals.gui += "\nhighlight_line("+str(line_number)+")"

        ret = None
        flag = Calc.calculate(expr[0], scope, Globals.var_table)
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
            flag = Calc.calculate(expr[0], scope, Globals.var_table)
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

        # Try to get line number
        code[0] = "__ITS_FLAG__"+code[0]
        diff_index = str(Globals.code).find("__ITS_FLAG__")
        from .StringDiff import getIndex
        diff_index = getIndex(str(Globals.code), Globals.raw_code, diff_index)
        code[0] = code[0].replace("__ITS_FLAG__", '')
        line_number = Globals.raw_code.count("\n", 0, diff_index)
        Globals.gui += "\nhighlight_line("+str(line_number)+")"

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
                flag = Calc.calculate(condition[0], scope, Globals.var_table)
            return ret
    else:
        return "NO"
