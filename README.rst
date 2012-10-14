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

    squares = map(_ ** 2, range(100))
    three_digit_squares = filter(100 <= _ < 1000, squares)

    best = max(tries, key=_.score)
    sort(guys, key=-that.height)

    factorial = lambda n: reduce(_ * _, range(1, n))

Last example is not implemented yet.
