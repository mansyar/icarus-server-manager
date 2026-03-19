import pytest
from unittest.mock import patch
from PySide6.QtWidgets import QLabel
from icarus_sentinel.ui.about_view import AboutView

@pytest.fixture
def mock_sys_info():
    with patch("icarus_sentinel.ui.about_view.get_app_version", return_value="1.2.3.4"), \
         patch("icarus_sentinel.ui.about_view.get_system_info", return_value={
             "os": "Windows 10",
             "ram": "16.0 GB",
             "cpu": "AMD64"
         }):
        yield

def test_about_view_initialization(qtbot, mock_sys_info):
    """Test that AboutView initializes with correct data."""
    view = AboutView()
    qtbot.addWidget(view)
    
    # Check if labels exist and contain expected text
    assert "Icarus Sentinel" in view.title_label.text()
    assert "1.2.3.4" in view.version_label.text()
    assert "Windows 10" in view.os_label.text()
    assert "16.0 GB" in view.ram_label.text()
    assert "AMD64" in view.cpu_label.text()
    assert "Icarus Sentinel Team" in view.credits_label.text()
