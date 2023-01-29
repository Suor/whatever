# -*- coding: utf-8 -*-
"""
The Whatever object inspired by Perl 6 one.

See http://perlcabal.org/syn/S02.html#The_Whatever_Object
"""
import operator, sys
from types import CodeType

__all__ = ['_', 'that']
PY2 = sys.version_info[0] == 2
PY38 = sys.version_info[:2] >= (3, 8)
PY311 = sys.version_info[:2] >= (3, 11)


# TODO: or not to do
# object.__call__(self[, args...])

# TODO: pow with module arg:
# object.__pow__(self, other[, modulo])


def _make_code(arity, name, varnames):
    # Python 3 got kwonlyargcount, Python 3.8 got posonlyargcount
    args = [arity, arity] if PY2 else [arity, 0, 0, arity] if PY38 else [arity, 0, arity]
    args.extend([1, 67, b'', (), (), varnames, __name__, name])
    # Python 3.11 got qualname
    if PY311:
        args.append('%s.%s' % (__name__, name))
    args.extend([1, b''])
    # Python 3.11 got exceptiontable
    if PY311:
        args.append(b'')
    return CodeType(*args)


class Whatever(object):
    def __contains__(self, other):
        raise NotImplementedError('Sorry, can\'t to hook "in" operator in this way')

    @staticmethod
    def __call__(*args, **kwargs):
        return WhateverCode.make_call(lambda f: f(*args, **kwargs), 1)

    __code__ = _make_code(1, 'Whatever', ('f',))


class WhateverCode(object):
    def __init__(self, arity):
        self._arity = arity

    @classmethod
    def make_call(cls, func, arity):
        sub_cls = type('WhateverCodeCall', (WhateverCode,), {'__call__': staticmethod(func)})
        return sub_cls(arity)

    def __contains__(self, other):
        raise NotImplementedError('Sorry, can\'t hook "in" operator in this way')

    # Simulate normal callable
    @property
    def __code__(self):
        fname = self.__call__.__name__ or 'operator'
        varnames = tuple('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'[:self._arity])
        return _make_code(self._arity, fname, varnames)


### Unary ops

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

def gen_binary(op, left, right):
    W, C, D = Whatever, WhateverCode, None
    name, rname, func, args = op
    ltype, rtype = types = operand_type(left), operand_type(right)

    # Constant incorporating optimizations
    lfunc = rfunc = None
    if ltype is D:
        _lfunc = lambda x: func(left, x)
        lfunc = getattr(left, name, _lfunc) if name else _lfunc
    if rtype is D:
        if name == '__getattr__':
            assert isinstance(right, str)
            # NOTE: eval('lambda x: x.%s' % right) is even faster, but to slow to construct
            rfunc = operator.attrgetter(right)
        elif name == '__getitem__':
            rfunc = operator.itemgetter(right)
        else:
            _rfunc = lambda x: func(x, right)
            rfunc = getattr(right, rname, _rfunc) if rname else _rfunc

    # Resolve embedded __call__ in advance
    if ltype is C:
        lcall = left.__call__
    if rtype is C:
        rcall = right.__call__
    largs, rargs = argcount(left), argcount(right)

    ops = {
        (W, D): rfunc,
        (D, W): lfunc,
        # (C, D) are optimized for one argument variant
        (C, D): (lambda x: rfunc(lcall(x))) if largs == 1 else
                        (lambda *xs: rfunc(lcall(*xs))),
        (D, C): (lambda x: lfunc(rcall(x))) if rargs == 1 else
                        (lambda *xs: lfunc(rcall(*xs))),
        (W, W): func,
        (W, C): lambda x, *ys: func(x, rcall(*ys)),
        (C, W): lambda *xs: func(lcall(*xs[:-1]), xs[-1]),
        (C, C): lambda *xs: func(lcall(*xs[:largs]), rcall(*xs[largs:])),
    }
    return WhateverCode.make_call(ops[types], arity=largs + rargs)

def binary(op):
    return lambda left, right: gen_binary(op, left, right)

def rbinary(op):
    return lambda left, right: gen_binary(op, right, left)


### Define ops

def op(name, rname=None, func=None, args=2):
    name = '__%s__' % name
    if rname:
        rname = '__%s__' % rname
    return (name, rname, func or getattr(operator, name), args)

def rop(name, func=None):
    return op(name, 'r' + name, func=func, args=2)

def ops(names, args=2):
    return [op(name, args=args) for name in names]

def rops(names):
    return [rop(name) for name in names]


OPS = rops(['add', 'sub', 'mul', 'floordiv', 'truediv', 'mod', 'pow',
            'lshift', 'rshift', 'and', 'xor', 'or'])                       \
    + [rop('divmod', func=divmod)]                                         \
    + ops(['eq', 'ne', 'lt', 'le', 'gt', 'ge'])                            \
    + ops(['neg', 'pos', 'abs', 'invert'], args=1)                         \
    + [op('getattr', func=getattr), op('getitem')]

# This things were dropped in python 3
if PY2:
    OPS += [rop('div'), op('cmp', func=cmp)]  # noqa

for op in OPS:
    name, rname, func, args = op
    if args == 1:
        setattr(Whatever, name, unary(func))
        setattr(WhateverCode, name, code_unary(func))
    elif args == 2:
        setattr(Whatever, name, binary(op))
        setattr(WhateverCode, name, binary(op))
        if rname:
            setattr(Whatever, rname, rbinary(op))
            setattr(WhateverCode, rname, rbinary(op))

_ = that = Whatever()
