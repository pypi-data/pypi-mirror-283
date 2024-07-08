from std import __set__
from sympy.core.sympify import sympify, converter
from sympy.core.symbol import dtype
from sympy import NonnegativeIntegers
from ..Inductive import *
from ..Type import *


class Nat(Inductive):

    def __new__(cls, n=0):
        assert isinstance(n, int)
        if not n:
            return Nat.zero
        assert n > 0
        return Nat.succ(n - 1)

    zero = Self
    succ: Self = Self

    def __str__(self):
        return str(int(self))


@__set__(Nat.succ)
def __new__(cls, *args):
    self = object.__new__(cls)
    self.args = args
    # assert isinstance(arg, cls)
    return self


@__set__(Nat.zero.__class__)
def __int__(self):
    return 0


@__set__(Nat.succ)
def __int__(self):
    n = self.arg
    if not isinstance(n, int):
        n = int(n)
    return n + 1


@__set__(Nat.zero.__class__)
def __lt__(self, other):
    return isinstance(other, Nat.succ)


@__set__(Nat.succ)
def __lt__(self, other):
    if isinstance(other, Nat.succ):
        return self.arg < other.arg
    return False


@__set__(Nat)
@staticmethod
def copy(**kwargs):
    return Nat


Nat.is_nonnegative = Nat.is_integer = Nat.is_rational = Nat.is_real = Nat.is_complex = True

Nat.is_negative = False

Nat.is_zero = Nat.is_extended_positive = None

Nat.is_Range = Nat.is_Interval = True

Nat.start = 0

Nat.etype = dtype.integer(negative=False)

converter[Nat.succ] = lambda val: sympify(int(str(val)))

converter[Nat.zero.__class__] = lambda val: sympify(0)

converter[Nat.__class__] = lambda val: NonnegativeIntegers


__all__ = 'Nat',