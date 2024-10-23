import numpy as np
from app.commands import Command

class MedianCommand(Command):
    def __init__(self, calculator):
        self.calculator = calculator

    def execute(self):
        if not self.calculator.values:
            print("⚠️ No values added yet. Cannot calculate median.")
            return None
        median_value = np.median(self.calculator.values)
        print(f"📊 Median: {median_value}")
        return median_value

def register_commands(command_handler, calculator):
    command_handler.register_command("median", MedianCommand(calculator))
