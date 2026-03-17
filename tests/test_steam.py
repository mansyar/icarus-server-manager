import pytest
import os
import shutil
from unittest.mock import patch, MagicMock
from steam_manager import SteamManager

@pytest.fixture
def steam_manager(tmp_path):
    return SteamManager(root_dir=str(tmp_path))

def test_steam_manager_init(steam_manager, tmp_path):
    assert steam_manager.root_dir == str(tmp_path)
    assert steam_manager.steamcmd_path == os.path.join(str(tmp_path), "steamcmd", "steamcmd.exe")

@patch("urllib.request.urlretrieve")
@patch("zipfile.ZipFile")
@patch("os.remove")
def test_download_steamcmd(mock_remove, mock_zip, mock_urlretrieve, steam_manager):
    # Setup
    mock_zip_instance = mock_zip.return_value.__enter__.return_value
    
    # Execute
    steam_manager.download_steamcmd()
    
    # Verify
    mock_urlretrieve.assert_called_once()
    mock_zip.assert_called_once()
    mock_zip_instance.extractall.assert_called_once()
    mock_remove.assert_called_once()
