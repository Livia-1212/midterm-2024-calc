from app.commands import Command
from collections import Counter

class ModeCommand(Command):
    def __init__(self, calculator):
        self.calculator = calculator

    def execute(self):
        if not self.calculator.values:
            return "Error: No values to calculate mode."
        count = Counter(self.calculator.values)
        max_freq = max(count.values())
        modes = [num for num, freq in count.items() if freq == max_freq]
        if len(modes) == 1:
            return modes[0]
        return modes  # Return a list if there are multiple modes

def register_commands(command_handler, calculator):
    """Register the mode command."""
    command_handler.register_command("mode", ModeCommand(calculator))
