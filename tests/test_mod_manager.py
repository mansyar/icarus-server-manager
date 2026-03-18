import pytest
import os
import shutil
import zipfile
from icarus_sentinel.core.mod_manager import ModManager

@pytest.fixture
def server_root(tmp_path):
    root = tmp_path / "server"
    root.mkdir()
    return root

@pytest.fixture
def mod_manager(server_root):
    return ModManager(server_root=str(server_root))

def test_list_mods_empty(mod_manager):
    assert mod_manager.list_mods() == []

def test_install_mod_pak(mod_manager, server_root, tmp_path):
    mod_file = tmp_path / "test_mod.pak"
    mod_file.write_text("dummy pak content")
    
    mod_manager.install_mod(str(mod_file))
    
    expected_path = server_root / "Icarus" / "Content" / "Paks" / "mods" / "test_mod.pak"
    assert expected_path.exists()
    assert expected_path.read_text() == "dummy pak content"
    assert "test_mod.pak" in mod_manager.list_mods()

def test_install_mod_zip(mod_manager, server_root, tmp_path):
    zip_path = tmp_path / "mod.zip"
    pak_content = "zipped pak content"
    
    with zipfile.ZipFile(zip_path, 'w') as z:
        z.writestr("zipped_mod.pak", pak_content)
        z.writestr("readme.txt", "ignore me")
    
    mod_manager.install_mod(str(zip_path))
    
    expected_path = server_root / "Icarus" / "Content" / "Paks" / "mods" / "zipped_mod.pak"
    assert expected_path.exists()
    assert expected_path.read_text() == pak_content
    assert "zipped_mod.pak" in mod_manager.list_mods()
    assert not (server_root / "Icarus" / "Content" / "Paks" / "mods" / "readme.txt").exists()

def test_remove_mod(mod_manager, server_root):
    mods_dir = server_root / "Icarus" / "Content" / "Paks" / "mods"
    mods_dir.mkdir(parents=True)
    mod_file = mods_dir / "to_remove.pak"
    mod_file.write_text("content")
    
    assert "to_remove.pak" in mod_manager.list_mods()
    
    mod_manager.remove_mod("to_remove.pak")
    
    assert not mod_file.exists()
    assert "to_remove.pak" not in mod_manager.list_mods()

def test_install_mod_creates_dir(mod_manager, server_root, tmp_path):
    mod_file = tmp_path / "test.pak"
    mod_file.write_text("data")
    
    # Ensure dir doesn't exist
    mods_dir = server_root / "Icarus" / "Content" / "Paks" / "mods"
    assert not mods_dir.exists()
    
    mod_manager.install_mod(str(mod_file))
    
    assert mods_dir.exists()
