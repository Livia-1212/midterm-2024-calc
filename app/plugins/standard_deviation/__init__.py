from app.commands import Command
import math

class StandardDeviationCommand(Command):
    def __init__(self, calculator):
        self.calculator = calculator

    def execute(self):
        if not self.calculator.values:
            return "Error: No values to calculate standard deviation."
        mean = sum(self.calculator.values) / len(self.calculator.values)
        variance = sum((x - mean) ** 2 for x in self.calculator.values) / len(self.calculator.values)
        return math.sqrt(variance)

def register_commands(command_handler, calculator):
    """Register the standard deviation command."""
    command_handler.register_command("standard_deviation", StandardDeviationCommand(calculator))
