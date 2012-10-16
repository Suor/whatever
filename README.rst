The Whatever Object
===================

An easy way to make lambdas by partial application of python operators.

Inspired by Perl 6 one, see http://perlcabal.org/syn/S02.html#The_Whatever_Object

Usage
-----

::

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
