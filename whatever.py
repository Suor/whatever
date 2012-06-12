# -*- coding: utf-8 -*-
"""
The Whatever object inspired by Perl 6 one.

See http://perlcabal.org/syn/S02.html#The_Whatever_Object
"""
import operator

# TODO:
# # vararg, no reverse
# object.__call__(self[, args...])

# # vararg with reverse

# # pow
# object.__pow__(self, other[, modulo])
# object.__rpow__(self, other)

# # unary
# object.__neg__(self)
# object.__pos__(self)
# object.__abs__(self)
# object.__invert__(self)


class Whatever(object):
    def __getattr__(self, name):
        return operator.attrgetter(name)

    def __getitem__(self, key):
        return operator.itemgetter(key)


def _binary(op):
    return lambda self, other: lambda that: op(that, other)

def _rbinary(op):
    return lambda self, other: lambda that: op(other, that)

for name in ['__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__']:
    op = getattr(operator, name)
    setattr(Whatever, name, _binary(op))

reversible = ['__add__', '__sub__', '__mul__', '__floordiv__', '__mod__',
              '__lshift__', '__rshift__', '__and__', '__xor__', '__or__',
              '__div__', '__truediv__']
for name in reversible:
    op = getattr(operator, name)
    rname = name[:2] + 'r' + name[2:]
    setattr(Whatever, name, _binary(op))
    setattr(Whatever, rname, _rbinary(op))

# TODO: __cmp__ __divmod__ with cmp() and divmod() funcs


_ = that = Whatever()
