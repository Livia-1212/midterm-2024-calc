import numpy as np
from app.commands import Command

class StandardDeviationCommand(Command):
    def __init__(self, calculator):
        self.calculator = calculator

    def execute(self):
        if not self.calculator.values:
            print("⚠️ No values added yet. Cannot calculate standard deviation.")
            return None
        std_dev = np.std(self.calculator.values)
        print(f"📊 Standard Deviation: {std_dev}")
        return std_dev

def register_commands(command_handler, calculator):
    command_handler.register_command("standard_deviation", StandardDeviationCommand(calculator))
