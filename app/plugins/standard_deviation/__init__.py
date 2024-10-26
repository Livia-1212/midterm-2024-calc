import logging
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
        std_dev_rounded = round(std_dev, 2)  # Round to 2 decimal places

        print(f"📊 Standard Deviation: {std_dev_rounded}")
        return std_dev_rounded
