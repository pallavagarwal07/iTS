from __future__ import print_function, absolute_import, division
from abc import abstractmethod

from .Exceptions import any_user_error
from .Globals import priority_type

def typecast(obj, type_T, force=False):
    if obj.typeclass == 'point' and type_T.typeclass == 'num':
        if not force:
            raise any_user_error(
                    "Value", obj.val, "implicitly converted to",
                    int(obj.val), "causing possible loss of precision. ",
                    "Please use explicit type casting to allow this.")
    return type_T(obj.val)

def common_type(obj1, obj2):
    p1 = priority_type[obj1.STR]
    p2 = priority_type[obj2.STR]

    if p1 > p2:
        obj2 = typecast(obj2, type(obj1))
    else:
        obj1 = typecast(obj1, type(obj2))

    return (obj1, obj2)

def coerce(fnx):
    def output(obj1, obj2):
        if type(obj1) == type(obj2):
            return fnx(obj1, obj2)
        obj1, obj2 = common_type(obj1, obj2)
        return getattr(obj1, fnx.__name__)(obj2)
    return output

class Numeric:
    MAX =  float('Inf')
    MIN = -float('Inf')
    val = 0.0

    @abstractmethod
    def __div__(self, other):
        pass

    @abstractmethod
    def __divmod__(self, other):
        pass

    @abstractmethod
    def __mod__(self, other):
        pass

    @abstractmethod
    def __lshift__(self, other):
        pass

    @abstractmethod
    def __rshift__(self, other):
        pass

    @abstractmethod
    def __and__(self, other):
        pass

    @abstractmethod
    def __xor__(self, other):
        pass

    @abstractmethod
    def __or__(self, other):
        pass

    # Implementation of the following functions is common for all types.
    @coerce
    def __add__(self, other):
        val = self.val + other.val
        return type(self)(val)

    @coerce
    def __sub__(self, other):
        val = self.val - other.val
        return type(self)(val)

    @coerce
    def __mul__(self, other):
        val = self.val * other.val
        return type(self)(val)

    @coerce
    def __pow__(self, other, modulo=float('Inf')):
        val = self.val ** other.val
        return type(self)(val)

    def __neg__(self):
        return type(self)(-self.val)

    def __pos__(self):
        return type(self)(self.val)

    def __abs__(self):
        return type(self)(abs(self.val))

    def __invert__(self):
        return type(self)(~self.val)

    def __int__(self):
        return int(self.val)

    def __long__(self):
        return long(self.val)

    def __float__(self):
        return float(self.val)

    def __oct__(self):
        return oct(self.val)

    def __hex__(self):
        return hex(self.val)

    def __str__(self):
        return str(self.val)

    def __repr__(self):
        return str(self.val)

class Point_T(Numeric):
    typeclass = "point"
    val = 0.0

    def __init__(self, val):
        val = float(val)
        self.val = val

    @coerce
    def __div__(self, other):
        if other.val == 0:
            raise any_user_error("Division by 0 not allowed!")
        val = self.val / other.val
        return type(self)(val)

    @coerce
    def __divmod__(self, other):
        if other.val == 0:
            raise any_user_error("Division by 0 not allowed!")
        raise any_user_error("Modulo applied on types", self.STR, "and",
                other.STR, "which is not allowed. Use modulo on integer ",
                "(and related) types only.")

    @coerce
    def __mod__(self, other):
        raise any_user_error("Modulo applied on types", self.STR, "and",
                other.STR, "which is not allowed. Use modulo on integer ",
                "(and related) types only.")

    @coerce
    def __lshift__(self, other):
        raise any_user_error("Left shift (<<) applied on types", self.STR,
                "and", other.STR, "which is not allowed. Use it on ",
                "integer (and related) types only.")

    @coerce
    def __rshift__(self, other):
        raise any_user_error("Right shift (>>) applied on types", self.STR,
                "and", other.STR, "which is not allowed. Use it on ",
                "integer (and related) types only.")

    @coerce
    def __and__(self, other):
        raise any_user_error("Bitwise and (&) applied on types", self.STR,
                "and", other.STR, "which is not allowed. Use it on ",
                "integer (and related) types only.")

    @coerce
    def __xor__(self, other):
        raise any_user_error("Bitwise XOR (^) applied on types", self.STR,
                "and", other.STR, "which is not allowed. Use it on ",
                "integer (and related) types only.")

    @coerce
    def __or__(self, other):
        raise any_user_error("Bitwise OR ( | ) applied on types", self.STR,
                "and", other.STR, "which is not allowed. Use it on ",
                "integer (and related) types only.")

class Float_T(Point_T):
    STR = 'float'

class Double_T(Point_T):
    STR = 'double'

class LongDouble_T(Point_T):
    STR = 'long double'

class Num_T(Numeric):
    STR = "number"
    MAX =  2**127 - 1
    MIN = -2**127
    typeclass = "num"

    val = 0

    def __init__(self, val):
        val = int(val)
        if val > self.MAX or val < self.MIN:
            raise any_user_error(
                    "Value", val, "out of bounds of the type",
                    self.STR, "which can store values from",
                    self.MIN, "to", self.MAX,".")
        self.val = val

    @coerce
    def __div__(self, other):
        if other.val == 0:
            raise any_user_error("Division by 0 not allowed!")
        val = self.val // other.val
        return type(self)(val)

    @coerce
    def __divmod__(self, other):
        if other.val == 0:
            raise any_user_error("Division by 0 not allowed!")
        val = self.val // other.val
        mod = self.val % other.val
        return (type(self)(val), type(self)(mod))

    @coerce
    def __mod__(self, other):
        if other.val == 0:
            raise any_user_error("Modulo by 0 not allowed!")
        val = self.val % other.val
        return type(self)(val)

    @coerce
    def __lshift__(self, other):
        val = self.val << other.val
        return type(self)(val)

    @coerce
    def __rshift__(self, other):
        val = self.val >> other.val
        return type(self)(val)

    @coerce
    def __and__(self, other):
        val = self.val & other.val
        return type(self)(val)

    @coerce
    def __xor__(self, other):
        val = self.val ^ other.val
        return type(self)(val)

    @coerce
    def __or__(self, other):
        val = self.val | other.val
        return type(self)(val)


class Char_T(Num_T):
    STR = "char"
    MAX =  2**7 - 1
    MIN = -2**7

class Int_T(Num_T):
    STR = "int"
    MAX =  2**31 - 1
    MIN = -2**31

class Long_T(Num_T):
    STR = "long"
    MAX =  2**63 - 1
    MIN = -2**63

class LongLong_T(Num_T):
    STR = "long long"
    MAX =  2**63 - 1
    MIN = -2**63

type_map = {
        "number"        : Num_T,
        "char"          : Char_T,
        "int"           : Int_T,
        "long"          : Long_T,
        "long int"      : Long_T,
        "long long"     : LongLong_T,
        "long long int" : LongLong_T,

        "float"         : Float_T,
        "double"        : Double_T,
        "long double"   : LongDouble_T,
}
