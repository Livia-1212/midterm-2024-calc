# app/plugins/reset/__init__.py

from app.commands import Command

class ResetCommand(Command):
    def __init__(self, calculator):
        self.calculator = calculator

    def execute(self):
        """Reset the calculator's value to 0."""
        self.calculator.reset()
        return 0  # Return 0 after reset
