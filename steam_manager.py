import os
import urllib.request
import zipfile
import shutil
import subprocess
from typing import Optional

class SteamManager:
    """Manager for SteamCMD installation and server deployment."""
    
    STEAMCMD_URL = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_win32.zip"
    ICARUS_APPID = "2089300"

    def __init__(self, root_dir: Optional[str] = None) -> None:
        """Initializes the SteamManager.

        Args:
            root_dir: The base directory for SteamCMD. Defaults to the directory of this file.
        """
        if root_dir is None:
            self.root_dir = os.path.dirname(os.path.abspath(__file__))
        else:
            self.root_dir = root_dir
        
        self.steamcmd_dir = os.path.join(self.root_dir, "steamcmd")
        self.steamcmd_path = os.path.join(self.steamcmd_dir, "steamcmd.exe")

    def download_steamcmd(self) -> None:
        """Downloads and extracts SteamCMD.
        
        Raises:
            OSError: If there's an issue with file operations.
            urllib.error.URLError: If the download fails.
        """
        if not os.path.exists(self.steamcmd_dir):
            os.makedirs(self.steamcmd_dir)
        
        zip_path = os.path.join(self.steamcmd_dir, "steamcmd.zip")
        
        # Download
        urllib.request.urlretrieve(self.STEAMCMD_URL, zip_path)
        
        # Extract
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(self.steamcmd_dir)
        
        # Clean up
        if os.path.exists(zip_path):
            os.remove(zip_path)

    def is_installed(self) -> bool:
        """Checks if SteamCMD is installed.

        Returns:
            True if steamcmd.exe exists, False otherwise.
        """
        return os.path.exists(self.steamcmd_path)

    def install_server(self, install_dir: str) -> subprocess.Popen:
        """Installs or updates the Icarus server.

        Args:
            install_dir: The directory where the server should be installed.

        Returns:
            The subprocess.Popen object for the SteamCMD process.
        """
        if not self.is_installed():
            self.download_steamcmd()

        cmd = [
            self.steamcmd_path,
            "+force_install_dir", install_dir,
            "+login", "anonymous",
            "+app_update", self.ICARUS_APPID, "validate",
            "+quit"
        ]
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        return process
