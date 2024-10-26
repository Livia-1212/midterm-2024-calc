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
        """
        Execute a registered command using the command name and optional value.
        """
        command_name = command_name.lower()

        # Check if the command exists in the registry
        if command_name not in self.commands:
            print(f"Error: Command '{command_name}' not found.")
            return None

        command_class = self.commands[command_name]

        # Handle commands that do not require arguments
        if command_class.__name__ in ["GreetCommand", "ResetCommand"]:
            command = command_class()
        elif command_value is not None:
            command = command_class(self.calculator, command_value)
        else:
            command = command_class(self.calculator)

        # Execute the command and return the result
        try:
            return command.execute()
        except ValueError as ve:
            print(f"Value Error: {ve}")
        except Exception as e:
            print(f"Unexpected Error: {e}")
            return None
