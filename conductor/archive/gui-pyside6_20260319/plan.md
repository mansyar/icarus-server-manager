# Implementation Plan: GUI Overhaul - PySide6 Industrial Transition

## Phase 1: Environment and Core Window Setup [checkpoint: 5b43688]
- [x] Task: Update Tech Stack and Requirements (da12b6f)
    - [x] Add PySide6 and pytest-qt to requirements.txt and update tech-stack.md.
- [x] Task: Create `tests/ui/test_main_window.py` with failing test for window initialization. (d857b8c)
- [x] Task: Implement `MainWindow` class inheriting from `QMainWindow` in `icarus_sentinel/ui/main_window.py`. (d7e6353)
- [x] Task: Refactor application entry point (`main.py`) to launch the PySide6 app. (1d79a26)
- [x] Task: Conductor - User Manual Verification 'Phase 1: Environment and Core Window Setup' (Protocol in workflow.md) (5b43688)

## Phase 2: Modernizing Threading & MVC Wiring [checkpoint: a1aee40]
- [x] Task: Create `tests/core/test_qthread_workers.py` to test Qt-based background workers. (ea23caa)
- [x] Task: Refactor the `Controller` class to manage `QThread` instances instead of standard Python threads for server launch, monitoring, and backups. (4ce2bdf)
- [x] Task: Define Qt Signals (`Signal`) on workers to communicate state changes back to the main thread. (4ce2bdf)
- [x] Task: Conductor - User Manual Verification 'Phase 2: Modernizing Threading & MVC Wiring' (Protocol in workflow.md) (a1aee40)

## Phase 3: Sidebar and Navigation [checkpoint: ed59e09]
- [x] Task: Create `tests/ui/test_sidebar.py` with failing tests for sidebar buttons and view switching logic. (19f9b4f)
- [x] Task: Implement the left-aligned `SidebarWidget` with navigation buttons (Dashboard, Settings, Backups, etc.). (e6dbbe3)
- [x] Task: Implement a `QStackedWidget` in the central area to handle view transitions. (e6dbbe3)
- [x] Task: Apply initial QSS/QML styling and user-provided icons to the sidebar. (e6dbbe3)
- [x] Task: Conductor - User Manual Verification 'Phase 3: Sidebar and Navigation' (Protocol in workflow.md) (ed59e09)

## Phase 4: Recreating the Dashboard (The Mockup) [checkpoint: d7a2d61]
- [x] Task: Create `tests/ui/test_dashboard_view.py` with failing tests for dashboard components (metrics, console, massive button). (9973f60)
- [x] Task: Implement `DashboardView` widget. (2183831)
- [x] Task: Implement `MetricsWidget` with custom glowing progress bars using QSS or custom paint events. (2183831)
- [x] Task: Implement the "Orbital Launch" `ControlWidget` utilizing the caution-striped texture. (2183831)
- [x] Task: Implement the persistent `ConsoleWidget` for real-time logs. (2183831)
- [x] Task: Apply the deep space background, metallic plate backgrounds, and overall industrial QSS styling to match the mockup exactly. (2183831)
- [x] Task: Connect Controller signals (CPU/RAM updates, logs, server state) to the Dashboard UI slots. (2183831)
- [x] Task: Conductor - User Manual Verification 'Phase 4: Recreating the Dashboard (The Mockup)' (Protocol in workflow.md) (d7a2d61)

## Phase 5: Migrating Remaining Views
- [x] Task: Create test and implement `SettingsView` (mapping to INIManager). (dfced84)
- [x] Task: Create test and implement `BackupsView` (mapping to BackupManager). (dfced84)
- [x] Task: Create test and implement `SaveSyncView` (mapping to SaveSyncManager). (dfced84)
- [x] Task: Apply cohesive QSS styling to these secondary views to ensure they fit the industrial theme. (dfced84)
- [x] Task: Conductor - User Manual Verification 'Phase 5: Migrating Remaining Views' (Protocol in workflow.md) (dfced84)

## Phase 6: Cleanup and Finalization
- [x] Task: Delete all obsolete CustomTkinter code (`app.py`, old ui folders). (378ae2c)
- [x] Task: Delete legacy `test_ui.py`, `test_responsive.py`, etc., that relied on Tkinter. (378ae2c)
- [x] Task: Verify executable compilation (`build_exe.py`) works correctly with PySide6. (8f51bc3)
- [x] Task: Conductor - User Manual Verification 'Phase 6: Cleanup and Finalization' (Protocol in workflow.md) (8f51bc3)

## Phase: Review Fixes
- [x] Task: Apply review suggestions (3c8df49)