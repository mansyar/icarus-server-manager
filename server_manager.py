import json
import os
import subprocess
import psutil

class ServerProcessManager:
    def __init__(self, state_file="server_state.json"):
        self.state_file = state_file
        self.state = {"pid": None, "status": "stopped"}
        self.restart_count = 0
        self.max_restarts = 3
        self.load_state()

    def load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    self.state = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.state = {"pid": None, "status": "stopped"}

    def save_state(self):
        try:
            with open(self.state_file, "w") as f:
                json.dump(self.state, f)
        except IOError:
            pass

    def start_server(self, exe_path, port=17777, query_port=27015):
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
        self.stop_server(old_process)
        return self.start_server(exe_path, port, query_port)

    def get_resource_usage(self, process):
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
        if not process or not process.stdout:
            return
            
        for line in iter(process.stdout.readline, ""):
            if line:
                callback(line.strip())

    def handle_crash(self, exe_path):
        if self.restart_count < self.max_restarts:
            self.restart_count += 1
            return self.start_server(exe_path)
        else:
            self.state["status"] = "crashed"
            self.save_state()
            return None
