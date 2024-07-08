from ...Type import *
from ...Inductive import *
from ...Prelude import *


class List(Inductive):

    def __new__(cls, *args):
        if not args:
            return cls.nil
        head, *tail = args
        α = cls.__annotations__['cons'][0]
        if not isinstance(head, α):
            head = α(head)
        return cls.cons(head, cls(*tail))

    α = Type
    # `[]` is the empty list.
    nil = Self
    # If `a : α` and `l : List α`, then `cons a l`, or `a :: l`, is the list whose first element is `a` and with `l` as the rest of the list.
    cons: tuple[α, Self] = Self

    def __str__(self):
        args = []
        while self is not self.nil:
            head, self = self.args
            args.append(head)
        return '[%s]' % ", ".join(str(arg) for arg in args)
    
    def __len__(self):
        if self is self.nil:
            return int(Nat.zero)
        head, tail = self.args
        return int(Nat.succ(len(tail)))
