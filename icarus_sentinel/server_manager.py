"""Module for managing the Icarus server process lifecycle and monitoring.

This module provides the ServerProcessManager class to handle starting, stopping,
restarting, and monitoring the Icarus server process, including state recovery
and crash detection.
"""

import json
import os
import subprocess
import psutil
from datetime import datetime
from icarus_sentinel.notification_manager import NotificationManager
from icarus_sentinel.a2s_client import A2SClient

class ServerProcessManager:
    """Manages the lifecycle and resource monitoring of the Icarus server process."""

    def __init__(self, state_file="server_state.json", notification_manager=None, a2s_client=None, backup_manager=None):
        self.state_file = state_file
        self.state = {"pid": None, "status": "stopped"}
        self.restart_count = 0
        self.max_restarts = 3
        self.ram_threshold_gb = 16.0
        self.smart_restart_enabled = False
        self.smart_restart_time = "04:00"
        self.last_smart_restart_date = None
        self.notifications = notification_manager or NotificationManager()
        self.a2s_client = a2s_client or A2SClient()
        self.backup_manager = backup_manager
        self.last_sync_timestamp = None
        self.load_state()

    def load_state(self):
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    self.state = json.load(f)
                    self.ram_threshold_gb = self.state.get("ram_threshold_gb", 16.0)
                    self.smart_restart_enabled = self.state.get("smart_restart_enabled", False)
                    self.smart_restart_time = self.state.get("smart_restart_time", "04:00")
                    self.last_smart_restart_date = self.state.get("last_smart_restart_date")
                    self.last_sync_timestamp = self.state.get("last_sync_timestamp")
                    
                    if self.backup_manager:
                        self.backup_manager.interval_minutes = self.state.get("backup_interval_minutes", 30.0)
                        self.backup_manager.retention_limit = self.state.get("backup_retention_limit", 50)
            except (json.JSONDecodeError, IOError):
                self.state = {"pid": None, "status": "stopped"}

    def save_state(self):
        try:
            self.state["ram_threshold_gb"] = self.ram_threshold_gb
            self.state["smart_restart_enabled"] = self.smart_restart_enabled
            self.state["smart_restart_time"] = self.smart_restart_time
            self.state["last_smart_restart_date"] = self.last_smart_restart_date
            self.state["last_sync_timestamp"] = self.last_sync_timestamp
            
            if self.backup_manager:
                self.state["backup_interval_minutes"] = self.backup_manager.interval_minutes
                self.state["backup_retention_limit"] = self.backup_manager.retention_limit
                
            with open(self.state_file, "w") as f:
                json.dump(self.state, f)
        except IOError:
            pass

    def start_server(self, exe_path, port=17777, query_port=27015, server_name="Icarus Server", max_players=8, password=None, admin_password=None, no_steam=False):
        cmd = [
            exe_path,
            f"-Port={port}",
            f"-QueryPort={query_port}",
            f"-SteamServerName={server_name}",
            f"-maxplayers={max_players}",
            "-Log"
        ]
        
        if no_steam: cmd.append("-NOSTEAM")
        if password: cmd.append(f"-JoinPassword={password}")
        if admin_password: cmd.append(f"-AdminPassword={admin_password}")
        
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
        if not process: return
        try:
            p = psutil.Process(process) if isinstance(process, int) else process
            p.terminate()
            try:
                p.wait(timeout=5)
            except (psutil.TimeoutExpired, subprocess.TimeoutExpired):
                p.kill()
        except (psutil.NoSuchProcess, ProcessLookupError, psutil.AccessDenied):
            pass
        
        if self.backup_manager: self.backup_manager.on_server_stop()
        self.state["pid"] = None
        self.state["status"] = "stopped"
        self.save_state()

    def get_resource_usage(self, process):
        if not process: return {"cpu": 0.0, "ram_gb": 0.0}
        pid = process.pid if hasattr(process, "pid") else process
        if hasattr(process, "poll") and process.poll() is not None: return {"cpu": 0.0, "ram_gb": 0.0}
        
        try:
            p = psutil.Process(pid)
            if not p.is_running(): return {"cpu": 0.0, "ram_gb": 0.0}
            cpu = p.cpu_percent(interval=None)
            ram_gb = round(p.memory_info().rss / (1024**3), 2)
            
            if ram_gb > self.ram_threshold_gb:
                if self.state["status"] == "running":
                    self.state["status"] = "warning"
                    self.save_state()
                    self.notifications.notify("High RAM Usage Alert", f"Icarus Server is using {ram_gb}GB of RAM.")
            elif ram_gb <= self.ram_threshold_gb and self.state["status"] == "warning":
                self.state["status"] = "running"
                self.save_state()

            return {"cpu": cpu, "ram_gb": ram_gb}
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return {"cpu": 0.0, "ram_gb": 0.0}

    def stream_logs(self, process, callback):
        if not process or not process.stdout: return
        for line in iter(process.stdout.readline, ""):
            if line: callback(line.strip())

    def should_smart_restart(self, query_port=27015, log_func=None):
        """Checks if a smart restart should be triggered."""
        if not self.smart_restart_enabled:
            return False
        
        now_dt = datetime.now()
        now_time = now_dt.strftime("%H:%M")
        today_date = now_dt.strftime("%Y-%m-%d")

        target_time = self.smart_restart_time.strip() if self.smart_restart_time else ""
        if target_time and len(target_time) == 4 and ":" in target_time:
            target_time = "0" + target_time

        # DEBUG: Log the time check if minute matches or if requested
        if log_func:
            log_func(f"DEBUG: Smart Restart Check - Current: {now_time}, Target: {target_time}, Enabled: {self.smart_restart_enabled}")

        if now_time != target_time:
            return False
        
        if self.last_smart_restart_date == today_date:
            if log_func: log_func(f"DEBUG: Smart Restart already performed today ({today_date})")
            return False
        
        if self.state["status"] not in ["running", "warning"] or self.state["pid"] is None:
            if log_func: log_func(f"DEBUG: Smart Restart skipped - Server status is {self.state['status']}")
            return False

        # Check player count
        if log_func: log_func("DEBUG: Smart Restart time matched. Checking player count...")
        players = self.a2s_client.get_player_count(port=query_port)
        
        if players == 0:
            self.last_smart_restart_date = today_date
            self.save_state()
            return True
        else:
            if log_func: log_func(f"DEBUG: Smart Restart skipped - {players} players active.")
        
        return False

    def get_available_system_ram_pct(self):
        mem = psutil.memory_info() if hasattr(psutil, "memory_info") else psutil.virtual_memory()
        return round((mem.available / mem.total) * 100, 2)
