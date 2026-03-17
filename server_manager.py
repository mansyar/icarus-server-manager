import json
import os
import subprocess

class ServerProcessManager:
    def __init__(self, state_file="server_state.json"):
        self.state_file = state_file
        self.state = {"pid": None, "status": "stopped"}
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
        if process:
            try:
                process.terminate()
                # We don't want to block indefinitely, but a short wait is good for state sync
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
            except ProcessLookupError:
                pass
        
        self.state["pid"] = None
        self.state["status"] = "stopped"
        self.save_state()

    def restart_server(self, old_process, exe_path, port=17777, query_port=27015):
        self.stop_server(old_process)
        return self.start_server(exe_path, port, query_port)
