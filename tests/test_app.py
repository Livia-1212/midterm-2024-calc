import logging
import os
import sys
from unittest.mock import patch
import numpy as np
import pandas as pd
import pytest
from app import App
from app.commands import Command



@pytest.fixture(scope="module")
def app_instance():
    """Fixture to create an App instance for testing."""
    return App()


# App Initialization and Commands Registration
def test_app_initialization(app_instance):
    """Test App initialization and command registration."""
    assert app_instance.calculator is not None, "Calculator not initialized."
    assert app_instance.command_handler is not None, "CommandHandler not initialized."
    assert 'ENVIRONMENT' in app_instance.settings, "ENVIRONMENT not in settings."
    expected_commands = [
        "add", "subtract", "multiply", "divide",
        "mean", "median", "mode", "standard_deviation",
        "grades", "greet", "csv", "reset"
    ]
    for command in expected_commands:
        assert command in app_instance.command_handler.commands, f"'{command}' not registered."


# REPL and Special Commands
def test_repl_add_command(app_instance, monkeypatch, capsys):
    """Test REPL 'add' command."""
    inputs = iter(["add 10", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):
        app_instance.repl()

    captured = capsys.readouterr()
    assert "✅ Result: 10" in captured.out, "REPL did not handle 'add' command correctly."


def test_handle_special_commands(app_instance):
    """Test special commands 'reset' and 'exit'."""
    app_instance.calculator.value = 100
    app_instance.handle_special_commands("reset")
    assert app_instance.calculator.value == 0, "Calculator not reset."
    with patch.object(sys, 'exit', side_effect=SystemExit):
        with pytest.raises(SystemExit):
            app_instance.handle_special_commands("exit")


# Command Execution Tests
@pytest.mark.parametrize("command, initial, expected", [
    ("add 15", 0, 15),
    ("subtract 5", 20, 15),
    ("multiply 2", 10, 20),
    ("divide 4", 20, 5)
])
def test_calculator_commands(app_instance, command, initial, expected):
    """Test calculator commands (add, subtract, multiply, divide)."""
    app_instance.calculator.value = initial

    # Split command to separate name and value
    parts = command.split()
    command_name = parts[0]
    command_value = float(parts[1])

    # Execute command with the extracted value
    app_instance.command_handler.execute_command(command_name, command_value)

    # Check if the calculator value matches the expected result
    assert app_instance.calculator.value == expected, f"Command '{command}' failed."

def test_division_by_zero(app_instance):
    """Test division by zero."""
    app_instance.calculator.value = 10
    result = app_instance.command_handler.execute_command("divide", 0)
    assert result == "Error: Division by zero", "Division by zero error not raised."



def test_mean_command(app_instance):
    """Test MeanCommand."""
    app_instance.calculator.values = [10, 20, 30]
    mean = app_instance.command_handler.execute_command("mean")
    assert mean == 20, "Mean command failed."


def test_median_command(app_instance):
    """Test MedianCommand."""
    app_instance.calculator.values = [10, 30, 20]
    median = app_instance.command_handler.execute_command("median")
    assert median == 20, "Median command failed."


def test_mode_command(app_instance):
    """Test ModeCommand."""
    app_instance.calculator.values = [5, 5, 10, 10, 20]
    mode = app_instance.command_handler.execute_command("mode")

    # Ensure mode is a list before sorting
    mode = [mode] if isinstance(mode, (int, np.integer)) else mode
    assert sorted(mode) == [5, 10], "Mode command failed."


def test_standard_deviation_command(app_instance):
    """Test StandardDeviationCommand."""
    app_instance.calculator.values = [10, 20, 30, 40, 50]
    std_dev = app_instance.command_handler.execute_command("standard_deviation")
    expected_std_dev = 14.14  # Pre-calculated expected value
    assert round(std_dev, 2) == expected_std_dev, "Standard Deviation command failed."


def test_save_history_no_directory(app_instance):
    """Test saving history when the directory doesn't exist."""
    invalid_path = './non_existent_dir/test_history_export.csv'

    # Ensure the directory does not exist
    if os.path.exists('./non_existent_dir'):
        os.rmdir('./non_existent_dir')

    # Expect FileNotFoundError when attempting to save
    with pytest.raises(FileNotFoundError, match="Path to CSV file does not exist"):
        app_instance.save_history(file_path=invalid_path)


def test_save_calculator_values(app_instance, tmp_path):
    """Test saving calculator values to CSV when history is empty."""
    app_instance.calculator.values = [10, 20, 30]
    csv_file_path = tmp_path / "test_calc_values_export.csv"
    app_instance.save_history(file_path=str(csv_file_path))
    df = pd.read_csv(csv_file_path)
    assert df['Result'].tolist() == [10, 20, 30], "Calculator values not saved correctly."


def test_greet_command(app_instance, capsys, caplog):
    """Test GreetCommand output."""
    with caplog.at_level(logging.INFO):
        app_instance.command_handler.execute_command("greet")
    
    # Capture printed output
    captured = capsys.readouterr()

    expected_print_output = "Hello! This is a calculator with statistical operations.\n"

    # Check if the printed output contains the greeting message
    assert expected_print_output in captured.out, "Greet command printed output mismatch."
    
    # Check if the log message matches
    expected_log_message = (
        "Welcome! You can start by entering data for 'class1' or 'class2' using the 'grades' command."
    )
    assert expected_log_message in caplog.text, "Greet command log message mismatch."


def test_repl_invalid_command(app_instance, capsys, monkeypatch):
    """Test REPL handling of an invalid command."""
    inputs = iter(["invalid_command", "exit"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):
        app_instance.repl()

    captured = capsys.readouterr()
    assert "❌ Error: Unknown command 'invalid_command'." in captured.out, (
        "REPL did not handle unrecognized commands correctly."
    )


def test_execute_dummy_command(app_instance):
    """Test successful execution of a dummy command."""
    class DummyCommand(Command):
        """Dummy command for testing."""
        def __init__(self, calculator=None, value=None):
            self.calculator = calculator
            self.value = value

        def execute(self):
            return f"Executed with value: {self.value}"

    # Register and execute the DummyCommand
    app_instance.command_handler.register_command("dummy", DummyCommand)
    result = app_instance.command_handler.execute_command("dummy 42")
    assert result == "Executed with value: 42.0", "Dummy command execution failed."

def test_load_environment_variables(app_instance, monkeypatch):
    """Test loading of environment variables."""
    # Mock the environment variables
    monkeypatch.setenv('ENVIRONMENT', 'DEVELOPMENT')
    monkeypatch.setenv('LOG_LEVEL', 'DEBUG')

    # Load the environment variables in the app instance
    env_vars = app_instance.load_environment_variables()

    # Check if 'ENVIRONMENT' is loaded correctly
    assert 'ENVIRONMENT' in env_vars, "ENVIRONMENT variable not loaded."
    assert env_vars.get('ENVIRONMENT') == 'DEVELOPMENT', "ENVIRONMENT not set to 'DEVELOPMENT'."
    
    # Check if 'LOG_LEVEL' is loaded correctly
    assert env_vars.get('LOG_LEVEL') == 'DEBUG', "LOG_LEVEL not set to 'DEBUG'."



def dummy_command():
    return "dummy"

def test_command_registration(app_instance):
    """Test registering the same command twice."""
    command_name = "test_command"

    app_instance.command_handler.register_command(command_name, dummy_command)
    app_instance.command_handler.register_command(command_name, dummy_command)

    assert command_name in app_instance.command_handler.commands, "Command not registered."



def test_calculator_addition(app_instance):
    """Test addition in the calculator."""
    app_instance.calculator.value = 10
    app_instance.calculator.add_value(5)
    assert app_instance.calculator.value == 15, "Addition failed."

def test_calculator_subtraction(app_instance):
    """Test subtraction in the calculator."""
    app_instance.calculator.value = 20
    app_instance.calculator.subtract_value(5)
    assert app_instance.calculator.value == 15, "Subtraction failed."
