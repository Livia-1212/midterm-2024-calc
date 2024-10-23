from scipy import stats
from app.commands import Command

class ModeCommand(Command):
    def __init__(self, calculator):
        self.calculator = calculator

    def execute(self):
        if not self.calculator.values:
            print("⚠️ No values added yet. Cannot calculate mode.")
            return None
        mode_result = stats.mode(self.calculator.values, keepdims=True)
        mode_value = mode_result.mode[0]
        print(f"📊 Mode: {mode_value}")
        return mode_value

def register_commands(command_handler, calculator):
    command_handler.register_command("mode", ModeCommand(calculator))
