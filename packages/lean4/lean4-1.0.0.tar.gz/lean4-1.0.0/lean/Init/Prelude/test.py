from lean import *


class front(Function):
    α = Type
    def __new__(cls, xs : List[α]) -> Option[α]:
        if not xs:
            return Option[cls.α].none
        else:
            y, _ = xs.args
            return Option[cls.α].some(y)


print(front(List[Nat](2, 3, 5, 7)))
print(front(List[Nat]()))

A = (str @ (Int @ Nat) @ Int)("five", 5, 7, 0)
print(A)
B = (str @ Int @ (Nat @ Int))("five", 5, 7, 0)
print(B)

assert A == B
