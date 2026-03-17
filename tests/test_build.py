import os
import subprocess
import pytest
from unittest.mock import patch

def test_build_function_calls_pyinstaller():
    """Verify that build() calls PyInstaller with expected arguments."""
    import sys
    sys.path.append(".")
    import build_exe
    with patch("PyInstaller.__main__.run") as mock_run:
        build_exe.build()
        mock_run.assert_called_once()
        args = mock_run.call_args[0][0]
        assert "--onefile" in args
        assert "--windowed" in args
        assert "--version-file=version_info.txt" in args
        assert "IcarusSentinel" in " ".join(args)

def test_pyinstaller_installed():
    """Verify that pyinstaller is installed and accessible."""
    try:
        subprocess.run(["pyinstaller", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        pytest.fail("PyInstaller is not installed or not in PATH.")

def test_build_script_exists():
    """Verify that the build script exists."""
    assert os.path.exists("build_exe.py"), "build_exe.py script does not exist."

def test_build_includes_data_files():
    """Verify that build() includes the necessary data files."""
    import sys
    sys.path.append(".")
    import build_exe
    with patch("PyInstaller.__main__.run") as mock_run:
        build_exe.build()
        args = mock_run.call_args[0][0]
        # Check for server_state.json
        data_args = [a for a in args if a.startswith("--add-data")]
        assert any("server_state.json" in a for a in data_args)
