from app.commands import Command

class MedianCommand(Command):
    def __init__(self, calculator):
        self.calculator = calculator

    def execute(self):
        if not self.calculator.values:
            return "Error: No values to calculate median."
        sorted_values = sorted(self.calculator.values)
        n = len(sorted_values)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_values[mid - 1] + sorted_values[mid]) / 2
        else:
            return sorted_values[mid]

def register_commands(command_handler, calculator):
    """Register the median command."""
    command_handler.register_command("median", MedianCommand(calculator))
