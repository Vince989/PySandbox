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
    assert calc.eval("1 + 2") == 3.0
    assert calc.eval("1 + 2 + 4") == 7.0
    assert calc.eval("-1 + 2") == 1.0
    assert calc.eval("1 +- 1") == "0"
    assert calc.eval("-1 - -1") == "0"
    assert calc.eval("5-4") == "1"
    assert calc.eval("5*2") == "10"
    assert calc.eval("(2+5)*3") == "21"
    assert calc.eval("10/2") == "5"
    assert calc.eval("2+2*5+5") == "17"
    assert calc.eval("2.8*3-1") == "7.4"
    assert calc.eval("2^8") == "256"
    assert calc.eval("2^8*5-1") == "1279"

    # "DLC" cases
    # assert calc.eval("sqrt(4)") == "2" # TODO
    # assert calc.eval("1/0") == ERROR # TODO
