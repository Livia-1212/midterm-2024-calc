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
        mean_value = round(mean_value, 2)  # Round to 2 decimal places
        print(f"📊 Mean: {mean_value}")
        return mean_value
