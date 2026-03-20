import pytest
import os
import json
import subprocess
import psutil
from unittest.mock import patch, MagicMock

from icarus_sentinel.server_manager import ServerProcessManager

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
    
    assert saved_state["pid"] == 1234
    assert saved_state["status"] == "running"
    assert saved_state["notify_server_started"] is True

def test_save_state_io_error(manager, state_file):
    with patch("builtins.open", side_effect=IOError):
        manager.save_state()
        # Should not raise exception

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

def test_load_state_io_error(state_file):
    initial_state = {"pid": 5678, "status": "running"}
    with open(str(state_file), "w") as f:
        json.dump(initial_state, f)
        
    with patch("builtins.open", side_effect=IOError):
        manager = ServerProcessManager(state_file=str(state_file))
        assert manager.state == {"pid": None, "status": "stopped"}

@patch("threading.Thread")
@patch("psutil.Process")
@patch("subprocess.Popen")
def test_start_server(mock_popen, mock_psutil, mock_thread, manager):
    mock_process = MagicMock()
    mock_process.pid = 9999
    mock_popen.return_value = mock_process
    mock_psutil.return_value = MagicMock()
    
    server_exe = "C:/icarus/IcarusServer.exe"
    manager.start_server(server_exe, port=17777, query_port=27015)
    
    mock_popen.assert_called_once()
    args, kwargs = mock_popen.call_args
    cmd = args[0]
    assert server_exe in cmd
    assert "-Port=17777" in cmd
    assert "-QueryPort=27015" in cmd
    
    assert manager.state["pid"] == 9999
    assert manager.state["status"] == "running"

def test_stop_server_popen(manager):
    mock_process = MagicMock()
    manager.stop_server(mock_process)
    
    mock_process.terminate.assert_called_once()
    assert manager.state["pid"] is None
    assert manager.state["status"] == "stopped"

@patch("psutil.Process")
def test_stop_server_pid(mock_psutil_process, manager):
    mock_proc_instance = mock_psutil_process.return_value
    manager.stop_server(1234)
    
    mock_psutil_process.assert_called_with(1234)
    mock_proc_instance.terminate.assert_called_once()
    assert manager.state["pid"] is None

@patch("psutil.Process")
def test_stop_server_pid_not_found(mock_psutil_process, manager):
    mock_psutil_process.side_effect = psutil.NoSuchProcess(1234)
    manager.stop_server(1234)
    # Should not raise exception
    assert manager.state["pid"] is None

@patch("psutil.Process")
def test_get_resource_usage_popen(mock_psutil_process, manager):
    mock_proc_instance = mock_psutil_process.return_value
    mock_proc_instance.is_running.return_value = True
    mock_proc_instance.cpu_percent.return_value = 15.5
    mock_memory_info = MagicMock()
    mock_memory_info.rss = 1024 * 1024 * 512 # 512MB
    mock_proc_instance.memory_info.return_value = mock_memory_info
    
    mock_process = MagicMock()
    mock_process.pid = 1234
    
    usage = manager.get_resource_usage(mock_process)
    
    assert usage["cpu"] == 15.5
    assert usage["ram_gb"] == 0.5
    mock_psutil_process.assert_called_with(1234)

@patch("psutil.Process")
def test_get_resource_usage_pid(mock_psutil_process, manager):
    mock_proc_instance = mock_psutil_process.return_value
    mock_proc_instance.is_running.return_value = True
    mock_proc_instance.cpu_percent.return_value = 10.0
    mock_memory_info = MagicMock()
    mock_memory_info.rss = 1024 * 1024 * 1024 # 1GB
    mock_proc_instance.memory_info.return_value = mock_memory_info
    
    usage = manager.get_resource_usage(5678)
    
    assert usage["cpu"] == 10.0
    assert usage["ram_gb"] == 1.0
    mock_psutil_process.assert_called_with(5678)

def test_get_resource_usage_none(manager):
    usage = manager.get_resource_usage(None)
    assert usage == {"cpu": 0.0, "ram_gb": 0.0}

@patch("psutil.Process")
def test_get_resource_usage_finished_popen(mock_psutil_process, manager):
    mock_process = MagicMock()
    mock_process.pid = 1234
    mock_proc_instance = mock_psutil_process.return_value
    mock_proc_instance.is_running.return_value = False
    
    usage = manager.get_resource_usage(mock_process)
    assert usage == {"cpu": 0.0, "ram_gb": 0.0}

@patch("psutil.Process")
def test_get_resource_usage_exception(mock_psutil_process, manager):
    mock_psutil_process.side_effect = psutil.AccessDenied()
    usage = manager.get_resource_usage(1234)
    assert usage == {"cpu": 0.0, "ram_gb": 0.0}

def test_stream_logs(manager):
    mock_process = MagicMock()
    mock_process.stdout.readline.side_effect = ["line 1", "line 2", ""]
    
    lines = []
    def callback(line):
        lines.append(line)
        
    manager.stream_logs(mock_process, callback)
    
    # Batching combines lines
    assert "line 1" in lines[0]
    assert "line 2" in lines[0]

def test_stream_logs_none(manager):
    manager.stream_logs(None, lambda x: None)
    # Should not raise exception
