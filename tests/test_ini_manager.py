"""Unit tests for the INIManager class."""

import pytest
import os
from icarus_sentinel.core.ini_manager import INIManager

@pytest.fixture
def ini_file(tmp_path):
    path = tmp_path / "ServerSettings.ini"
    content = """[/Script/IcarusServer.IcarusServerSettings]
SessionName=TestServer
ServerPassword=secret
AdminPassword=admin123
Port=17777
QueryPort=27015
"""
    path.write_text(content)
    return path

@pytest.fixture
def manager(ini_file):
    return INIManager(str(ini_file))

def test_load_settings(manager):
    assert manager.get_setting("SessionName") == "TestServer"
    assert manager.get_setting("ServerPassword") == "secret"
    assert manager.get_setting("AdminPassword") == "admin123"
    assert manager.get_setting("Port") == "17777"

def test_set_and_save_settings(manager, ini_file):
    manager.set_setting("SessionName", "NewName")
    manager.set_setting("Port", "18888")
    manager.save()
    
    with open(str(ini_file), "r") as f:
        content = f.read()
    
    assert "SessionName=NewName" in content
    assert "Port=18888" in content
    assert "ServerPassword=secret" in content # Ensure unmanaged settings are preserved

def test_get_raw_text(manager, ini_file):
    raw_text = manager.get_raw_text()
    assert "SessionName=TestServer" in raw_text
    assert "[/Script/IcarusServer.IcarusServerSettings]" in raw_text

def test_save_raw_text(manager, ini_file):
    new_raw_content = "[/Script/IcarusServer.IcarusServerSettings]\nSessionName=RawEdited\n"
    manager.save_raw_text(new_raw_content)
    
    # Reload to verify
    manager.load()
    assert manager.get_setting("SessionName") == "RawEdited"
    
    with open(str(ini_file), "r") as f:
        assert f.read() == new_raw_content

def test_missing_file_handled(tmp_path):
    missing_path = tmp_path / "nonexistent.ini"
    manager = INIManager(str(missing_path))
    # Should not raise, just have empty/default settings
    assert manager.get_setting("SessionName") is None

def test_update_on_launch_setting(manager):
    # This might be in a different section or even a different file, 
    # but for now let's assume it's managed by INIManager if we want it persisted.
    # The spec says "Update Checkbox ... within this Configuration tab".
    # It might be in a separate app_settings.json, but the spec says "INI Synchronization" 
    # and mentions "ServerSettings.ini" specifically for Req 3.2.
    # Req 1.3 says "Update on Launch" checkbox.
    # Let's assume for now it's in a [Sentinel] section or similar if we use INI.
    manager.set_setting("UpdateOnLaunch", "True", section="Sentinel")
    assert manager.get_setting("UpdateOnLaunch", section="Sentinel") == "True"
