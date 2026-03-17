import pytest
import os
import json
from unittest.mock import patch, MagicMock

from server_manager import ServerProcessManager

@pytest.fixture
def state_file(tmp_path):
    return tmp_path / "server_state.json"

@pytest.fixture
def manager(state_file):
    return ServerProcessManager(state_file=str(state_file))

def test_init_creates_default_state(manager, state_file):
    assert manager.state_file == str(state_file)
    assert manager.state == {"pid": None, "status": "stopped"}

def test_save_state(manager, state_file):
    manager.state["pid"] = 1234
    manager.state["status"] = "running"
    manager.save_state()
    
    assert os.path.exists(str(state_file))
    with open(str(state_file), "r") as f:
        saved_state = json.load(f)
    assert saved_state == {"pid": 1234, "status": "running"}

def test_load_state(state_file):
    initial_state = {"pid": 5678, "status": "running"}
    with open(str(state_file), "w") as f:
        json.dump(initial_state, f)
    
    manager = ServerProcessManager(state_file=str(state_file))
    assert manager.state == initial_state

def test_load_state_corrupted_file(state_file):
    with open(str(state_file), "w") as f:
        f.write("not json")
    
    manager = ServerProcessManager(state_file=str(state_file))
    assert manager.state == {"pid": None, "status": "stopped"}
