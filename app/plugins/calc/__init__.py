# app/plugins/calc/__init__.py

from app.commands import Command


class AddCommand(Command):
    def __init__(self, calculator, value=0):
        self.calculator = calculator
        self.value = value

    def execute(self):
        self.calculator.add_value(self.value)
        return self.calculator.value


class SubtractCommand(Command):
    def __init__(self, calculator, value=0):
        self.calculator = calculator
        self.value = value

    def execute(self):
        self.calculator.subtract_value(self.value)
        return self.calculator.value


class MultiplyCommand(Command):
    def __init__(self, calculator, value=0):
        self.calculator = calculator
        self.value = value

    def execute(self):
        self.calculator.multiply_value(self.value)
        return self.calculator.value


class DivideCommand(Command):
    def __init__(self, calculator, value=0):
        self.calculator = calculator
        self.value = value

    def execute(self):
        result = self.calculator.divide_value(self.value)
        if result == "Error: Division by zero":
            return result
        return self.calculator.value

