import configparser
import os

class INIManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = configparser.ConfigParser(interpolation=None, strict=False)
        self.config.optionxform = str # Preserve case
        self.load()

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                self.config.read_file(f)
        else:
            # Initialize with default section if missing
            if not self.config.has_section("/Script/IcarusServer.IcarusServerSettings"):
                self.config.add_section("/Script/IcarusServer.IcarusServerSettings")

    def get_setting(self, key, section="/Script/IcarusServer.IcarusServerSettings"):
        if self.config.has_option(section, key):
            return self.config.get(section, key)
        return None

    def set_setting(self, key, value, section="/Script/IcarusServer.IcarusServerSettings"):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value))

    def save(self):
        with open(self.file_path, "w") as f:
            self.config.write(f, space_around_delimiters=False)

    def get_raw_text(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return f.read()
        return ""

    def save_raw_text(self, text):
        with open(self.file_path, "w") as f:
            f.write(text)
        self.load() # Refresh config object after raw edit
