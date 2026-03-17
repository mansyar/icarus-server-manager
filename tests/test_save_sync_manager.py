import os
import shutil
import pytest
from core.save_sync_manager import SaveSyncManager
from core.ini_manager import INIManager

@pytest.fixture
def mock_env(tmp_path, monkeypatch):
    local_appdata = tmp_path / "LocalAppData"
    local_appdata.mkdir()
    monkeypatch.setenv("LOCALAPPDATA", str(local_appdata))
    
    # Create local structure
    steam_root = local_appdata / "Icarus" / "Saved" / "PlayerData" / "Steam"
    steam_root.mkdir(parents=True)
    
    steam_id_dir = steam_root / "12345678"
    steam_id_dir.mkdir()
    
    local_prospects = steam_id_dir / "Prospects"
    local_prospects.mkdir()
    
    with open(local_prospects / "LocalSave.json", "w") as f:
        f.write('{"name": "Local"}')
        
    return tmp_path

@pytest.fixture
def sync_manager(mock_env):
    server_path = mock_env / "server"
    server_path.mkdir()
    
    # Create server structure
    server_prospects = server_path / "Icarus" / "Saved" / "PlayerData" / "DedicatedServer" / "Prospects"
    server_prospects.mkdir(parents=True)
    
    with open(server_prospects / "ServerSave.json", "w") as f:
        f.write('{"name": "Server"}')
        
    ini_path = server_path / "Icarus" / "Saved" / "Config" / "WindowsServer" / "ServerSettings.ini"
    ini_path.parent.mkdir(parents=True)
    ini_manager = INIManager(str(ini_path))
    
    return SaveSyncManager(server_path=str(server_path), ini_manager=ini_manager)

def test_list_steam_ids(sync_manager):
    ids = sync_manager.list_local_steam_ids()
    assert "12345678" in ids

def test_list_prospects(sync_manager):
    local_dir = sync_manager.get_local_prospects_dir("12345678")
    local_prospects = sync_manager.list_prospects(local_dir)
    assert "LocalSave" in local_prospects
    
    server_dir = sync_manager.get_server_prospects_dir()
    server_prospects = sync_manager.list_prospects(server_dir)
    assert "ServerSave" in server_prospects

def test_sync_to_server(sync_manager):
    success = sync_manager.sync_to_server("12345678", "LocalSave")
    assert success
    
    server_dir = sync_manager.get_server_prospects_dir()
    assert os.path.exists(os.path.join(server_dir, "LocalSave.json"))
    
    # Check INI update
    assert sync_manager.ini_manager.get_setting("LoadProspect") == "LocalSave"
    assert sync_manager.ini_manager.get_setting("ResumeProspect") == "True"

def test_sync_to_local(sync_manager):
    success = sync_manager.sync_to_local("12345678", "ServerSave")
    assert success
    
    local_dir = sync_manager.get_local_prospects_dir("12345678")
    assert os.path.exists(os.path.join(local_dir, "ServerSave.json"))
