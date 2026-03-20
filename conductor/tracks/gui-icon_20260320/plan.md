# Implementation Plan: GUI Icon & Visual Identity (gui-icon_20260320)

## Phase 1: Resource Management & Scaffolding
Establish the foundation for bundling assets into the application code for portability.

- [x] Task: Create `icarus_sentinel/ui/resources.qrc` and include `assets/app_icon.png` (using prefix `icons`). 1f83730
- [ ] Task: Compile `resources.qrc` to `icarus_sentinel/ui/resources_rc.py` using `pyside6-rcc`.
- [ ] Task: Write unit tests in `tests/test_resources.py` to verify `QIcon(":/icons/app_icon.png")` returns a valid icon.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Resource Management & Scaffolding' (Protocol in workflow.md)

## Phase 2: UI Application
Apply the icon across the primary user interfaces.

- [ ] Task: Update `icarus_sentinel/ui/main_window.py` to import `resources_rc` and set the window icon using `self.setWindowIcon(QIcon(":/icons/app_icon.png"))`.
- [ ] Task: Update `icarus_sentinel/ui/about_view.py` to import `resources_rc` and display `app_icon.png` in a `QLabel` (Pixmap).
- [ ] Task: Update `icarus_sentinel/main.py` to implement a `QSplashScreen` that displays `app_icon.png` during the initialization phase.
- [ ] Task: Write UI tests in `tests/test_ui_icons.py` to verify the main window has the correct icon set.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: UI Application' (Protocol in workflow.md)

## Phase 3: Build & Distribution
Ensure the visual identity is preserved in the compiled executable.

- [ ] Task: Create or update `build.py` (or PyInstaller spec) to include the `--icon=assets/app_icon.png` flag.
- [ ] Task: Perform a trial PyInstaller build (dry run or metadata check) to verify the executable icon configuration.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Build & Distribution' (Protocol in workflow.md)
