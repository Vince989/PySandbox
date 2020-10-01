# -*- coding: utf-8 -*-
class Calc(object):
    # Subtraction avoidance flag, causes subtractions
    # to be replaced by negative additions instead
    no_subs = True

    @staticmethod
    def parse(formula: str) -> str:
        # TODO Assert that there are as many  ('s  as  )'s

        formula = str.replace(formula, " ", "")

        if Calc.no_subs:
            formula = str.replace(formula, "+-", "-")
            formula = str.replace(formula, "--", "+")

            # Swap -'s for +- instead,
            # then remove leading + if now present
            formula = str.replace(formula, "-", "+-")
            if formula[0] == "+":
                formula = formula[1:]

            # Remove "garbage" added from previous step
            formula = str.replace(formula, "*+-", "*-")
            formula = str.replace(formula, "/+-", "/-")

        return formula

    # noinspection PyTypeChecker,PyUnresolvedReferences
    @staticmethod
    def eval(formula: str) -> float:
        # Clean it up first...
        formula = Calc.parse(formula)

        # TODO Handle sqrt() ? -> ^0.5

        # TODO For ( ) -> eval() the sub-formula

        # TODO ^

        # Handle the additions, and negative additions
        if formula.find("+", 1) > -1:
            parts = formula.split("+", maxsplit=1)
            parts[0] = Calc.eval(parts[0])
            parts[1] = Calc.eval(parts[1])
            formula = str(parts[0] + parts[1])

        # Handle the multiplications and divisions
        if formula.find("*", 1) > -1:
            parts = formula.split("*", maxsplit=1)
            parts[0] = Calc.eval(parts[0])
            parts[1] = Calc.eval(parts[1])
            formula = str(parts[0] * parts[1])

        if formula.find("/", 1) > -1:
            parts = formula.split("/", maxsplit=1)
            parts[0] = Calc.eval(parts[0])
            parts[1] = Calc.eval(parts[1])
            formula = str(parts[0] / parts[1])

        # No more tokens, return the value
        return float(formula)
