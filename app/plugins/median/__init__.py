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
        median_value = round(median_value, 2)  # Round to 2 decimal places
        print(f"📊 Median: {median_value}")
        return median_value
