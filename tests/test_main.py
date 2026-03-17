"""Basic smoke tests for the main entry point."""
from src.main import main

def test_main_runs(capsys):
    """Verifies that the main() function prints the expected output."""
    main()
    captured = capsys.readouterr()
    assert "Hello from Icarus Server Manager!" in captured.out
