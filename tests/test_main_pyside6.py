import pytest
from unittest.mock import MagicMock, patch
import sys

@patch("icarus_sentinel.main.QApplication")
@patch("icarus_sentinel.main.MainWindow")
@patch("icarus_sentinel.main.QSplashScreen")
@patch("icarus_sentinel.main.QPixmap")
@patch("icarus_sentinel.main.Qt")
def test_main_with_splash_screen(mock_qt, mock_pixmap, mock_splash, mock_window, mock_app):
    """Verifies that the main() function shows a splash screen."""
    from icarus_sentinel.main import main
    
    # We need to mock sys.exit to avoid stopping the test
    with patch("sys.exit") as mock_exit:
        main()
        
    mock_app.assert_called_once()
    mock_splash.assert_called_once()
    mock_splash.return_value.show.assert_called_once()
    mock_window.assert_called_once()
    mock_splash.return_value.finish.assert_called_once_with(mock_window.return_value)
