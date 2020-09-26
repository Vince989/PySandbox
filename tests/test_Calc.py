# -*- coding: utf-8 -*-
from ..Calc import Calc

calc = Calc()


# noinspection PyPep8Naming
def test_CalcParse():
    assert calc
    assert calc.parse("1 + 2") == "1+2"
    assert calc.parse("1+-2") == "1-2"
    assert calc.parse("1 +- 2") == "1-2"
    assert calc.parse("1--2") == "1+2"
    assert calc.parse("-1 - -2") == "-1+2"


# noinspection PyPep8Naming
def test_CalcEval():
    # TODO Bogus result, wtf to do ???  :P
    # assert calc.parse("1 + 1") == "1"

    # Actual test cases
    assert calc.eval("1 + 2") == "3"
    assert calc.eval("1 +- 1") == "0"
    assert calc.eval("-1 - -1") == "0"
    # ...
    # assert calc.eval("sqrt(4)") == "2" # TODO
    # assert calc.eval("1/0") == ERROR # TODO
