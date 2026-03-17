# Specification: Packaging & Distribution (MVP Release Prep)

## Overview
The goal of this track is to fulfill the final non-functional requirement for the MVP: portability. We need to distribute **Icarus Sentinel** as a single executable or folder distribution so that users do not need to install Python or any dependencies on their local machines.

## Functional Requirements
1.  **Executable Compilation:** Use **PyInstaller** to bundle the Python application (`icarus_sentinel` package), the Python interpreter, and all dependencies (from `requirements.txt`) into a standalone Windows executable (`IcarusSentinel.exe`).
2.  **Asset Inclusion:** Ensure PyInstaller includes necessary non-Python files, specifically the CustomTkinter theme files, UI assets (if any), and default configuration files (`server_state.json` initialized to defaults).
3.  **Distribution Package:** Create a release `.zip` archive containing the `IcarusSentinel.exe` and a `README.md` file with quick-start instructions.
4.  **Automated CI/CD:** Set up a GitHub Actions workflow to automatically run PyInstaller, create the `.zip` archive, and publish a GitHub Release when a new tag is pushed.

## Non-Functional Requirements
-   **Portability:** The resulting executable must run on a clean Windows 10/11 machine without Python installed.
-   **Size:** Aim to keep the executable and resulting `.zip` as small as possible.
-   **Automation:** The build process must be reproducible and automated via GitHub Actions.

## Acceptance Criteria
-   [ ] Running PyInstaller locally successfully creates a working `IcarusSentinel.exe`.
-   [ ] The compiled executable launches without errors and functions identically to the script version.
-   [ ] The final `.zip` archive contains the executable and a `README.md`.
-   [ ] Pushing a new version tag (e.g., `v1.0.0`) to GitHub triggers an Action that builds and attaches the `.zip` to the release.

## Out of Scope
-   Creating a Windows Installer (.msi/.exe installer setup).
-   Code signing the executable (this will trigger Windows SmartScreen, but code signing is expensive/complex for an MVP).