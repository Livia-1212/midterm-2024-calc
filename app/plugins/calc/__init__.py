from .calculator import Calculator
from app.commands import Command

# Command classes for calculator operations
class AddCommand(Command):
    def __init__(self, calculator, value):
        self.calculator = calculator
        self.value = value

    def execute(self):
        return self.calculator.add(self.value)

class SubtractCommand(Command):
    def __init__(self, calculator, value):
        self.calculator = calculator
        self.value = value

    def execute(self):
        return self.calculator.subtract(self.value)

class MultiplyCommand(Command):
    def __init__(self, calculator, value):
        self.calculator = calculator
        self.value = value

    def execute(self):
        return self.calculator.multiply(self.value)

class DivideCommand(Command):
    def __init__(self, calculator, value):
        self.calculator = calculator
        self.value = value

    def execute(self):
        if self.value == 0:
            print("Error: Division by zero")
            return None
        return self.calculator.divide(self.value)

def register_commands(command_handler, calculator):
    """Register calculator commands with the command handler."""
    command_handler.register_command("add", AddCommand(calculator, 0))
    command_handler.register_command("subtract", SubtractCommand(calculator, 0))
    command_handler.register_command("multiply", MultiplyCommand(calculator, 0))
    command_handler.register_command("divide", DivideCommand(calculator, 0))
