"""Constants for Icarus Sentinel."""

import os
import sys

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Fallback to the project root directory
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    return os.path.normpath(os.path.join(base_path, relative_path))

# View Names
VIEW_SERVER = "Server"
VIEW_CONFIG = "Configuration"
VIEW_BACKUPS = "Backups"
VIEW_SYNC = "Save Sync"
VIEW_MODS = "Mods"

# Default Paths
DEFAULT_INSTALL_DIR = "icarus_server"
DEFAULT_BACKUP_DIR = "backups"

# State File Path
STATE_FILE = get_resource_path(os.path.join("icarus_sentinel", "resources", "server_state.json"))

# INI Sections
SECTION_SENTINEL = "Sentinel"

# Monitoring
MONITORING_INTERVAL_MS = 5000

# Defaults
DEFAULT_PORT = "17777"
DEFAULT_QUERY_PORT = "27015"
DEFAULT_SERVER_NAME = "ICARUS Dedicated Server [OFME]"
