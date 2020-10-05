# -*- coding: utf-8 -*-
from ..Calc import Calc

calc = Calc()


def test_calc_parse():
    assert calc
    assert calc.parse("16 +  32") == "16+32"
    assert calc.parse("  ") == ""

    if calc.no_subs:
        assert calc.parse("16 + -32") == "16+-32"
        assert calc.parse("-16 + -32") == "-16+-32"

        assert calc.parse("16--32") == "16+32"
        assert calc.parse("16--32--64") == "16+32+64"
        assert calc.parse("16 - -32") == "16+32"
        assert calc.parse("16 - -32 -  -64") == "16+32+64"
        assert calc.parse("-16 - -4") == "-16+4"
        assert calc.parse("-16 - -4 -  -2") == "-16+4+2"

        assert calc.parse("64  - 16") == "64+-16"
        assert calc.parse("-64  - 16") == "-64+-16"

    assert calc.parse("10 * -2") == "10*-2"
    assert calc.parse("10 / -2") == "10/-2"


def test_calc_eval_base():
    # TODO Bogus result from the specs, wtf to do ???  :P
    # assert calc.parse("1 + 1") == 1

    # Additions
    assert calc.eval("1 + 2") == 3
    assert calc.eval("+1 + 2") == 3
    assert calc.eval("1 + 2 + 4") == 7
    assert calc.eval("-1 + 2") == 1
    assert calc.eval("-1+2 + 4+8") == 13

    # "Subtractions", which are worked around
    assert calc.eval("1 + -1") == 0
    assert calc.eval("-1 - -1") == 0
    assert calc.eval("8 + -4 + -1") == 3
    assert calc.eval("5-4") == 1
    assert calc.eval("-5-4") == -9
    assert calc.eval("8 - 4 + 2") == 6
    assert calc.eval("8 + 4 - 2") == 10

    # Multiplications
    assert calc.eval("5*2") == 10
    assert calc.eval("5 * -2") == -10
    assert calc.eval("2+2*5+5") == 17

    # TODO Fix rounding issues?
    # assert calc.eval("2.8*3-1") == 7.4
    assert calc.eval("2.8*3-1") == 2.8*3-1  # 7.39999...

    # Divisions
    assert calc.eval("10/2") == 5
    assert calc.eval("10/2 + 2") == 7
    assert calc.eval("2 + 10/2") == 7


def test_calc_eval_more():
    # Priorities
    assert calc.eval("(2+5)*3") == 21
    assert calc.eval("2*(5+3)") == 16

    # Exponents
    assert calc.eval("2^8") == 256
    assert calc.eval("2^8*5-1") == 1279

    # "DLC" cases
    # assert calc.eval("sqrt(4)") == "2" # TODO
    # assert calc.eval("1/0") == ERROR
