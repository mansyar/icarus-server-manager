import PyInstaller.__main__
import os
import sys

def build():
    """Compiles the application into a standalone executable using PyInstaller."""
    
    # Base entry point
    entry_point = os.path.join("icarus_sentinel", "main.py")
    
    # Non-Python files to include (Source;Destination)
    # On Windows, use ';' as separator
    data_files = [
        ("icarus_sentinel/resources/server_state.json", "icarus_sentinel/resources"),
    ]
    
    args = [
        entry_point,
        "--name=IcarusSentinel",
        "--onefile",
        "--windowed",
        "--clean",
    ]
    
    # Add data files
    for src, dst in data_files:
        args.append(f"--add-data={src}{os.pathsep}{dst}")
        
    print(f"Building with arguments: {' '.join(args)}")
    
    PyInstaller.__main__.run(args)

if __name__ == "__main__":
    build()
