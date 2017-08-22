import pytest
from whatever import _, that


def test_basic():
    assert _ is that


def test_caller():
    assert _(11)(lambda x: x ** 2) == 121
    assert _('100', base=11)(int) == 121


def test_attrs():
    assert callable(_.attr)

    class A(object):
        def __init__(self, name):
            self.name = name

    assert _.name(A('zebra')) == 'zebra'

    class B(object):
        def __getattr__(self, name):
            return name * 2

    b = B()
    assert _.foo(b) == 'foofoo'


def test_getitem():
    assert callable(_[0])
    assert _[0]([1, 2, 3]) == 1
    assert _[1:]([1, 2, 3]) == [2, 3]

    assert callable(_['item'])
    assert _['name']({'name': 'zebra'}) == 'zebra'


def test_add():
    # last and right
    assert (_ + 1)(10) == 11
    assert (1 + _)(10) == 11

    # non commutative
    assert (_ + 'y')('x') == 'xy'
    assert ('y' + _)('x') == 'yx'


def test_late_binding():
    assert (_ * 2)(2) == 4
    assert (_ * 2)('2') is NotImplemented


@pytest.mark.xfail
def test_overloaded():
    class StickyString(str):
        def __add__(self, other):
            if other is _:
                return NotImplemented
            return str(self) + str(other)

        def __radd__(self, other):
            if other is _:
                return NotImplemented
            return str(other) + str(self)

    foo = StickyString('foo')
    assert foo + 2 == 'foo2'
    assert (_ + 2)(foo) == 'foo2'
    assert (foo + _)(2) == 'foo2'
    assert (_ + foo)(2) == '2foo'


def test_comparison():
    assert callable(_ < 10)
    assert (_ < 10)(5) is (5 < 10)
    assert (_ < 10)(15) is (15 < 10)

    assert (_ == None)(None) is (None == None)
    assert (_ != None)(None) is (None != None)

    assert list(filter(5 < _, range(10))) == [6, 7, 8, 9]


def test_unary():
    assert callable(-_)
    assert callable(abs(_))

    assert (-_)(5) == -5
    assert abs(_)(-5) == 5
    assert min([2,3,5,6], key=-_) == 6


def test_chained_ops():
    assert callable(_ + 1 + 2)
    assert (_ + 1 + 2)(10) == 13

    assert (_ * 2 + 3)(1) == 5
    assert (_ + 2 * 3)(1) == 7

    assert (_ + 1 + 1 + 1 + 1 + 1)(0) == 5
    assert (_ + 1 + 1)(1) == 3
    assert (1 + _ + 1)(1) == 3
    assert (1 + (1 + _))(1) == 3

    assert ( _  + 'y' + 'z')('x') == 'xyz'
    assert ('x' +  _  + 'z')('y') == 'xyz'
    assert ('x' + 'y' +  _ )('z') == 'xyz'

    assert -abs(_)(-5) == -5
    assert abs(3 - _)(10) == 7


# NOTE: this is impossible since there is no boolean overloading in python
# def test_chained_comparison():
#     assert (1 < _ < 10)(7)
#     assert not (1 < _ < 10)(10)
#     assert not (1 < _ < 10)(1)


def test_chained_attrs():
    class A(object):
        def __init__(self, val):
            self.val = val

    assert callable(-that.val)
    assert (-that.val)(A(10)) == -10
    assert (that.val + 100)(A(10)) == 110

    assert ((_ + ', ' + 'Guys!').lower)('Hi')() == 'hi, guys!'
    assert that.val.val(A(A('a value'))) == 'a value'


def test_chained_getitem():
    assert callable(-that[0])
    assert callable(-that[2:])
    assert callable(that['key'] + 1)
    assert callable((_ + 1)['key'])

    assert (-_[0])([1,2,3]) == -1
    assert (_[1:] + [4])([1,2,3]) == [2,3,4]
    assert (_ + [4])[2:]([1,2,3]) == [3,4]

    assert (_['val'] * 5)({'val': 2}) == 10
    assert _['i']['j']({'i': {'j': 7}}) == 7


def test_higher_cardinality():
    assert (_ + _)(1, 2) == 3
    assert (_ + _ + 1)(1, 2) == 4
    assert (1 + (_ + _))(1, 2) == 4
    assert (_ ** _ ** _)(2, 3, 4) == 2 ** 3 ** 4
    assert ((_ ** _) ** _)(2, 3, 4) == (2 ** 3) ** 4
    assert (_ ** (_ ** _))(2, 3, 4) == 2 ** (3 ** 4)


def test_introspect_whatever():
    code = _.__code__
    assert code.co_argcount == 1
    assert len(code.co_varnames) == 1
    assert code.co_nlocals == 1


def test_introspection():
    assert (_ + 1).__code__.co_argcount == 1
    assert (_ + _).__code__.co_argcount == 2
    assert (_ + 1 + _).__code__.co_argcount == 2

    code = (_ + _).__code__
    assert 'add' in code.co_name
    assert len(code.co_varnames) == 2
    assert code.co_nlocals == 2


def test_code_to_code():
    assert (_ ** 2 + _ ** 2)(3, 4) == 5 ** 2


def test_contains():
    with pytest.raises(NotImplementedError): 1 in _
