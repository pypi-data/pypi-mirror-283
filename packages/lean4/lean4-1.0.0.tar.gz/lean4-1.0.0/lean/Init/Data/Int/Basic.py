from std import __set__
from ...Inductive import *
from ...Prelude import *
from ...Type import *


class Int(Inductive):

    def __new__(cls, n=0):
        assert isinstance(n, int)
        if n >= 0:
            return Int.ofNat(Nat(n))
        return Int.negSucc(Nat(-n))

    # A natural number is an integer (`0` to `∞`).
    ofNat: Nat = Self
    # The negation of the successor of a natural number is an integer (`-1` to `-∞`).
    negSucc: Nat = Self


@__set__(Int.ofNat)
def __str__(self):
    return str(self.arg)


@__set__(Int.negSucc)
def __str__(self):
    return '-' + str(self.arg)


__all__ = 'Int',