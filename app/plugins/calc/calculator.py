# app/plugins/calc/calculator.py

class Calculator:
    def __init__(self):
        self.value = 0
        self.values = []  # Initialize an empty list to store grades

    def add_value(self, num):
        """
        Add a value to the current total and to the list of values.
        """
        self.value += num
        self.values.append(num)

    def subtract_value(self, num):
        """
        Subtract a value from the current total.
        """
        self.value -= num

    def multiply_value(self, num):
        """
        Multiply the current total by a given number.
        """
        self.value *= num

    def divide_value(self, num):
        """
        Divide the current total by a given number.
        """
        if num == 0:
            return "Error: Division by zero"
        self.value /= num

    def reset(self):
        """
        Reset the calculator's value and clear stored values.
        """
        self.value = 0
        self.values.clear()
