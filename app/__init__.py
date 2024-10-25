import os
import logging
import pandas as pd
from dotenv import load_dotenv
from app.commands import CommandHandler
from app.plugins.calc.calculator import Calculator
from app.plugins.calc import AddCommand, SubtractCommand, MultiplyCommand, DivideCommand
from app.plugins.data import DataCommand
from app.plugins.greet import GreetCommand
from app.plugins.mean import MeanCommand
from app.plugins.median import MedianCommand
from app.plugins.mode import ModeCommand
from app.plugins.standard_deviation import StandardDeviationCommand
from app.plugins.logging_config import configure_logging
from app.plugins.csv import CsvCommand

class App:
    def __init__(self):
        # Ensure logging is configured based on environment variables
        os.makedirs('logs', exist_ok=True)
        configure_logging()
        load_dotenv()

        # Load environment variables
        self.settings = self.load_environment_variables()
        self.settings.setdefault('ENVIRONMENT', 'PRODUCTION')

        # Initialize CommandHandler, Calculator, and history DataFrame
        self.command_handler = CommandHandler()
        self.calculator = Calculator()
        self.history = pd.DataFrame(columns=["Operation", "Value", "Result"])

        # Register all commands
        self.register_all_commands()

    def load_environment_variables(self):
        """Load environment variables into a dictionary."""
        settings = {key: value for key, value in os.environ.items()}
        logging.info("Environment variables loaded.")
        return settings

    def register_all_commands(self):
        """Register commands from all plugins."""
        # Register calculator commands
        self.command_handler.register_command("add", AddCommand(self.calculator, 0))
        self.command_handler.register_command("subtract", SubtractCommand(self.calculator, 0))
        self.command_handler.register_command("multiply", MultiplyCommand(self.calculator, 0))
        self.command_handler.register_command("divide", DivideCommand(self.calculator, 0))

        # Register statistical commands
        self.command_handler.register_command("mean", MeanCommand(self.calculator))
        self.command_handler.register_command("median", MedianCommand(self.calculator))
        self.command_handler.register_command("mode", ModeCommand(self.calculator))
        self.command_handler.register_command("standard_deviation", StandardDeviationCommand(self.calculator))

        # Register other commands
        self.command_handler.register_command("data", DataCommand(self.calculator))
        self.command_handler.register_command("greet", GreetCommand())
        self.command_handler.register_command("csv", CsvCommand(self.calculator))

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

        while True:
            try:
                command_input = input(">>> ").strip().lower()

                if command_input in ['exit', 'reset']:
                    self.handle_special_commands(command_input)
                    if command_input == 'exit':
                        break
                    continue

                parts = command_input.split()
                command_name = parts[0]

                if len(parts) < 2 and command_name not in [
                    "greet", "data", "mean", "median", "mode", "standard_deviation", "csv"]:
                    logging.warning("Invalid command format or missing value.")
                    print("❌ Error: Please enter a command followed by a value.")
                    continue

                value = float(parts[1]) if len(parts) > 1 else None

                if command_name in self.command_handler.commands:
                    if value is not None:
                        self.calculator.add_value(value)
                        self.command_handler.commands[command_name].value = value

                    result = self.command_handler.execute_command(command_name)

                    if result is not None:
                        self.update_history(command_name, value, result)

                        if command_name == "mean":
                            print(f"✅ The mean of the total scores from class 1 and class 2 is: {result}")
                        else:
                            print(f"✅ Result: {result}")
                else:
                    logging.error(f"Unknown command: {command_name}")
                    print(f"❌ Error: Unknown command '{command_name}'.")

            except Exception as e:
                logging.error(f"An unexpected error occurred: {e}")
                print(f"❌ An unexpected error occurred: {e}")

    def handle_special_commands(self, command_name):
        """Handle special commands like reset and exit."""
        if command_name == "reset":
            self.calculator.reset()
            logging.info("Calculator value reset to 0.")
            print("✅ Calculator value reset to 0. History remains intact.")
        elif command_name == "exit":
            self.save_history()

    def update_history(self, operation, value, result):
        """Update the operation history DataFrame."""
        new_entry = pd.DataFrame([{
            "Operation": operation,
            "Value": value,
            "Result": result
        }])

        if not new_entry.isna().all().all():
            self.history = pd.concat([self.history, new_entry], ignore_index=True)

    def save_history(self):
        """Save calculation history to a CSV file using Pandas."""
        csv_path = './data/grades_export.csv'

        # Use Pandas for efficient data writing
        self.history.to_csv(csv_path, index=False)

        logging.info(f"Grades saved to CSV at '{csv_path}'.")
        print(f"\n📁 Grades saved to '{csv_path}'.")

    def start(self):
        """Start the application."""
        logging.info("Application started. Type 'exit' to exit.")
        self.repl()
