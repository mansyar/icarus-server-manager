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

def test_bundle_release():
    """Verify that bundle_release.py correctly creates a ZIP archive."""
    import sys
    sys.path.append(".")
    import bundle_release
    import zipfile
    
    # Mock os.path.exists to simulate presence of dist/IcarusSentinel.exe and README.md
    with patch("os.path.exists") as mock_exists:
        mock_exists.side_effect = lambda p: p in [os.path.join("dist", "IcarusSentinel.exe"), "README.md"]
        
        # Mock zipfile.ZipFile
        with patch("zipfile.ZipFile") as mock_zip:
            bundle_release.bundle()
            
            mock_zip.assert_called_once()
            args, kwargs = mock_zip.call_args
            assert args[0] == "IcarusSentinel.zip"
            
            # Check if write was called for both files
            instance = mock_zip.return_value.__enter__.return_value
            assert instance.write.call_count == 2
            
            # Verify file names passed to write
            called_files = [call.args[0] for call in instance.write.call_args_list]
            assert os.path.join("dist", "IcarusSentinel.exe") in called_files
            assert "README.md" in called_files
