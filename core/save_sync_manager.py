import os
import shutil
import glob
from typing import List, Optional
from core.ini_manager import INIManager

class SaveSyncManager:
    """Manages two-way synchronization of save files between local and server."""

    def __init__(self, server_path: str, ini_manager: Optional[INIManager] = None):
        self.server_path = server_path
        self.ini_manager = ini_manager
        self.local_appdata = os.environ.get("LOCALAPPDATA")

    def get_local_save_path(self) -> Optional[str]:
        """Returns the root directory for local Steam player data."""
        if not self.local_appdata:
            return None
        return os.path.join(self.local_appdata, "Icarus", "Saved", "PlayerData")

    def list_local_steam_ids(self) -> List[str]:
        """Lists available SteamIDs in the local save root."""
        root = self.get_local_save_path()
        if not root or not os.path.exists(root):
            return []
        return [d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))]

    def list_steam_ids(self) -> List[str]:
        """Alias for list_local_steam_ids for backward compatibility if needed, but we should use list_local_steam_ids."""
        return self.list_local_steam_ids()

    def get_local_prospects_dir(self, steam_id: str) -> Optional[str]:
        """Returns the local Prospects directory for a specific SteamID."""
        root = self.get_local_save_path()
        if not root:
            return None
        return os.path.join(root, steam_id, "Prospects")

    def get_server_prospects_dir(self) -> str:
        """Returns the server Prospects directory."""
        return os.path.join(self.server_path, "Icarus", "Saved", "PlayerData", "DedicatedServer", "Prospects")

    def list_prospects(self, directory: str) -> List[str]:
        """Lists .json prospect files in a directory (without extension)."""
        if not os.path.exists(directory):
            return []
        files = glob.glob(os.path.join(directory, "*.json"))
        return [os.path.splitext(os.path.basename(f))[0] for f in files]

    def sync_to_server(self, steam_id: str, prospect_name: str, update_ini: bool = True) -> bool:
        """Copies a local save to the server."""
        local_dir = self.get_local_prospects_dir(steam_id)
        server_dir = self.get_server_prospects_dir()

        if not local_dir or not os.path.exists(local_dir):
            return False

        src = os.path.join(local_dir, f"{prospect_name}.json")
        if not os.path.exists(src):
            return False

        os.makedirs(server_dir, exist_ok=True)
        dst = os.path.join(server_dir, f"{prospect_name}.json")
        shutil.copy2(src, dst)

        if update_ini and self.ini_manager:
            self.ini_manager.set_setting("LoadProspect", prospect_name)
            self.ini_manager.set_setting("ResumeProspect", "True")
            self.ini_manager.save()

        return True

    def sync_to_local(self, steam_id: str, prospect_name: str) -> bool:
        """Copies a server save to the local machine."""
        local_dir = self.get_local_prospects_dir(steam_id)
        server_dir = self.get_server_prospects_dir()

        if not local_dir:
            return False

        src = os.path.join(server_dir, f"{prospect_name}.json")
        if not os.path.exists(src):
            return False

        os.makedirs(local_dir, exist_ok=True)
        dst = os.path.join(local_dir, f"{prospect_name}.json")
        self._safe_copy(src, dst)

        return True

    def _safe_copy(self, src: str, dst: str):
        """Copies src to dst safely by using a temporary file."""
        temp_dst = dst + ".tmp"
        shutil.copy2(src, temp_dst)
        if os.path.exists(dst):
            # Create a backup of the original if it exists
            backup_dst = dst + ".bak"
            shutil.copy2(dst, backup_dst)
        
        os.replace(temp_dst, dst)

    def sync_prospects(self, steam_id: str):
        """Perform bidirectional sync between local and server prospects."""
        local_dir = self.get_local_prospects_dir(steam_id)
        server_dir = self.get_server_prospects_dir()

        if not local_dir or not os.path.exists(local_dir):
            return

        os.makedirs(server_dir, exist_ok=True)

        local_prospects = self.list_prospects(local_dir)
        server_prospects = self.list_prospects(server_dir)

        all_prospects = set(local_prospects) | set(server_prospects)

        for prospect in all_prospects:
            local_path = os.path.join(local_dir, f"{prospect}.json")
            server_path = os.path.join(server_dir, f"{prospect}.json")

            local_exists = os.path.exists(local_path)
            server_exists = os.path.exists(server_path)

            if local_exists and server_exists:
                local_mtime = os.path.getmtime(local_path)
                server_mtime = os.path.getmtime(server_path)

                if local_mtime > server_mtime:
                    self._safe_copy(local_path, server_path)
                elif server_mtime > local_mtime:
                    self._safe_copy(server_path, local_path)
            elif local_exists:
                self._safe_copy(local_path, server_path)
            elif server_exists:
                self._safe_copy(server_path, local_path)
