import os
import logging
import pandas as pd
from dotenv import load_dotenv
from app.commands import CommandHandler
from app.plugins.calc.calculator import Calculator
from app.plugins.calc import AddCommand, SubtractCommand, MultiplyCommand, DivideCommand
from app.plugins.reset import ResetCommand
from app.plugins.data import DataCommand
from app.plugins.greet import GreetCommand
from app.plugins.mean import MeanCommand
from app.plugins.median import MedianCommand
from app.plugins.mode import ModeCommand
from app.plugins.standard_deviation import StandardDeviationCommand
from app.plugins.logging_config import configure_logging
from app.plugins.csv import CsvCommand
import warnings


class App:
    def __init__(self):
        os.makedirs('logs', exist_ok=True)
        configure_logging()
        load_dotenv()

        # Load environment variables
        self.settings = self.load_environment_variables()
        self.settings.setdefault('ENVIRONMENT', 'PRODUCTION')

        # Initialize CommandHandler and Calculator
        self.calculator = Calculator()
        self.command_handler = CommandHandler(self.calculator)
        self.history = pd.DataFrame(columns=["Operation", "Value", "Result"])

        # Register all commands
        self.register_all_commands()

    def start(self):
        """Start the application."""
        logging.info("Application started. Type 'exit' to exit.")
        self.repl()  # Call the REPL method

    def load_environment_variables(self):
        """Load environment variables into a dictionary."""
        settings = {key: value for key, value in os.environ.items()}
        logging.info("Environment variables loaded.")
        return settings

    def register_all_commands(self):
        """Register and execute commands from all plugins."""
        self.command_handler.register_command("add", AddCommand)
        self.command_handler.register_command("subtract", SubtractCommand)
        self.command_handler.register_command("multiply", MultiplyCommand)
        self.command_handler.register_command("divide", DivideCommand)
        self.command_handler.register_command("mean", MeanCommand)
        self.command_handler.register_command("median", MedianCommand)
        self.command_handler.register_command("mode", ModeCommand)
        self.command_handler.register_command("standard_deviation", StandardDeviationCommand)
        self.command_handler.register_command("grades", DataCommand)
        self.command_handler.register_command("greet", GreetCommand)
        self.command_handler.register_command("csv", CsvCommand)
        self.command_handler.register_command("reset", ResetCommand(self.calculator))

        logging.info("All commands registered.")

    def repl(self):
        """Command-line REPL interface for interacting with the app."""
        instructions = (
            "\n🔢 Welcome to the Calculator REPL!"
            "\n\n📚 Available Operations:"
            "\n  - add <value>: Adds a value to the current total (e.g., 'add 5')."
            "\n  - subtract <value>: Subtracts a value from the current total (e.g., 'subtract 3')."
            "\n  - multiply <value>: Multiplies the current total by a value (e.g., 'multiply 4')."
            "\n  - divide <value>: Divides the current total by a value (e.g., 'divide 2')."
            "\n  - mean: Calculates the mean of entered grades."
            "\n  - median: Calculates the median of entered grades."
            "\n  - mode: Calculates the mode of entered grades."
            "\n  - standard_deviation: Calculates the standard deviation of entered grades."
            "\n  - grades: Enter grades for different categories (assignment, project, etc.)."
            "\n  - greet: Displays a greeting message."
            "\n  - csv: Exports collected grades to a CSV file."
            "\n  - reset: Resets the calculator value to 0 (history remains)."
            "\n  - exit: Exits the program and displays the summary."
            "\n\nℹ️ Type 'exit' to quit and view the summary at any time.\n"
        )

        print(instructions)

        # List of commands that do not require a value
        no_value_commands = ["mean", "median", "mode", "standard_deviation", "grades", "greet", "csv", "reset"]

        while True:
            try:
                command_input = input(">>> ").strip()

                # Exit command handling
                if command_input == 'exit' or command_input == 'reset':
                    self.handle_special_commands(command_input)
                    break

                # Split command input
                parts = command_input.split()
                command_name = parts[0]

                # Check if command is valid
                if command_name not in self.command_handler.commands:
                    print(f"❌ Error: Unknown command '{command_name}'.")
                    continue

                # Handle commands that do not require a value
                if command_name in no_value_commands:
                    result = self.command_handler.execute_command(command_name)
                else:
                    # Commands that require a value
                    if len(parts) < 2:
                        print("❌ Error: Please enter a command followed by a value.")
                        continue

                    try:
                        value = float(parts[1])
                    except ValueError:
                        print("❌ Error: Please enter a valid number.")
                        continue

                    # Set the value and execute the command
                    command = self.command_handler.commands[command_name](self.calculator, value)
                    result = command.execute()

                # Display the result
                if result is not None:
                    if isinstance(result, float):
                        result = round(result, 2)
                    print(f"✅ Result: {result}")

            except Exception as e:
                print(f"❌ An unexpected error occurred: {e}")

    def handle_special_commands(self, command_name):
        """Handle special commands like reset and exit."""
        if command_name == "reset":
            self.calculator.reset()
            logging.info("Calculator value reset to 0.")
            print("✅ Calculator value reset to 0. History remains intact.")
        elif command_name == "exit":
            self.save_history()
            logging.info("Exiting REPL.")
            print("\n👋 Exiting REPL. Calculator Summary:")
            print(self.history)
            import sys
            sys.exit()

    def save_history(self, file_path='./data/grades_export.csv'):
        """Save calculation history to a CSV file."""
        directory = os.path.dirname(file_path)

        # Ensure the directory exists
        if directory and not os.path.exists(directory):
            raise FileNotFoundError("Path to CSV file does not exist, please create the directory.")

        # Save the history if it exists
        if not self.history.empty:
            self.history.to_csv(file_path, index=False)
            logging.info(f"Grades saved to CSV at '{file_path}'.")
            print(f"\n📁 Grades saved to '{file_path}'.")
        elif self.calculator.values:
            # Save current calculator values if history is empty
            history_df = pd.DataFrame({
                "Operation": ["add"] * len(self.calculator.values),
                "Value": self.calculator.values,
                "Result": self.calculator.values
            })
            history_df.to_csv(file_path, index=False)
            logging.info(f"Calculator values saved to CSV at '{file_path}'.")
            print(f"\n📁 Calculator values saved to '{file_path}'.")
        else:
            print("No data to save. History and calculator values are empty.")
