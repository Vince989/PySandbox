# -*- coding: utf-8 -*-
class Calc(object):
    # Subtraction avoidance flag, causes subtractions
    # to be replaced by negative additions instead
    no_subs = True

    @staticmethod
    def parse(formula: str) -> str:
        # TODO Assert that there are as many  ('s  as  )'s

        formula = str.replace(formula, " ", "")

        if formula:  # if formula is now empty, skip the rest
            formula = str.replace(formula, "--", "+")

            # Do we work around subtractions
            # by doing negative-additions instead?
            if Calc.no_subs:
                # Start by changing all +- signs to -
                formula = str.replace(formula, "+-", "-")

                # Then swap -'s for +- instead,
                # and remove leading + if now present
                formula = str.replace(formula, "-", "+-")
                if formula[0] == "+":
                    formula = formula[1:]

                # Finally, remove "garbage" added from previous step
                formula = str.replace(formula, "*+-", "*-")
                formula = str.replace(formula, "/+-", "/-")

        return formula

    # noinspection PyTypeChecker,PyUnresolvedReferences
    @staticmethod
    def eval(formula: str) -> float:
        # Clean it up first...
        formula = Calc.parse(formula)

        # TODO Handle sqrt() ? -> ^0.5

        # For ( ) -> eval() the sub-formula
        # TODO Improve parsing it can support more than one ( ) combo
        if formula.find("(") > -1:
            opening = formula.split("(", maxsplit=1)
            closing = opening[1].split(")", maxsplit=1)
            closing[0] = Calc.eval(closing[0])
            formula = opening[0] + str(closing[0]) + closing[1]

        # TODO ^

        # Handle the additions, and negative additions
        if formula.find("+", 1) > -1:
            parts = formula.split("+", maxsplit=1)
            parts[0] = Calc.eval(parts[0])
            parts[1] = Calc.eval(parts[1])
            formula = str(parts[0] + parts[1])

        # Handle the multiplications and divisions
        if formula.find("*") > -1:
            parts = formula.split("*", maxsplit=1)
            parts[0] = Calc.eval(parts[0])
            parts[1] = Calc.eval(parts[1])
            formula = str(parts[0] * parts[1])

        if formula.find("/") > -1:
            parts = formula.split("/", maxsplit=1)
            parts[0] = Calc.eval(parts[0])
            parts[1] = Calc.eval(parts[1])
            formula = str(parts[0] / parts[1])

        # No more tokens, return the value
        return float(formula)


if __name__ == "__main__":
    ans = "1"
    while ans:
        ans = input("Hello! What do want to calculate? (Empty line to exit) ")
        if ans:
            print(Calc.eval(ans))
    else:
        print("Bye bye!")
