import zipfile
import os
import sys

def bundle():
    """Bundles the compiled executable and README into a release ZIP archive."""
    exe_path = os.path.join("dist", "IcarusSentinel.exe")
    readme_path = "README.md"
    zip_name = "IcarusSentinel.zip"
    
    if not os.path.exists(exe_path):
        print(f"Error: {exe_path} not found. Run build_exe.py first.")
        sys.exit(1)
        
    if not os.path.exists(readme_path):
        print(f"Error: {readme_path} not found.")
        sys.exit(1)
        
    print(f"Creating {zip_name}...")
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(exe_path, os.path.basename(exe_path))
        zipf.write(readme_path, os.path.basename(readme_path))
        
    print(f"Successfully created {zip_name}")

if __name__ == "__main__":
    bundle()
