from __future__ import print_function, absolute_import
from abc import abstractmethod

from .Exceptions import any_user_error

def wrapper(fnx):
    def output(obj1, obj2):
        if type(obj1)
        return fnx(*args)
    return output

class Numeric:
    MAX =  float('Inf')
    MIN = -float('Inf')
    val = 0.0

    @abstractmethod
    def __add__(self, other):
        pass
    
    @abstractmethod
    def __sub__(self, other):
        pass
    
    @abstractmethod
    def __mul__(self, other):
        pass
    
    @abstractmethod
    def __div__(self, other):
        pass
    
    @abstractmethod
    def __mod__(self, other):
        pass
    
    @abstractmethod
    def __divmod__(self, other):
        pass
    
    @abstractmethod
    def __pow__(self, other, modulo=float('Inf')):
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
    
    @abstractmethod
    def __radd__(self, other):
        pass
    
    @abstractmethod
    def __rsub__(self, other):
        pass
    
    @abstractmethod
    def __rmul__(self, other):
        pass
    
    @abstractmethod
    def __rdiv__(self, other):
        pass
    
    @abstractmethod
    def __rmod__(self, other):
        pass
    
    @abstractmethod
    def __rdivmod__(self, other):
        pass
    
    @abstractmethod
    def __rpow__(self, other):
        pass
    
    @abstractmethod
    def __rlshift__(self, other):
        pass
    
    @abstractmethod
    def __rrshift__(self, other):
        pass
    
    @abstractmethod
    def __rand__(self, other):
        pass
    
    @abstractmethod
    def __rxor__(self, other):
        pass
    
    @abstractmethod
    def __ror__(self, other):
        pass
    
    @abstractmethod
    def __neg__(self):
        pass
    
    @abstractmethod
    def __pos__(self):
        pass
    
    @abstractmethod
    def __abs__(self):
        pass
    
    @abstractmethod
    def __invert__(self):
        pass
    
    @abstractmethod
    def __complex__(self):
        pass
    
    @abstractmethod
    def __int__(self):
        pass
    
    @abstractmethod
    def __long__(self):
        pass
    
    @abstractmethod
    def __float__(self):
        pass
    
    @abstractmethod
    def __oct__(self):
        pass
    
    @abstractmethod
    def __hex__(self):
        pass
    
    @abstractmethod
    def __coerce__(self, other):
        pass
    
class Num_T:
    MAX = 2**128 - 1
    MIN = -2**128
    STR = "num"

    val = 0
    
    def __init__(self, val):
        self.val = val

    @coerce
    def __add__(self, other):
        assert(isinstance(other, type(self)))

        val = self.val + other.val
        if val > self.MAX or val < self.MIN:
            raise Exceptions.any_user_error(
                    "Value", val, "out of bounds of the type",
                    STR, "which can store values from",
                    self.MIN, "to", self.MAX,".")
        return type(self)(val)
    
    @coerce
    def __radd__(self, other):
        return self + other

    def __str__(self):
        return str(self.val)

    def __repr__(self):
        return str(self.val)

class Int_T(Num_T):
    MAX =  2147483647
    MIN = -2147483648
    STR = "int"

    val = 0
