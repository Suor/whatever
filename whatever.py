# -*- coding: utf-8 -*-
"""
The Whatever object inspired by Perl 6 one.

See http://perlcabal.org/syn/S02.html#The_Whatever_Object
"""
import operator

__ALL__ = ['_', 'that']

# TODO: or not to do
# object.__call__(self[, args...])

# TODO: pow with module arg:
# object.__pow__(self, other[, modulo])

# NOTE: Is this possible:
#     map(_.meth(1,2,3), objects)
# A problem that _.meth when called should return a "meth" attribute of it's caller
# not schedule call as here.
# NOTE: Maybe use some javascript-like syntax:
#       _.meth.call(1,2,3) # or
#       _.call('meth', 1,2,3)


class Whatever(object):
    pass

class WhateverCode(object):
    def __init__(self, func):
        self._func = func

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)


def unary(op):
    return lambda self: WhateverCode(op)

def code_unary(op):
    return lambda self: WhateverCode(lambda that: op(self(that)))


# Binary ops
# w + d => wc(lambda x: x + d)                   # binary
# d + w => wc(lambda x: d + x)                   # rbinary
# c + d => wc(lambda *xs: c(*xs) + d)            # code_binary
# d + c => wc(lambda *xs: d + c(*xs))            # code_rbinary
# w + w => wc(+)                                 # binary
# w + c => wc(lambda x, *ys: x + c(*ys))         # binary
# c + w => wc(lambda *xs, y: c(*xs) + y)         # code_binary
# c + c => wc(lambda *xs, *ys: c(*xs) + c(*ys))  # code_binary

def operand_type(value):
    return type(value) if isinstance(value, (Whatever, WhateverCode)) else None

def gen_binary(op, left, right):
    W, C, D = Whatever, WhateverCode, None
    ops = {
        (W, D): lambda x: op(x, right),
        (D, W): lambda x: op(left, x),
        (C, D): lambda *xs: op(left(*xs), right),
        (D, C): lambda *xs: op(left, right(*xs)),
        (W, W): op,
        (W, C): lambda x, *ys: op(x, right(*ys)),
        (C, W): lambda *xs: op(left(*xs[:-1]), xs[-1])
    }
    types = operand_type(left), operand_type(right)
    if types not in ops:
        raise NotImplementedError
    return WhateverCode(ops[types])

def binary(op):
    return lambda left, right: gen_binary(op, left, right)

def rbinary(op):
    return lambda left, right: gen_binary(op, right, left)


def rname(name):
    return name[:2] + 'r' + name[2:]

def op(name, func=None, args=2, reversible=False):
    return (name, func or getattr(operator, name), args, reversible)

def ops(names, args=2, reversible=False):
    return [op(name, args=args, reversible=reversible)
            for name in names]

OPS = ops(['__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__'])    \
    + ops(['__add__', '__sub__', '__mul__', '__floordiv__', '__mod__',     \
              '__lshift__', '__rshift__', '__and__', '__xor__', '__or__',  \
              '__div__', '__truediv__', '__pow__'], reversible=True)       \
    + [op('__cmp__', cmp), op('__divmod__', divmod, reversible=True)]      \
    + ops(['__neg__', '__pos__', '__abs__', '__invert__'], args=1)         \
    + [op('__getattr__', getattr), op('__getitem__')]

for name, op, args, reversible in OPS:
    # print name, op, args, reversible
    if args == 1:
        setattr(Whatever, name, unary(op))
        setattr(WhateverCode, name, code_unary(op))
    elif args == 2:
        setattr(Whatever, name, binary(op))
        setattr(WhateverCode, name, binary(op))
        if reversible:
            setattr(Whatever, rname(name), rbinary(op))
            setattr(WhateverCode, rname(name), rbinary(op))

_ = that = Whatever()
