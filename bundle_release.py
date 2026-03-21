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
        
        # Add ONLY relevant assets for the User Guide
        relevant_assets = [
            "assets/app_icon.png",
            "assets/dashboard_preview.png",
            "assets/config_preview.png"
        ]
        
        for asset in relevant_assets:
            if os.path.exists(asset):
                zipf.write(asset, asset)
            else:
                print(f"Warning: Asset {asset} not found.")
        
    print(f"Successfully created {zip_name}")

if __name__ == "__main__":
    bundle()
