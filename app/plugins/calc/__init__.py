import os
import pkgutil
import importlib
import logging
import pandas as pd  # For history management
from dotenv import load_dotenv
from app.commands import CommandHandler
from app.plugins.calc import Calculator
from app.plugins.logging_config import configure_logging
from app.plugins.data import DataCommand
from app.plugins.greet import GreetCommand
from app.plugins.calc import AddCommand, SubtractCommand, MultiplyCommand, DivideCommand

class App:
    def __init__(self):
        os.makedirs('logs', exist_ok=True)
        configure_logging()
        load_dotenv()
        self.settings = self.load_environment_variables()
        self.settings.setdefault('ENVIRONMENT', 'PRODUCTION')
        self.command_handler = CommandHandler()
        self.calculator = Calculator()
        self.history = pd.DataFrame(columns=["Operation", "Value", "Result"])  # Initialize empty DataFrame

        # Register commands from all plugins
        self.register_all_commands()

    def load_environment_variables(self):
        """Load environment variables into a dictionary."""
        settings = {key: value for key, value in os.environ.items()}
        logging.info("Environment variables loaded.")
        return settings
    
    def load_plugins(self):
        """Dynamically load all plugins from the app.plugins package."""
        plugins_package = 'app.plugins'
        plugins_path = plugins_package.replace('.', '/')
        if not os.path.exists(plugins_path):
            logging.warning(f"Plugins directory '{plugins_path}' not found.")
            return

        for _, plugin_name, is_pkg in pkgutil.iter_modules([plugins_path]):
            if is_pkg:
                try:
                    plugin_module = importlib.import_module(f'{plugins_package}.{plugin_name}')
                    self.register_plugin_commands(plugin_module, plugin_name)
                except ImportError as e:
                    logging.error(f"Error importing plugin {plugin_name}: {e}")



    def register_all_commands(self):
        """Register and execute commands from all plugins."""
        # Register DataCommand
        self.command_handler.register_command("data", DataCommand())
        logging.info("DataCommand registered.")

        # Register GreetCommand
        self.command_handler.register_command("greet", GreetCommand())
        logging.info("GreetCommand registered.")

        # Register Calculator Commands
        self.command_handler.register_command("add", AddCommand(self.calculator, 0))
        self.command_handler.register_command("subtract", SubtractCommand(self.calculator, 0))
        self.command_handler.register_command("multiply", MultiplyCommand(self.calculator, 0))
        self.command_handler.register_command("divide", DivideCommand(self.calculator, 0))
        logging.info("Calculator commands registered.")

        # Execute commands for testing purposes (optional)
        self.command_handler.execute_command("greet")  # Execute GreetCommand
        self.command_handler.execute_command("data")   # Execute DataCommand

    def repl(self):
        """Command-line REPL interface for interacting with the app."""
        operations = {
            'add': 'Add a value',
            'subtract': 'Subtract a value',
            'multiply': 'Multiply by a value',
            'divide': 'Divide by a value',
            'mean': 'Calculate mean',
            'median': 'Calculate median',
            'mode': 'Calculate mode',
            'standard_deviation': 'Calculate standard deviation',
            'greet': 'Greet the user',
            'data': 'Show data structure examples',
            'reset': 'Reset the calculator value to 0 (history remains)'  # Include reset command
        }

        # Display initial welcome message and instructions
        print("\n🔢 Welcome to the Calculator REPL!")
        print("📚 Available Operations:")
        for command, description in operations.items():
            print(f"  - {command}: {description}")
        print("\nℹ️  Example: To add 5, type 'add 5'.")
        print("ℹ️  Use 'reset' to restart the calculation but keep the log history.")
        print("Type 'exit' to quit and view the summary.\n")

        while True:
            try:
                command_input = input(">>> ").strip().lower()

                if command_input == 'exit':
                    self.save_history()  # Save history before exiting
                    calc_summary = {
                        'History': self.history.to_dict(orient='records'),
                        'Final Value': self.calculator.value,
                        'Operations': list(operations.keys())
                    }
                    print("\n👋 Exiting REPL. Calculator Summary:")
                    print(self.history)
                    break

                # Split command and value (e.g., "add 5")
                parts = command_input.split()
                command_name = parts[0]

                if command_name == "reset":
                    self.calculator.reset()  # Reset calculator value
                    print("✅ Calculator value reset to 0. History remains intact.")
                    continue

                if len(parts) < 2 and command_name not in ["greet", "data"]:
                    print("❌ Error: Please enter a command followed by a value.")
                    continue

                value = float(parts[1]) if len(parts) > 1 else None

                if command_name in self.command_handler.commands:
                    if value is not None:
                        self.calculator.add_value(value)  # Store value for statistics
                        self.command_handler.commands[command_name].value = value
                    result = self.command_handler.execute_command(command_name)

                    if result is not None:
                        # Update history DataFrame
                        new_entry = pd.DataFrame([{
                            "Operation": command_name,
                            "Value": value,
                            "Result": result
                        }])
                        self.history = pd.concat([self.history, new_entry], ignore_index=True)
                        print(f"✅ Result: {result}")
                else:
                    print(f"❌ Error: Unknown command '{command_name}'.")

            except Exception as e:
                print(f"❌ An unexpected error occurred: {e}")

    def save_history(self):
        """Save calculation history to a CSV file."""
        csv_path = "./data/calculation_history.csv"
        self.history.to_csv(csv_path, index=False)
        print(f"\n📁 Calculation history saved to '{csv_path}'.")

    def start(self):
        """Start the application."""
        self.load_plugins()
        logging.info("Application started. Type 'exit' to exit.")
        self.repl()
