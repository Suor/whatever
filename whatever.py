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
    return lambda self: WhateverCode(lambda that: op(that))

def binary(op):
    return lambda self, other: WhateverCode(lambda that: op(that, other))

def rbinary(op):
    return lambda self, other: WhateverCode(lambda that: op(other, that))

def code_unary(op):
    return lambda self: WhateverCode(lambda that: op(self(that)))

def code_binary(op):
    return lambda self, other: WhateverCode(lambda that: op(self(that), other))

def code_rbinary(op):
    return lambda self, other: WhateverCode(lambda that: op(other, self(that)))

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
        setattr(WhateverCode, name, code_binary(op))
        if reversible:
            setattr(Whatever, rname(name), rbinary(op))
            setattr(WhateverCode, rname(name), code_rbinary(op))

_ = that = Whatever()
