# -*- coding: utf-8 -*-
"""
The Whatever object inspired by Perl 6 one.

See http://perlcabal.org/syn/S02.html#The_Whatever_Object
"""
import operator, types, sys

__all__ = ['_', 'that']
_py_version = sys.version_info[0]


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
    def __contains__(self, other):
        raise NotImplementedError('Sorry, can\'t to hook "in" operator in this way')


class WhateverCode(object):
    def __init__(self, arity):
        self._arity = arity

    @classmethod
    def make_call(cls, func, arity):
        sub_cls = type('WhateverCodeCall', (WhateverCode,), {'__call__': staticmethod(func)})
        return sub_cls(arity)

    def __nonzero__(self):
        return False

    def __contains__(self, other):
        raise NotImplementedError('Sorry, can\'t hook "in" operator in this way')

    @property
    def __code__(self):
        # Add co_kwonlyargcount for Python 3
        args = ((self._arity, self._arity) if _py_version == 2 else (self._arity, 0, self._arity)) \
             + (0, 0, b'', (), (), (), '', 'operator', 0, b'')
        return types.CodeType(*args)


def unary(op):
    return lambda self: WhateverCode.make_call(op, 1)

def code_unary(op):
    return lambda self: WhateverCode.make_call(lambda that: op(self(that)), self._arity)


### Binary ops

def operand_type(value):
    return Whatever     if isinstance(value, Whatever) else     \
           WhateverCode if isinstance(value, WhateverCode) else \
           None

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
    arity = argcount(left) + argcount(right)
    return WhateverCode.make_call(ops[types](), arity=arity)

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
              '__truediv__', '__pow__'], reversible=True)                  \
    + [op('__divmod__', divmod, reversible=True)]                          \
    + ops(['__neg__', '__pos__', '__abs__', '__invert__'], args=1)         \
    + [op('__getattr__', getattr), op('__getitem__')]


# OMG what about py1
if _py_version == 2:
    OPS += [op('__div__', reversible=True), op('__cmp__', cmp)]
elif _py_version == 3:
    OPS += [op('__floordiv__', reversible=True)]

for name, op, args, reversible in OPS:
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
