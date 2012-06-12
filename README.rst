Whatever
========

Usage
-----

::

    from whatever import _, that

    # get a list of guys names
    names = map(_.name, guys)
    names = map(that.name, guys)

    squares = map(_ ** 2, range(100))
    three_digit_squares = filter(_ < 1000, squares)

    best = max(tries, key=_.score)
    sort(guys, key=-that.height)

    factorial = lambda n: reduce(_ * _, range(1, n))

Last two examples are not implemented yet.
