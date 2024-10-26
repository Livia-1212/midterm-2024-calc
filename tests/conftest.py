# tests/conftest.py
import pytest
from app import App
from app.plugins.greet import GreetCommand
from app.plugins.data import DataCommand
from app.plugins.mean import MeanCommand
from app.plugins.median import MedianCommand
from app.plugins.mode import ModeCommand
from app.plugins.reset import ResetCommand

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

@pytest.fixture
def mean_command(app_instance):
    """Fixture for the MeanCommand."""
    return MeanCommand(app_instance.calculator)

@pytest.fixture
def median_command(app_instance):
    """Fixture for the MedianCommand."""
    return MedianCommand(app_instance.calculator)

@pytest.fixture
def mode_command(app_instance):
    """Fixture for the ModeCommand."""
    return ModeCommand(app_instance.calculator)

@pytest.fixture
def reset_command(app_instance):
    """Fixture for the ResetCommand."""
    return ResetCommand(app_instance.calculator)
