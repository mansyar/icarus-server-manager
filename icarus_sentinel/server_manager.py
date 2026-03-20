"""Module for managing the Icarus server process lifecycle and monitoring.

This module provides the ServerProcessManager class to handle starting, stopping,
restarting, and monitoring the Icarus server process, including state recovery
and crash detection.
"""

import json
import os
import subprocess
import psutil
import re
from datetime import datetime
from icarus_sentinel.notification_manager import NotificationManager
from icarus_sentinel.a2s_client import A2SClient

class ServerProcessManager:
    """Manages the lifecycle and resource monitoring of the Icarus server process."""

    def __init__(self, state_file="server_state.json", notification_manager=None, a2s_client=None, backup_manager=None):
        self.state_file = state_file
        self.state = {"pid": None, "status": "stopped"}
        self._process_obj = None # Persistent psutil.Process for accurate CPU tracking
        self.restart_count = 0
        self.max_restarts = 3
        self.ram_threshold_gb = 16.0
        self.smart_restart_enabled = False
        self.smart_restart_time = "04:00"
        self.last_smart_restart_date = None
        self.notify_server_started = True
        self.notify_player_activity = True
        self.notify_server_error = True
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
                    self.notify_server_started = self.state.get("notify_server_started", True)
                    self.notify_player_activity = self.state.get("notify_player_activity", True)
                    self.notify_server_error = self.state.get("notify_server_error", True)
                    
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
            self.state["notify_server_started"] = self.notify_server_started
            self.state["notify_player_activity"] = self.notify_player_activity
            self.state["notify_server_error"] = self.notify_server_error
            
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
        self._process_obj = psutil.Process(process.pid)
        self.save_state()
        
        # Monitor for crash in background thread (Wait for exit)
        def _monitor_crash():
            ret = process.wait()
            # If pid is still set, it means it wasn't a clean stop via stop_server
            if self.state["pid"] == process.pid and ret != 0:
                self.state["status"] = "error"
                self.save_state()
                if self.notify_server_error:
                    self.notifications.notify("Server Crash", f"Icarus Server has crashed with code {ret}.")
        
        import threading
        threading.Thread(target=_monitor_crash, daemon=True).start()
        
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
        self._process_obj = None
        self.save_state()

    def get_resource_usage(self, process):
        if not process: return {"cpu": 0.0, "ram_gb": 0.0}
        pid = process.pid if hasattr(process, "pid") else process
        
        if self._process_obj is None or self._process_obj.pid != pid:
            try:
                self._process_obj = psutil.Process(pid)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                return {"cpu": 0.0, "ram_gb": 0.0}

        try:
            if not self._process_obj.is_running():
                self._process_obj = None
                return {"cpu": 0.0, "ram_gb": 0.0}
            
            cpu = self._process_obj.cpu_percent(interval=None)
            ram_gb = round(self._process_obj.memory_info().rss / (1024**3), 2)
            
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
            self._process_obj = None
            return {"cpu": 0.0, "ram_gb": 0.0}

    def stream_logs(self, process, callback, event_callback=None):
        if not process or not process.stdout: return
        
        import time
        last_emit = time.time()
        batch = []
        
        for line in iter(process.stdout.readline, ""):
            if line:
                clean_line = line.strip()
                batch.append(clean_line)
                
                now = time.time()
                # Emit batch every 100ms or if batch is getting large
                if now - last_emit > 0.1 or len(batch) >= 20:
                    callback("\n".join(batch))
                    batch = []
                    last_emit = now

                # Parse for events and trigger notifications (keep these individual)
                event = self.parse_log_line(clean_line)
                if event:
                    if event_callback:
                        event_callback(event)
                        
                    if event["type"] == "server_started" and self.notify_server_started:
                        self.notifications.notify("Icarus Server", "Server has started and is ready for players.")
                    elif event["type"] == "player_join" and self.notify_player_activity:
                        self.notifications.notify("Player Joined", f"{event['player']} has joined the server.")
                    elif event["type"] == "player_leave" and self.notify_player_activity:
                        self.notifications.notify("Player Left", f"{event['player']} has left the server.")
        
        # Final flush
        if batch:
            callback("\n".join(batch))

    def should_smart_restart(self, query_port=27015):
        """Checks if a smart restart should be triggered."""
        if not self.smart_restart_enabled:
            return False
        
        now_dt = datetime.now()
        now_time = now_dt.strftime("%H:%M")
        today_date = now_dt.strftime("%Y-%m-%d")

        target_time = self.smart_restart_time.strip() if self.smart_restart_time else ""
        if target_time and len(target_time) == 4 and ":" in target_time:
            target_time = "0" + target_time

        if now_time != target_time:
            return False
        
        if self.last_smart_restart_date == today_date:
            return False
        
        if self.state["status"] not in ["running", "warning"] or self.state["pid"] is None:
            return False

        # Check player count
        players = self.a2s_client.get_player_count(port=query_port)
        
        if players == 0:
            self.last_smart_restart_date = today_date
            self.save_state()
            return True
        
        return False

    def get_available_system_ram_pct(self):
        mem = psutil.virtual_memory()
        return round((mem.available / mem.total) * 100, 2)

    def parse_log_line(self, line: str):
        """Parses a single log line for key server events.
        
        Args:
            line: The raw log line from Icarus server.
            
        Returns:
            A dict containing event 'type' and 'player' if applicable, or None.
        """
        # 1. Server Started (Various indicators)
        if re.search(r"ReadFromProspectSaveState complete", line, re.IGNORECASE) or \
           re.search(r"LogIcarus: Display: Server started", line, re.IGNORECASE) or \
           re.search(r"Engine is initialized\. Leaving FEngineLoop::Init", line, re.IGNORECASE):
            return {"type": "server_started"}
        
        # 2. Player Join
        join_match = re.search(r"LogNet: Join succeeded: (.*)", line, re.IGNORECASE)
        if join_match:
            return {"type": "player_join", "player": join_match.group(1).strip()}
            
        # 3. Player Leave
        leave_match = re.search(r"LogNet: Client \((.*)\) closed connection", line, re.IGNORECASE)
        if leave_match:
            return {"type": "player_leave", "player": leave_match.group(1).strip()}
            
        return None
