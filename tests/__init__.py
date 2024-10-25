import subprocess
import pytest

def pytest_sessionstart(session):
    """Runs at the start of the pytest session."""
    # Run Pylint checks for code quality
    result = subprocess.run(
        ["pylint", "app", "commands", "tests"], capture_output=True, text=True, check=False
    )

    if result.returncode != 0:
        print("\n❌ Pylint found issues. Check the output above for details.")
        print(result.stdout)  # Display the Pylint output
    else:
        print("\n✅ Pylint checks passed.")

def pytest_sessionfinish(session, exitstatus):
    """Runs at the end of the pytest session."""
    if exitstatus == 0:
        print("\n✅ All tests passed successfully.")
    else:
        print("\n❌ Some tests failed. Check the output above for details.")
