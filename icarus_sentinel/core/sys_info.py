import platform
import psutil
import re
import os
from typing import Dict

def get_app_version() -> str:
    """
    Reads the application version from version_info.txt.
    Looks for the ProductVersion field.
    """
    version_file = "version_info.txt"
    if not os.path.exists(version_file):
        return "Unknown"
    
    try:
        with open(version_file, "r", encoding="utf-8") as f:
            content = f.read()
            # Look for StringStruct(u'ProductVersion', u'X.X.X.X')
            match = re.search(r"StringStruct\(u'ProductVersion', u'([^']+)'\)", content)
            if match:
                return match.group(1)
    except Exception:
        pass
        
    return "Unknown"

def get_system_info() -> Dict[str, str]:
    """
    Fetches basic system information: OS, RAM, and CPU.
    """
    # OS Name
    os_name = f"{platform.system()} {platform.release()}"
    
    # RAM
    mem = psutil.virtual_memory()
    total_ram_gb = mem.total / (1024 ** 3)
    ram_info = f"{total_ram_gb:.1f} GB"
    
    # CPU
    cpu_info = platform.processor() or "Unknown CPU"
    
    return {
        "os": os_name,
        "ram": ram_info,
        "cpu": cpu_info
    }
