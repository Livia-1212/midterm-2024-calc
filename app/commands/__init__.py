from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class CommandHandler:
    def __init__(self):
        self.commands = {}

    def register_command(self, command_name, command):
        """Register a new command with the given name."""
        self.commands[command_name] = command

    def execute_command(self, command_name):
        """Execute a registered command by its name."""
        if command_name in self.commands:
            return self.commands[command_name].execute()
        else:
            print(f"Error: Command '{command_name}' not found.")
            return None
