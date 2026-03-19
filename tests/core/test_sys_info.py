import pytest
from unittest.mock import patch, mock_open
from icarus_sentinel.core.sys_info import get_app_version, get_system_info

def test_get_app_version_success():
    """Test that app version is correctly parsed from version_info.txt."""
    mock_content = """
    StringStruct(u'ProductVersion', u'1.2.3.4')
    """
    with patch("builtins.open", mock_open(read_data=mock_content)):
        assert get_app_version() == "1.2.3.4"

def test_get_app_version_fallback():
    """Test that app version returns a fallback if file is missing or malformed."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        assert get_app_version() == "Unknown"

def test_get_system_info():
    """Test that system info returns expected keys and values."""
    with patch("platform.system", return_value="Windows"), \
         patch("platform.release", return_value="10"), \
         patch("psutil.virtual_memory") as mock_mem, \
         patch("platform.processor", return_value="AMD64"):
        
        mock_mem.return_value.total = 16 * 1024 * 1024 * 1024  # 16 GB
        
        info = get_system_info()
        
        assert info["os"] == "Windows 10"
        assert "16.0 GB" in info["ram"]
        assert info["cpu"] == "AMD64"
