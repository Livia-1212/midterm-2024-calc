import numpy as np

def test_app_initialization(app_instance):
    """Test App initialization."""
    assert app_instance is not None
    assert app_instance.settings["ENVIRONMENT"] in ["DEVELOPMENT", "PRODUCTION"]

def test_command_registration(app_instance):
    """Test command registration in the App instance."""
    commands = app_instance.command_handler.commands
    assert "add" in commands
    assert "subtract" in commands
    assert "multiply" in commands
    assert "divide" in commands
    assert "mean" in commands
    assert "median" in commands
    assert "mode" in commands
    assert "standard_deviation" in commands
    assert "data" in commands
    assert "greet" in commands
    assert "csv" in commands

def test_calculator_operations(app_instance):
    """Test basic calculator operations."""
    app_instance.calculator.reset()
    assert app_instance.calculator.add(10) == 10
    assert app_instance.calculator.subtract(4) == 6
    assert app_instance.calculator.multiply(3) == 18
    assert app_instance.calculator.divide(2) == 9
    assert app_instance.calculator.divide(0) is None  # Test division by zero

def test_statistical_operations(app_instance):
    """Test statistical operations."""
    # Ensure the calculator's value list is cleared before starting
    app_instance.calculator.values = []

    # Add the test values
    app_instance.calculator.add_value(3)
    app_instance.calculator.add_value(4)
    app_instance.calculator.add_value(5)

    # Execute statistical commands
    mean_result = app_instance.command_handler.execute_command("mean")
    median_result = app_instance.command_handler.execute_command("median")
    mode_result = app_instance.command_handler.execute_command("mode")
    std_dev_result = app_instance.command_handler.execute_command("standard_deviation")

    # Assert results based on test values
    assert mean_result == 4, f"Expected mean to be 4, but got {mean_result}"
    assert median_result == 4, f"Expected median to be 4, but got {median_result}"

    # Convert mode_result to a list of floats for comparison
    if isinstance(mode_result, (np.ndarray, list)):
        mode_result = [float(x) for x in mode_result]
    elif isinstance(mode_result, (np.integer, int, np.floating, float)):
        mode_result = [float(mode_result)]  # Convert single value to list

    # Adjust mode assertion to check if mode_result is a subset of expected_mode
    expected_mode = [3.0, 4.0, 5.0]
    assert all(x in expected_mode for x in mode_result), (
        f"Expected mode to be a subset of {expected_mode}, but got {mode_result}"
    )

    # Assert standard deviation with rounding to avoid floating-point issues
    assert round(std_dev_result, 2) == 0.82, f"Expected standard deviation to be 0.82, but got {std_dev_result}"


def test_reset_command(app_instance):
    """Test reset command functionality."""
    app_instance.calculator.add(100)
    app_instance.handle_special_commands("reset")
    assert app_instance.calculator.value == 0

def test_csv_export(app_instance, tmpdir):
    """Test CSV export functionality."""
    csv_file = tmpdir.join("grades_export.csv")
    app_instance.history.to_csv(str(csv_file))
    assert csv_file.check(file=True)
    assert csv_file.size() > 0

def test_exit_command(app_instance):
    """Test exit command handling."""
    app_instance.handle_special_commands("exit")
    assert app_instance.history is not None
