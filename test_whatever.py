from whatever import _, that


def test_basic():
    assert _ is that
    assert callable(_.name)


def test_attributes():
    class A(object):
        def __init__(self, name):
            self.name = name

    assert _.name(A('zebra')) == 'zebra'

    class B(object):
        def __getattr__(self, name):
            return name * 2

    b = B()
    assert _.foo(b) == 'foofoo'


def test_add():
    # last and right
    assert (_ + 1)(10) == 11
    assert (1 + _)(10) == 11

    # non commutative
    assert (_ + 'y')('x') == 'xy'
    assert ('y' + _)('x') == 'yx'

    # overloaded
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

    assert filter(5 < _, range(10)) == [6, 7, 8, 9]


def test_unary():
    assert callable(-_)
    assert callable(abs(_))

    assert (-_)(5) == -5
    assert abs(_)(-5) == 5
    assert min([2,3,5,6], key=-_) == 6

