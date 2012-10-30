# -*- coding: utf-8 -*-
"""
The Whatever object inspired by Perl 6 one.

See http://perlcabal.org/syn/S02.html#The_Whatever_Object
"""
import operator, types

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
    def __init__(self, func, arity=None):
        self._func = func
        self._arity = arity

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)

    def __nonzero__(self):
        return False

    @property
    def __code__(self):
        return types.CodeType(
            self._arity,
            self._arity,
            0,
            0,
            '',
            (),
            (),
            (),
            '',
            'operator',
            0,
            '')


def unary(op):
    return lambda self: WhateverCode(op)

def code_unary(op):
    return lambda self: WhateverCode(lambda that: op(self(that)))


### Binary ops

def operand_type(value):
    return type(value) if isinstance(value, (Whatever, WhateverCode)) else None

def argcount(operand):
    op_type = operand_type(operand)
    if op_type is None:
        return 0
    elif op_type is Whatever:
        return 1
    else:
        return operand._arity

def compose_codes(op, left, right):
    la = left._arity
    return lambda *xs: op(left(*xs[:la]), right(*xs[la:]))

def gen_binary(op, left, right):
    W, C, D = Whatever, WhateverCode, None
    ops = {
        (W, D): lambda: lambda x: op(x, right),
        (D, W): lambda: lambda x: op(left, x),
        (C, D): lambda: lambda *xs: op(left(*xs), right),
        (D, C): lambda: lambda *xs: op(left, right(*xs)),
        (W, W): lambda: op,
        (W, C): lambda: lambda x, *ys: op(x, right(*ys)),
        (C, W): lambda: lambda *xs: op(left(*xs[:-1]), xs[-1]),
        (C, C): lambda: compose_codes(op, left, right),
    }
    types = operand_type(left), operand_type(right)
    if types not in ops:
        raise NotImplementedError
    arity = sum(map(argcount, [left, right]))
    return WhateverCode(ops[types](), arity=arity)

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
