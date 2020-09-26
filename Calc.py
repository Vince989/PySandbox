# -*- coding: utf-8 -*-
class Calc(object):
    @staticmethod
    def parse(formula):
        formula = str.replace(formula, " ", "")
        formula = str.replace(formula, "+-", "-")
        formula = str.replace(formula, "--", "+")
        return formula

    @staticmethod
    def eval(formula):
        # Clean it up first...
        formula = Calc.parse(formula)

        # TODO Handle sqrt() ? -> ^0.5

        # TODO ( ) -> eval() the sub-formula

        # TODO ., ^ */ +-

        while formula.find("+", 1) > -1:
            splits = formula.split("+", maxsplit=1)
            splits[0] = Calc.eval(splits[0])
            splits[1] = Calc.eval(splits[1])
            formula = str(splits[0] + splits[1])

        # No more tokens, return the value
        return float(formula)
