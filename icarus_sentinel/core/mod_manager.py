import os
import shutil
import zipfile
from typing import List

class ModManager:
    """
    Handles installation, removal, and listing of Icarus server mods (.pak files).
    """
    def __init__(self, server_root: str):
        """
        Initializes the ModManager.

        Args:
            server_root: The root directory of the Icarus server installation.
        """
        self.server_root = server_root
        # Standard Icarus mod directory: \Icarus\Content\Paks\mods
        self.mods_dir = os.path.join(self.server_root, "Icarus", "Content", "Paks", "mods")

    def list_mods(self) -> List[str]:
        """
        Lists all .pak files in the server's mods directory.

        Returns:
            A list of filenames of installed mods.
        """
        if not os.path.exists(self.mods_dir):
            return []
        return [f for f in os.listdir(self.mods_dir) if f.endswith(".pak")]

    def install_mod(self, source_path: str) -> None:
        """
        Installs a mod from a .pak or .zip file.
        If .zip, extracts all .pak files into the mods directory.

        Args:
            source_path: The local path to the mod file or archive to install.
        """
        if not os.path.exists(self.mods_dir):
            os.makedirs(self.mods_dir, exist_ok=True)

        if source_path.lower().endswith(".pak"):
            shutil.copy2(source_path, self.mods_dir)
        elif source_path.lower().endswith(".zip"):
            with zipfile.ZipFile(source_path, 'r') as z:
                for file_info in z.infolist():
                    if file_info.filename.endswith(".pak"):
                        # Extract and flatten (ignore internal zip folder structure)
                        filename = os.path.basename(file_info.filename)
                        if not filename: # Skip directories
                            continue
                        target_path = os.path.join(self.mods_dir, filename)
                        with z.open(file_info) as source, open(target_path, "wb") as target:
                            shutil.copyfileobj(source, target)

    def remove_mod(self, mod_name: str) -> None:
        """
        Deletes a specific mod file from the server's mods directory.

        Args:
            mod_name: The filename of the mod to remove (e.g., 'MyMod.pak').
        """
        mod_path = os.path.join(self.mods_dir, mod_name)
        if os.path.exists(mod_path):
            os.remove(mod_path)
