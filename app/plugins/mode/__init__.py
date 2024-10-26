# app/plugins/mode/__init__.py
import numpy as np
from app.commands import Command

class ModeCommand(Command):
    def __init__(self, calculator):
        self.calculator = calculator

    def execute(self):
        if not self.calculator.values:
            print("⚠️ No values added yet. Cannot calculate mode.")
            return None

        # Calculate mode using numpy
        mode_result = np.unique(self.calculator.values, return_counts=True)
        mode_values, counts = mode_result
        max_count = np.max(counts)
        modes = mode_values[counts == max_count]

        # Ensure the return is always a list
        return modes.tolist()

def register_commands(command_handler, calculator):
    command_handler.register_command("mode", ModeCommand(calculator))
