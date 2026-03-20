import pytest
from unittest.mock import patch
import sys
import os

def test_build_includes_icon_flag():
    """Verifies that the build script includes the --icon flag for PyInstaller."""
    sys.path.append(".")
    import build_exe
    
    with patch("PyInstaller.__main__.run") as mock_run:
        build_exe.build()
        
        # Get the arguments passed to PyInstaller
        args = mock_run.call_args[0][0]
        
        # Check if --icon is present
        # We need to consider both the flag and its value
        icon_flag = "--icon=assets/app_icon.png"
        assert any(arg == icon_flag or arg == "--icon" for arg in args), f"Icon flag '{icon_flag}' should be in PyInstaller arguments."
        
        if "--icon" in args:
            idx = args.index("--icon")
            assert args[idx+1] == "assets/app_icon.png"
