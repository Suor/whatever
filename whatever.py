# -*- coding: utf-8 -*-
"""
The Whatever object inspired by Perl 6 one.

See http://perlcabal.org/syn/S02.html#The_Whatever_Object
"""
import operator

__ALL__ = ['_', 'that']

# TODO:
# # vararg, no reverse
# object.__call__(self[, args...])

# TODO: pow with module arg:
# object.__pow__(self, other[, modulo])

class Whatever(object):
    def __getattr__(self, name):
        return operator.attrgetter(name)

    def __getitem__(self, key):
        return operator.itemgetter(key)


def unary(op):
    return lambda self: lambda that: op(that)

def binary(op):
    return lambda self, other: lambda that: op(that, other)

def rbinary(op):
    return lambda self, other: lambda that: op(other, that)

def rname(name):
    return name[:2] + 'r' + name[2:]

def op(name, func=None, args=2, reversible=False):
    return (name, func or getattr(operator, name), args, reversible)

def ops(names, args=2, reversible=False):
    return [op(name, args=args, reversible=reversible)
            for name in names]

OPS = ops(['__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__'])    \
    + ops(['__add__', '__sub__', '__mul__', '__floordiv__', '__mod__',     \
              '__lshift__', '__rshift__', '__and__', '__xor__', '__or__',   \
              '__div__', '__truediv__', '__pow__'], reversible=True)        \
    + [op('__cmp__', cmp), op('__divmod__', divmod, reversible=True)]     \
    + ops(['__neg__', '__pos__', '__abs__', '__invert__'], args=1)

for name, op, args, reversible in OPS:
    if args == 1:
        setattr(Whatever, name, unary(op))
    elif args == 2:
        setattr(Whatever, name, binary(op))
        if reversible:
            setattr(Whatever, rname(name), rbinary(op))

_ = that = Whatever()
