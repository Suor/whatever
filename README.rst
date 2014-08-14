The Whatever Object
===================

An easy way to make lambdas by partial application of python operators.

Inspired by Perl 6 one, see http://perlcabal.org/syn/S02.html#The_Whatever_Object


Usage
-----

.. code:: python

    from whatever import _, that

    # get a list of guys names
    names = map(_.name, guys)
    names = map(that.name, guys)

    odd = map(_ * 2 + 1, range(10))

    squares = map(_ ** 2, range(100))
    small_squares = filter(_ < 100, squares)

    best = max(tries, key=_.score)
    sort(guys, key=-that.height)

    factorial = lambda n: reduce(_ * _, range(2, n+1))

NOTE: chained comparisons cannot be implemented since there is no boolean overloading in python.


CAVEATS
-------

In some special cases whatever can cause confusion:

.. code:: python

    _.attr # this makes callable
    obj._  # this fetches '_' attribute of obj

    _[key] # this works too
    d[_]   # KeyError, most probably

    _._    # short for attrgetter('_')
    _[_]   # short for lambda d, k: d[k]

    if _ == 'Any value':
        # You will get here, definitely
        # `_ == something` produces callable, which is true

    [1, 2, _ * 2, None].index('hi') # => 2, since bool(_ * 2 == 'hi') is True


Also, whatever sometimes fails on late binding:

.. code:: python

    (_ * 2)('2') # -> NotImplemented
