# -*- coding: utf-8 -*-
class Calc(object):
    @staticmethod
    def parse(formula):
        formula = str.replace(formula, " ", "")
        formula = str.replace(formula, "+-", "-")
        formula = str.replace(formula, "--", "+")
        # TODO Handle when it starts with -
        return formula

    @staticmethod
    def eval(formula):
        # Clean it up first...
        formula = Calc.parse(formula)

        # TODO Handle sqrt() ? -> ^0.5

        # TODO ( )

        # TODO ., ^ */ +-

        return formula

    pass
