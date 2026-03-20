import os
import re
import sys

def update_version_files(version_str: str):
    """
    Update version_info.txt and icarus_sentinel/__init__.py with the given version.
    
    Args:
        version_str: Version string, optionally starting with 'v' (e.g. 'v1.2.3')
    """
    # Clean version string: remove 'v' if present
    clean_version = version_str.lstrip('v')
    
    # Validate format: should be major.minor.patch (optionally .build)
    # Match at least 3 digits separated by dots
    if not re.match(r"^\d+\.\d+\.\d+(\.\d+)?$", clean_version):
        raise ValueError(f"Invalid version format: '{version_str}'. Expected X.Y.Z or X.Y.Z.W")
    
    # Ensure it has 4 components for version_info.txt
    parts = clean_version.split('.')
    while len(parts) < 4:
        parts.append('0')
    
    # PyInstaller tuple format (1, 2, 3, 4)
    tuple_version = f"({', '.join(parts)})"
    # Dot format 1.2.3.4
    dot_version = '.'.join(parts)
    # X.Y.Z format for __init__.py
    init_version = '.'.join(parts[:3])

    # 1. Update version_info.txt
    version_info_path = "version_info.txt"
    if os.path.exists(version_info_path):
        with open(version_info_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Update filevers and prodvers tuples
        content = re.sub(r"filevers=\(\d+, \d+, \d+, \d+\)", f"filevers={tuple_version}", content)
        content = re.sub(r"prodvers=\(\d+, \d+, \d+, \d+\)", f"prodvers={tuple_version}", content)
        
        # Update FileVersion and ProductVersion strings
        content = re.sub(r"StringStruct\(u'FileVersion', u'[0-9.]+'\)", f"StringStruct(u'FileVersion', u'{dot_version}')", content)
        content = re.sub(r"StringStruct\(u'ProductVersion', u'[0-9.]+'\)", f"StringStruct(u'ProductVersion', u'{dot_version}')", content)
        
        with open(version_info_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {version_info_path} to {dot_version}")
    else:
        print(f"Warning: {version_info_path} not found.")

    # 2. Update icarus_sentinel/__init__.py
    init_path = os.path.join("icarus_sentinel", "__init__.py")
    if os.path.exists(init_path):
        with open(init_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        content = re.sub(r"__version__ = \"[0-9.]+\"", f"__version__ = \"{init_version}\"", content)
        
        with open(init_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {init_path} to {init_version}")
    else:
        print(f"Warning: {init_path} not found.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/inject_version.py <version>")
        sys.exit(1)
        
    try:
        update_version_files(sys.argv[1])
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
