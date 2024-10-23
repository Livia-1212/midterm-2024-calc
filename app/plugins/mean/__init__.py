import numpy as np
from app.commands import Command

class MeanCommand(Command):
    def __init__(self, calculator):
        self.calculator = calculator

    def execute(self):
        if not self.calculator.values:
            print("⚠️ No values added yet. Cannot calculate mean.")
            return None
        mean_value = np.mean(self.calculator.values)
        print(f"📊 Mean: {mean_value}")
        return mean_value

def register_commands(command_handler, calculator):
    command_handler.register_command("mean", MeanCommand(calculator))
