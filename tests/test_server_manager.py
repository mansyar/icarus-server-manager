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

@patch("subprocess.Popen")
def test_start_server(mock_popen, manager):
    mock_process = MagicMock()
    mock_process.pid = 9999
    mock_popen.return_value = mock_process
    
    server_exe = "C:/icarus/IcarusServer.exe"
    # Create the directory so os.path.dirname doesn't fail if we check it
    manager.start_server(server_exe, port=17777, query_port=27015)
    
    mock_popen.assert_called_once()
    args, kwargs = mock_popen.call_args
    cmd = args[0]
    assert server_exe in cmd
    assert "-Port=17777" in cmd
    assert "-QueryPort=27015" in cmd
    assert "-Log" in cmd
    
    assert manager.state["pid"] == 9999
    assert manager.state["status"] == "running"

def test_stop_server(manager):
    mock_process = MagicMock()
    manager.stop_server(mock_process)
    
    mock_process.terminate.assert_called_once()
    assert manager.state["pid"] is None
    assert manager.state["status"] == "stopped"

@patch("subprocess.Popen")
def test_restart_server(mock_popen, manager):
    # Mock current running process
    mock_old_process = MagicMock()
    
    # Mock new process from restart
    mock_new_process = MagicMock()
    mock_new_process.pid = 8888
    mock_popen.return_value = mock_new_process
    
    server_exe = "C:/icarus/IcarusServer.exe"
    manager.restart_server(mock_old_process, server_exe)
    
    mock_old_process.terminate.assert_called_once()
    mock_popen.assert_called_once()
    assert manager.state["pid"] == 8888
