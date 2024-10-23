class Calculator:
    def __init__(self):
        self.value = 0
        self.values = []

    def add(self, value):
        self.value += value
        self.values.append(value)
        return self.value

    def subtract(self, value):
        self.value -= value
        return self.value

    def multiply(self, value):
        self.value *= value
        return self.value

    def divide(self, value):
        if value == 0:
            print("Error: Division by zero")
            return None
        self.value /= value
        return self.value

    def reset(self):
        self.value = 0
        return self.value

    def add_value(self, value):
        """Add value for statistical calculations."""
        self.values.append(value)
