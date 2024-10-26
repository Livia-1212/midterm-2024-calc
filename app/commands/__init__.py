from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class CommandHandler:
    def __init__(self, calculator=None):
        self.commands = {}
        self.calculator = calculator  # Initialize with a calculator instance

    def register_command(self, command_name, command_class):
        """
        Register a new command with a name and class.
        """
        if not command_name or not isinstance(command_name, str) or not command_class:
            raise ValueError("Invalid command name or command class.")
        
        self.commands[command_name.lower()] = command_class  # Use lowercase for consistency

    def execute_command(self, command_name, command_value=None):
        """Execute a registered command by its name and optional value."""
        if command_name not in self.commands:
            print(f"Error: Command '{command_name}' not found.")
            return None

        # Get the command class
        command_class = self.commands[command_name]

        # Create and execute the command
        if command_value is not None:
            command = command_class(self.calculator, command_value)
        else:
            command = command_class(self.calculator)

        return command.execute()

