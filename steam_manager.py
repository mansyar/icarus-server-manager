import os
import urllib.request
import zipfile
import shutil

class SteamManager:
    STEAMCMD_URL = "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_win32.zip"

    def __init__(self, root_dir=None):
        if root_dir is None:
            self.root_dir = os.path.dirname(os.path.abspath(__file__))
        else:
            self.root_dir = root_dir
        
        self.steamcmd_dir = os.path.join(self.root_dir, "steamcmd")
        self.steamcmd_path = os.path.join(self.steamcmd_dir, "steamcmd.exe")

    def download_steamcmd(self):
        """Downloads and extracts SteamCMD."""
        if not os.path.exists(self.steamcmd_dir):
            os.makedirs(self.steamcmd_dir)
        
        zip_path = os.path.join(self.steamcmd_dir, "steamcmd.zip")
        
        # Download
        urllib.request.urlretrieve(self.STEAMCMD_URL, zip_path)
        
        # Extract
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(self.steamcmd_dir)
        
        # Clean up
        os.remove(zip_path)

    def is_installed(self):
        return os.path.exists(self.steamcmd_path)
