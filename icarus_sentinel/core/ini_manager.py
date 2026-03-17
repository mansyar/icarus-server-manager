import configparser
import os
from typing import Optional

class INIManager:
    """Manages reading and writing of Icarus server .ini configuration files.
    
    This class uses configparser to handle two-way synchronization between
    GUI fields and the physical ServerSettings.ini file.
    """

    def __init__(self, file_path: str):
        """Initializes the INI manager.

        Args:
            file_path: The absolute path to the .ini file.
        """
        self.file_path = file_path
        self.config = configparser.ConfigParser(interpolation=None, strict=False)
        self.config.optionxform = str # Preserve case
        self.load()

    def load(self) -> None:
        """Loads the configuration from the file path."""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                self.config.read_file(f)
        else:
            # Initialize with default section if missing
            if not self.config.has_section("/Script/IcarusServer.IcarusServerSettings"):
                self.config.add_section("/Script/IcarusServer.IcarusServerSettings")

    def get_setting(self, key: str, section: str = "/Script/IcarusServer.IcarusServerSettings") -> Optional[str]:
        """Retrieves a setting value from a specific section.

        Args:
            key: The configuration key to look for.
            section: The INI section name.

        Returns:
            The value as a string if found, otherwise None.
        """
        if self.config.has_option(section, key):
            return self.config.get(section, key)
        return None

    def set_setting(self, key: str, value: str, section: str = "/Script/IcarusServer.IcarusServerSettings") -> None:
        """Sets a setting value in a specific section.

        Args:
            key: The configuration key.
            value: The value to set.
            section: The INI section name.
        """
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value))

    def save(self) -> None:
        """Writes the current configuration state to the disk."""
        with open(self.file_path, "w") as f:
            self.config.write(f, space_around_delimiters=False)

    def get_raw_text(self) -> str:
        """Retrieves the raw text content of the INI file.

        Returns:
            The file content as a raw string.
        """
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return f.read()
        return ""

    def save_raw_text(self, text: str) -> None:
        """Overwrites the INI file with raw text and reloads the parser.

        Args:
            text: The raw string content to save.
        """
        with open(self.file_path, "w") as f:
            f.write(text)
        self.load() # Refresh config object after raw edit
