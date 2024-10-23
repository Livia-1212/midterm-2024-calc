from app.commands import Command

class MeanCommand(Command):
    def __init__(self, calculator):
        self.calculator = calculator

    def execute(self):
        if not self.calculator.values:
            return "Error: No values to calculate mean."
        return sum(self.calculator.values) / len(self.calculator.values)

def register_commands(command_handler, calculator):
    """Register the mean command."""
    command_handler.register_command("mean", MeanCommand(calculator))
