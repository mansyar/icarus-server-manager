# Implementation Plan: Packaging & Distribution (MVP Release Prep)

## Phase 1: Local Executable Compilation
- [x] Task: Install PyInstaller and create build script. [87b691d]
    - [ ] Update `requirements.txt` with `pyinstaller` dependency.
    - [ ] Write a script or command to compile the `icarus_sentinel` application into a standalone executable (`IcarusSentinel.exe`).
- [ ] Task: Configure PyInstaller specs.
    - [ ] Configure PyInstaller to include required non-Python data files (e.g., UI assets, `customtkinter` theme, default `server_state.json` or `.ini` configuration files).
    - [ ] Add version information and application icon.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Local Executable Compilation' (Protocol in workflow.md)

## Phase 2: Build Artifacts and Documentation
- [ ] Task: Create `README.md` containing quick-start instructions and basic troubleshooting steps.
- [ ] Task: Create a script (e.g., Python or PowerShell) to automate bundling the built executable and `README.md` into a release `.zip` archive.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Build Artifacts and Documentation' (Protocol in workflow.md)

## Phase 3: Automated CI/CD Setup
- [ ] Task: Create a GitHub Actions workflow `.yml` file.
    - [ ] Configure the workflow to trigger on pushing tags (e.g., `v*`).
    - [ ] Set up the Windows build environment (install Python, dependencies).
    - [ ] Execute the build and packaging scripts.
    - [ ] Publish the resulting `.zip` archive as an artifact attached to a GitHub Release.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Automated CI/CD Setup' (Protocol in workflow.md)