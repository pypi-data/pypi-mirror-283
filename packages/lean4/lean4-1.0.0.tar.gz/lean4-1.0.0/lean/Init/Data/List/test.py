from lean import *


class length(Function):
    α = Type
    def __new__(cls, xs : List[α]) -> Nat:
        if xs is List[cls.α].nil:
            return Nat.zero
        else:
            y, ys = xs.args
            return Nat.succ(length[cls.α](ys))


print(length(List[Nat](2, 3, 5, 7)))
print(len(List[Nat](2, 3, 5, 7)))
print(not List[Nat](2, 3, 5, 7))

