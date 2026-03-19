# Implementation Plan: About Dialog & Versioning System

## Phase 1: Backend System Info & Version Sourcing [checkpoint: 3a0a079]
- [x] Task: Create `tests/core/test_sys_info.py` to write failing tests for reading the application version and fetching basic system info (OS, CPU, Total RAM). (82ca689)
- [x] Task: Implement system info fetching and version reading logic in a suitable core module (e.g., `icarus_sentinel/core/sys_info.py` or an existing utility module). (d7cf20a)
- [x] Task: Conductor - User Manual Verification 'Phase 1: Backend System Info & Version Sourcing' (Protocol in workflow.md) (3a0a079)

## Phase 2: About View UI Implementation [checkpoint: 6f734d2]
- [x] Task: Create `tests/ui/test_about_view.py` with failing tests for the `AboutView` widget (verifying UI elements for version, credits, and system info are created). (f52519f)
- [x] Task: Implement the `AboutView` class (inheriting from `QWidget`) in `icarus_sentinel/ui/about_view.py`, populated with the data from Phase 1 and styled with the dark charcoal/orange theme. (5aed86f)
- [x] Task: Conductor - User Manual Verification 'Phase 2: About View UI Implementation' (Protocol in workflow.md) (6f734d2)

## Phase 3: Sidebar Integration [checkpoint: b58e490]
- [x] Task: Update `tests/ui/test_sidebar.py` (or relevant main window tests) with a failing test for the new "About" sidebar button and view routing. (69274e1)
- [x] Task: Implement the "About" button in `SidebarWidget` and integrate `AboutView` into the main window's `QStackedWidget`. (a87d563)
- [x] Task: Conductor - User Manual Verification 'Phase 3: Sidebar Integration' (Protocol in workflow.md) (b58e490)

## Phase: Review Fixes
- [x] Task: Apply review suggestions (4a88e13)