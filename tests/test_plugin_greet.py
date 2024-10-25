
def test_greet_command_output(capsys, greet_command):
    """Test the GreetCommand output."""
    greet_command.execute()
    captured = capsys.readouterr()
    assert "Hello, this is a calculator with statistical operations!" in captured.out

def test_greet_command_logging(greet_command, caplog):
    """Test if GreetCommand logs the correct message."""
    with caplog.at_level("INFO"):
        greet_command.execute()
        assert "INFO" in caplog.text
        assert "Hello, this is a calculator with statistical operations!" in caplog.text
