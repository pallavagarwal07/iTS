from math import *

from .Globals import print1, print2, print3
from . import Calc

#Power Functions

funcs = {}


def __sqrt__(x):
    return sqrt(x)


def __pow__(x, y):
    return pow(x, y)


def __cbrt__(x):
    return pow(x, (1.0/3.0))


def __hypot__(x, y):
    return sqrt(x*x + y*y)


# Rounding and remainder functions


def __ceil__(x):
    return ceil(x)


def __floor__(x):
    return floor(x)


def __fmod__(x, y):
    return fmod(x, y)


def __fabs__(x):
    return fabs(x)


def __abs__(x):
    return abs(x)

def __round__(x):
    return round(x)


#Expoential and Logarithmic functions


def __exp__(x):
    return exp(x)


def __frexp__(x, y):
    return frexp(x)


def __ldexp__(x, y):
    return ldexp(x, y)


def __log__(x):
    return log(x)


def __log10__(x):
    return log10(x)


def __log2__(x):
    return log(x, 2)


def __modf__(x, y):
    return modf(x)


def __exp2__(x):
    return pow(2, x)


def __expm1__(x):
    return expm1(x)


#Trigonomentric and Hyperbolic functions


def __sin__(x):
    return sin(x)


def __asin__(x):
    return asin(x)


def __sinh__(x):
    return sinh(x)


def __asinh__(x):
    return asinh(x)


def __cos__(x):
    return cos(x)


def __acos__(x):
    return acos(x)


def __cosh__(x):
    return cosh(x)


def __acosh__(x):
    return acosh(x)


def __tan__(x):
    return tan(x)


def __atan__(x):
    return atan(x)


def __tanh__(x):
    return tanh(x)


def __atanh__(x):
    return atanh(x)


def __atan2__(x):
    return atan2(x)




funcs = {'sqrt':__sqrt__, 'pow':__pow__, 'cbrt':__cbrt__, 'hypot':__hypot__, 'ceil':__ceil__,
'floor':__floor__, 'fmod':__fmod__, 'fabs':__fabs__, 'abs':__abs__, 'round':__round__,
'exp':__exp__, 'frexp':__frexp__, 'ldexp':__ldexp__, 'log':__log__, 'log10':__log10__,
'log2':__log2__, 'modf':__modf__, 'exp2':__exp2__, 'expm1':__expm1__, 'sin':__sin__,
'asin':__asin__, 'sinh':__sinh__, 'asinh':__asinh__, 'cos':__cos__, 'acos':__acos__,
'cosh':__cosh__, 'acosh':__acosh__, 'tan':__tan__, 'atan':__atan__, 'tanh':__tanh__,
'atanh':__atanh__, 'atan2':__atan2__}


def invoke(name, params, scope):
    print2(name, params, scope)
    p = []
    for i in range(0,len(params)):
        p.append(Calc.calculate(params[i], scope))
    if name in ['pow', 'hypot', 'fmod', 'modf', 'ldexp', 'frexp']:
        return funcs[name](p[0], p[1])
    else:
        return funcs[name](p[0])
