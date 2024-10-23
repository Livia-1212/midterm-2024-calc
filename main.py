from app import App
from app.plugins.data import DataCommand

if __name__ == "__main__":
    app = App()
    app.start()
    app.command_handler.register_command("data", DataCommand())  # Register the DataCommand
    app.command_handler.execute_command("data")  # Execute the DataCommand


