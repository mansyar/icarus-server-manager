# Specification: GUI Icon & Visual Identity Implementation (gui-icon_20260320)

## 1. Overview
This track focuses on integrating the `assets/app_icon.png` icon into the Icarus Sentinel application to establish a consistent visual brand. The icon will serve as the window icon, taskbar identifier, executable icon, and a key asset within the internal UI (About dialog, Splash Screen).

## 2. Functional Requirements
- **FR 1: Window & Taskbar Icon:** Set `assets/app_icon.png` as the application-level icon using PySide6's `QIcon` class. This ensures it appears in the window title bar and the Windows taskbar.
- **FR 2: Executable Icon:** Configure the PyInstaller build process to use the `app_icon.png` icon for the final `.exe` file icon shown in File Explorer.
- **FR 3: UI Integration (About Dialog):** Update the `About` dialog UI to prominently display the `app_icon.png` icon.
- **FR 4: UI Integration (Splash Screen):** Implement or update the application's splash screen to feature the `app_icon.png` icon during the initialization phase.
- **FR 5: Resource Management:** Create and integrate a Qt Resource file (`.qrc`) to bundle the icon directly into the Python application code, ensuring portability and reliability when compiled.

## 3. Non-Functional Requirements
- **Performance:** Icon loading should be instantaneous and not block the main UI thread.
- **Portability:** The application must remain a single-folder or single-executable distribution without external dependency on the `assets/` folder at runtime (via `.qrc`).
- **Visual Fidelity:** Transparency in `app_icon.png` must be preserved across all platforms and display modes.

## 4. Acceptance Criteria
- [ ] The main window displays the `app_icon.png` icon in the top-left corner.
- [ ] The Windows taskbar displays the `app_icon.png` icon when the application is active.
- [ ] The "About" dialog contains a high-quality rendering of the `app_icon.png` icon.
- [ ] The splash screen displays the `app_icon.png` icon during startup.
- [ ] The application successfully builds with PyInstaller, and the resulting `.exe` has the `app_icon.png` icon (verified via metadata/build logs).

## 5. Out of Scope
- [ ] Creating alternative icon states (e.g., "active", "error", "updating").
- [ ] Multi-resolution icon generation beyond what is provided by the source PNG.
- [ ] Desktop shortcut creation (handled by installer, not the app itself).
