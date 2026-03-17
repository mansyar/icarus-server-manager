import pytest
import os
import shutil
from unittest.mock import patch, MagicMock
from icarus_sentinel.steam_manager import SteamManager

@pytest.fixture
def steam_manager(tmp_path):
    return SteamManager(root_dir=str(tmp_path))

def test_steam_manager_init(steam_manager, tmp_path):
    assert steam_manager.root_dir == str(tmp_path)
    assert steam_manager.steamcmd_path == os.path.join(str(tmp_path), "steamcmd", "steamcmd.exe")

@patch("os.path.exists")
@patch("urllib.request.urlretrieve")
@patch("zipfile.ZipFile")
@patch("os.remove")
@patch("os.makedirs")
def test_download_steamcmd(mock_makedirs, mock_remove, mock_zip, mock_urlretrieve, mock_exists, steam_manager):
    # Setup: simulate that zip exists for removal, but dir doesn't exist for makedirs
    mock_exists.side_effect = lambda path: path.endswith("steamcmd.zip")
    mock_zip_instance = mock_zip.return_value.__enter__.return_value
    
    # Execute
    steam_manager.download_steamcmd()
    
    # Verify
    mock_urlretrieve.assert_called_once()
    mock_zip.assert_called_once()
    mock_zip_instance.extractall.assert_called_once()
    mock_remove.assert_called_once()

@patch("subprocess.Popen")
def test_install_server(mock_popen, steam_manager, tmp_path):
    # Setup
    with patch.object(SteamManager, "is_installed", return_value=True):
        mock_process = MagicMock()
        mock_popen.return_value = mock_process
        
        install_dir = os.path.join(str(tmp_path), "icarus_server")
        
        # Execute
        steam_manager.install_server(install_dir)
        
        # Verify
        mock_popen.assert_called_once()
        args, kwargs = mock_popen.call_args
        cmd = args[0]
        assert steam_manager.steamcmd_path in cmd
        assert "+force_install_dir" in cmd
        assert install_dir in cmd
        assert "2089300" in cmd
