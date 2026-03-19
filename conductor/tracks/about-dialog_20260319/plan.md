# Implementation Plan: About Dialog & Versioning System

## Phase 1: Backend System Info & Version Sourcing
- [ ] Task: Create `tests/core/test_sys_info.py` to write failing tests for reading the application version and fetching basic system info (OS, CPU, Total RAM).
- [ ] Task: Implement system info fetching and version reading logic in a suitable core module (e.g., `icarus_sentinel/core/sys_info.py` or an existing utility module).
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Backend System Info & Version Sourcing' (Protocol in workflow.md)

## Phase 2: About View UI Implementation
- [ ] Task: Create `tests/ui/test_about_view.py` with failing tests for the `AboutView` widget (verifying UI elements for version, credits, and system info are created).
- [ ] Task: Implement the `AboutView` class (inheriting from `QWidget`) in `icarus_sentinel/ui/about_view.py`, populated with the data from Phase 1 and styled with the dark charcoal/orange theme.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: About View UI Implementation' (Protocol in workflow.md)

## Phase 3: Sidebar Integration
- [ ] Task: Update `tests/ui/test_sidebar.py` (or relevant main window tests) with a failing test for the new "About" sidebar button and view routing.
- [ ] Task: Implement the "About" button in `SidebarWidget` and integrate `AboutView` into the main window's `QStackedWidget`.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Sidebar Integration' (Protocol in workflow.md)

## Phase: Review Fixes
- [ ] Task: Apply review suggestions