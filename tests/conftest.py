# tests/conftest.py
import pytest
from app import App
from app.plugins.greet import GreetCommand
from app.plugins.data import DataCommand

@pytest.fixture(scope="module")
def app_instance():
    """Fixture to create an App instance for testing."""
    return App()

@pytest.fixture
def greet_command():
    """Fixture for the GreetCommand."""
    return GreetCommand()

@pytest.fixture
def data_command(app_instance):
    """Fixture for the DataCommand."""
    return DataCommand(app_instance.calculator)
