"""Basic smoke tests for the main entry point."""
from unittest.mock import patch
from icarus_sentinel.main import main

@patch("icarus_sentinel.main.App")
def test_main_runs(mock_app):
    """Verifies that the main() function correctly initializes the App."""
    main()
    mock_app.assert_called_once()
    mock_app.return_value.mainloop.assert_called_once()
