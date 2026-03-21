import zipfile
import os
import sys

def bundle():
    """Bundles the compiled executable, user guide, and assets into a release ZIP archive."""
    exe_path = os.path.join("dist", "IcarusSentinel.exe")
    guide_path = "USER_GUIDE.md"
    assets_dir = "assets"
    zip_name = "IcarusSentinel.zip"
    
    if not os.path.exists(exe_path):
        print(f"Error: {exe_path} not found. Run build_exe.py first.")
        sys.exit(1)
        
    if not os.path.exists(guide_path):
        print(f"Error: {guide_path} not found.")
        sys.exit(1)
        
    print(f"Creating {zip_name}...")
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add Executable
        zipf.write(exe_path, os.path.basename(exe_path))
        # Add User Guide
        zipf.write(guide_path, os.path.basename(guide_path))
        # Add Assets folder (required for icons/previews in User Guide)
        for root, dirs, files in os.walk(assets_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, file_path)
        
    print(f"Successfully created {zip_name}")

if __name__ == "__main__":
    bundle()
