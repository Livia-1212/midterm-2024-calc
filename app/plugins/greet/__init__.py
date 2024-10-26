# app/plugins/greet/__init__.py

import logging
from app.commands import Command


class GreetCommand(Command):
    def execute(self):
        # Logging information to guide the user
        logging.info("Welcome! You can start by entering data for 'class1' or 'class2' using the 'grades' command.")
        
        # Example instruction for the user
        instructions = (
            "\n📚 Instructions:"
            "\n1. Use the 'grades' command to add grades for different classes."
            "\n2. For example:"
            "\n   - Enter 'grades class1' to add grades for class1."
            "\n   - Enter 'grades class2' to add grades for class2."
            "\n3. After entering grades, you can calculate mean, median, mode, or standard deviation."
        )
        
        # Print the instructions to the console
        print("Hello! This is a calculator with statistical operations.")
        print(instructions)
