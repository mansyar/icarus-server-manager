"""Module for managing the Icarus server process lifecycle and monitoring.

This module provides the ServerProcessManager class to handle starting, stopping,
restarting, and monitoring the Icarus server process, including state recovery
and crash detection.
"""

import json
import os
import subprocess
import psutil

class ServerProcessManager:
    """Manages the lifecycle and resource monitoring of the Icarus server process.

    Attributes:
        state_file (str): Path to the JSON file for persisting server state.
        state (dict): Current server state, including PID and status.
        restart_count (int): Current count of automatic restarts since last manual start.
        max_restarts (int): Maximum allowed automatic restarts upon crash.
    """

    def __init__(self, state_file="server_state.json"):
        """Initializes the ServerProcessManager and loads existing state.

        Args:
            state_file (str): Path to the state persistence file.
        """
        self.state_file = state_file
        self.state = {"pid": None, "status": "stopped"}
        self.restart_count = 0
        self.max_restarts = 3
        self.load_state()

    def load_state(self):
        """Loads the server state from the persistent JSON file.

        Resets to default 'stopped' state if the file is missing or corrupted.
        """
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    self.state = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.state = {"pid": None, "status": "stopped"}

    def save_state(self):
        """Saves the current server state to the persistent JSON file.
        """
        try:
            with open(self.state_file, "w") as f:
                json.dump(self.state, f)
        except IOError:
            pass

    def start_server(self, exe_path, port=17777, query_port=27015):
        """Starts the Icarus server process with the specified configuration.

        Args:
            exe_path (str): Full path to the IcarusServer executable.
            port (int): The game port to use. Defaults to 17777.
            query_port (int): The query port to use. Defaults to 27015.

        Returns:
            subprocess.Popen: The started process object.
        """
        cmd = [
            exe_path,
            f"-Port={port}",
            f"-QueryPort={query_port}",
            "-Log"
        ]
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            cwd=os.path.dirname(exe_path)
        )
        
        self.state["pid"] = process.pid
        self.state["status"] = "running"
        self.save_state()
        return process

    def stop_server(self, process):
        """Gracefully stops the Icarus server process.

        Args:
            process (Union[subprocess.Popen, int]): The process object or PID to stop.
        """
        if not process:
            return

        try:
            if isinstance(process, int):
                # Handle raw PID (from state recovery)
                p = psutil.Process(process)
                p.terminate()
                try:
                    p.wait(timeout=5)
                except psutil.TimeoutExpired:
                    p.kill()
            else:
                # Handle subprocess.Popen object
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
        except (psutil.NoSuchProcess, ProcessLookupError, psutil.AccessDenied):
            pass
        
        self.state["pid"] = None
        self.state["status"] = "stopped"
        self.save_state()

    def restart_server(self, old_process, exe_path, port=17777, query_port=27015):
        """Restarts the server by stopping the old process and starting a new one.

        Args:
            old_process (Union[subprocess.Popen, int]): The current process to stop.
            exe_path (str): Full path to the executable.
            port (int): Game port.
            query_port (int): Query port.

        Returns:
            subprocess.Popen: The new server process object.
        """
        self.stop_server(old_process)
        return self.start_server(exe_path, port, query_port)

    def get_resource_usage(self, process):
        """Calculates current resource usage of the server process.

        Args:
            process (Union[subprocess.Popen, int]): The process object or PID to monitor.

        Returns:
            dict: CPU percentage and RAM usage in GB.
        """
        if not process:
            return {"cpu": 0.0, "ram_gb": 0.0}
        
        # Accept either a subprocess.Popen object or a raw PID (for recovery)
        pid = process.pid if hasattr(process, "pid") else process
        
        # If it's a Popen object, check if it's still running
        if hasattr(process, "poll") and process.poll() is not None:
            return {"cpu": 0.0, "ram_gb": 0.0}
        
        try:
            p = psutil.Process(pid)
            if not p.is_running():
                return {"cpu": 0.0, "ram_gb": 0.0}

            cpu = p.cpu_percent(interval=None)
            ram_bytes = p.memory_info().rss
            ram_gb = round(ram_bytes / (1024**3), 2)
            return {"cpu": cpu, "ram_gb": ram_gb}
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return {"cpu": 0.0, "ram_gb": 0.0}

    def stream_logs(self, process, callback):
        """Streams real-time console logs from the server process.

        Args:
            process (subprocess.Popen): The process to read logs from.
            callback (Callable[[str], None]): Function to call with each new line.
        """
        if not process or not process.stdout:
            return

        for line in iter(process.stdout.readline, ""):
            if line:
                callback(line.strip())

    def handle_crash(self, exe_path):
        """Attempts to recover from a crash by auto-restarting.

        Args:
            exe_path (str): Path to the server executable.

        Returns:
            Optional[subprocess.Popen]: The new process if restarted, else None.
        """
        if self.restart_count < self.max_restarts:
            self.restart_count += 1
            return self.start_server(exe_path)
        else:
            self.state["status"] = "crashed"
            self.save_state()
            return None
