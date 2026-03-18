"""Constants for Icarus Sentinel."""

import os

# View Names
VIEW_SERVER = "Server"
VIEW_CONFIG = "Configuration"
VIEW_BACKUPS = "Backups"
VIEW_SYNC = "Save Sync"
VIEW_MODS = "Mods"

# Default Paths
DEFAULT_INSTALL_DIR = "icarus_server"
DEFAULT_BACKUP_DIR = "backups"
# Use absolute path relative to this file's directory to ensure it's always in resources/
STATE_FILE = os.path.join(os.path.dirname(__file__), "resources", "server_state.json")

# INI Sections
SECTION_SENTINEL = "Sentinel"

# Monitoring
MONITORING_INTERVAL_MS = 5000
