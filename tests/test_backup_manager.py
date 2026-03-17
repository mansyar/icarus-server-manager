import pytest
from unittest.mock import MagicMock, patch
import time
from backup_manager import BackupManager

@pytest.fixture
def backup_manager(tmp_path):
    server_path = tmp_path / "server"
    backup_path = tmp_path / "backups"
    server_path.mkdir()
    backup_path.mkdir()
    
    # Create a dummy Prospects folder
    prospects_path = server_path / "Icarus" / "Saved" / "PlayerData" / "DedicatedServer" / "Prospects"
    prospects_path.mkdir(parents=True)
    
    return BackupManager(
        server_path=str(server_path),
        backup_path=str(backup_path),
        interval_minutes=30,
        retention_limit=5
    )

def test_manual_backup_trigger(backup_manager):
    # Mock the zipping function to avoid actual filesystem operations in this test
    with patch.object(backup_manager, "_perform_backup") as mock_backup:
        backup_manager.create_backup()
        mock_backup.assert_called_once()

def test_timer_trigger_logic(backup_manager):
    # We want to test that the timer eventually calls _perform_backup
    # Since we don't want to wait 30 minutes, we'll mock the interval and use a faster one or mock the timer
    backup_manager.interval_minutes = 0.001 # Very short interval for testing
    
    with patch.object(backup_manager, "_perform_backup") as mock_backup:
        backup_manager.start_timer()
        # Wait a bit for the timer to trigger
        time.sleep(0.1)
        backup_manager.stop_timer()
        
        assert mock_backup.called

def test_on_server_stop_trigger(backup_manager):
    with patch.object(backup_manager, "_perform_backup") as mock_backup:
        backup_manager.on_server_stop()
        mock_backup.assert_called_once()

def test_perform_backup_creates_zip(backup_manager):
    # Add a dummy file to Prospects
    prospects_path = os.path.join(backup_manager.server_path, "Icarus", "Saved", "PlayerData", "DedicatedServer", "Prospects")
    test_file = os.path.join(prospects_path, "test_save.txt")
    with open(test_file, "w") as f:
        f.write("test data")
        
    backup_manager._perform_backup()
    
    # Check if a zip file was created in backup_path
    backups = os.listdir(backup_manager.backup_path)
    assert len(backups) == 1
    assert backups[0].endswith(".zip")
    assert "Prospects_" in backups[0]

def test_perform_backup_missing_prospects(backup_manager, tmp_path):
    # Set server_path to a non-existent directory or one without Prospects
    backup_manager.server_path = str(tmp_path / "empty_server")
    os.mkdir(backup_manager.server_path)
    
    # Should not raise exception, just not create backup
    backup_manager._perform_backup()
    
    backups = os.listdir(backup_manager.backup_path)
    assert len(backups) == 0

def test_enforce_retention_deletes_oldest(backup_manager):
    # Create 5 dummy backup files with different timestamps
    backup_manager.retention_limit = 3
    
    # Files are sorted by name/timestamp, so older names are older files
    files = [
        "Prospects_2026-03-17_1000.zip",
        "Prospects_2026-03-17_1100.zip",
        "Prospects_2026-03-17_1200.zip",
        "Prospects_2026-03-17_1300.zip",
        "Prospects_2026-03-17_1400.zip",
    ]
    
    for f in files:
        with open(os.path.join(backup_manager.backup_path, f), "w") as f_obj:
            f_obj.write("dummy")
            
    backup_manager._enforce_retention()
    
    remaining = sorted(os.listdir(backup_manager.backup_path))
    assert len(remaining) == 3
    # Should keep the 3 newest (1200, 1300, 1400)
    assert "Prospects_2026-03-17_1000.zip" not in remaining
    assert "Prospects_2026-03-17_1100.zip" not in remaining
    assert "Prospects_2026-03-17_1200.zip" in remaining
    assert "Prospects_2026-03-17_1300.zip" in remaining
    assert "Prospects_2026-03-17_1400.zip" in remaining

def test_enforce_retention_ignores_other_files(backup_manager):
    backup_manager.retention_limit = 1
    
    with open(os.path.join(backup_manager.backup_path, "Prospects_2026-03-17_1000.zip"), "w") as f:
        f.write("dummy")
    with open(os.path.join(backup_manager.backup_path, "Prospects_2026-03-17_1100.zip"), "w") as f:
        f.write("dummy")
    with open(os.path.join(backup_manager.backup_path, "other_file.txt"), "w") as f:
        f.write("dummy")
        
    backup_manager._enforce_retention()
    
    remaining = os.listdir(backup_manager.backup_path)
    assert "other_file.txt" in remaining
    assert len([f for f in remaining if f.startswith("Prospects_")]) == 1

def test_restore_backup_extracts_files(backup_manager, tmp_path):
    # Create a dummy backup zip
    source_content = tmp_path / "source_content"
    source_content.mkdir()
    (source_content / "save.txt").write_text("restored data")
    
    backup_file = os.path.join(backup_manager.backup_path, "Prospects_test")
    shutil.make_archive(backup_file, "zip", str(source_content))
    
    # Perform restore
    backup_manager.restore_backup("Prospects_test.zip")
    
    # Verify file was restored to Prospects
    prospects_path = os.path.join(backup_manager.server_path, "Icarus", "Saved", "PlayerData", "DedicatedServer", "Prospects")
    restored_file = os.path.join(prospects_path, "save.txt")
    assert os.path.exists(restored_file)
    with open(restored_file, "r") as f:
        assert f.read() == "restored data"

def test_restore_backup_missing_file(backup_manager):
    # Should not raise exception
    try:
        backup_manager.restore_backup("non_existent.zip")
    except Exception as e:
        pytest.fail(f"restore_backup raised exception on missing file: {e}")

import shutil
import os
