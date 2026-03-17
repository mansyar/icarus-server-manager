import os
import threading
from datetime import datetime
from typing import Optional

class BackupManager:
    """Manages automated and manual backups for the Icarus server."""

    def __init__(self, server_path: str, backup_path: str, interval_minutes: float = 30.0, retention_limit: int = 50):
        self.server_path = server_path
        self.backup_path = backup_path
        self.interval_minutes = interval_minutes
        self.retention_limit = retention_limit
        self.timer: Optional[threading.Timer] = None
        self._is_running = False

    def start_timer(self) -> None:
        """Starts the recurring backup timer."""
        if self._is_running:
            return
        
        self._is_running = True
        self._schedule_next_backup()

    def stop_timer(self) -> None:
        """Stops the recurring backup timer."""
        self._is_running = False
        if self.timer:
            self.timer.cancel()
            self.timer = None

    def _schedule_next_backup(self) -> None:
        """Schedules the next backup event."""
        if not self._is_running:
            return
            
        # Convert minutes to seconds
        interval_seconds = self.interval_minutes * 60
        self.timer = threading.Timer(interval_seconds, self._timer_callback)
        self.timer.daemon = True
        self.timer.start()

    def _timer_callback(self) -> None:
        """Callback for the background timer."""
        if not self._is_running:
            return
            
        self.create_backup()
        self._schedule_next_backup()

    def create_backup(self) -> None:
        """Triggers an immediate backup."""
        self._perform_backup()

    def on_server_stop(self) -> None:
        """Triggered when the server process is stopped."""
        self.create_backup()

    def _perform_backup(self) -> None:
        """Internal method to perform the actual backup operation."""
        prospects_dir = os.path.join(
            self.server_path, "Icarus", "Saved", "PlayerData", "DedicatedServer", "Prospects"
        )
        
        if not os.path.exists(prospects_dir):
            return

        if not os.path.exists(self.backup_path):
            os.makedirs(self.backup_path)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
        backup_name = f"Prospects_{timestamp}"
        backup_file = os.path.join(self.backup_path, backup_name)

        try:
            # zip creation is blocking, but called from timer thread or manual trigger (which should be threaded if from UI)
            shutil.make_archive(backup_file, "zip", prospects_dir)
            self._enforce_retention()
        except Exception:
            # Log error or notify? PRD says "non-blocking execution" and "reliability"
            pass

    def _enforce_retention(self) -> None:
        """Deletes oldest backups if the limit is exceeded."""
        if not os.path.exists(self.backup_path):
            return

        # List all Prospects_*.zip files
        backups = [
            f for f in os.listdir(self.backup_path)
            if f.startswith("Prospects_") and f.endswith(".zip")
        ]
        
        # Sort by name (which contains timestamp in YYYY-MM-DD_HHMM format)
        backups.sort()

        if len(backups) > self.retention_limit:
            to_delete_count = len(backups) - self.retention_limit
            to_delete = backups[:to_delete_count]
            
            for f in to_delete:
                try:
                    os.remove(os.path.join(self.backup_path, f))
                except OSError:
                    pass

import shutil
