# Implementation Plan: Player Activity Tracking & A2S Integration

## Phase 1: Background A2S Query Integration
- [x] Task: Implement A2S Querying Logic 580b7b0
    - [x] Write failing unit tests for fetching server metrics and player list using `python-a2s` (mocking the server response).
    - [x] Implement the `A2SQueryService` to fetch and parse Name, Playtime, and Ping/Score.
    - [x] Ensure tests pass and the service gracefully handles network timeouts.
- [x] Task: Implement Background Query Thread 84fb096
    - [x] Write failing tests for a background worker thread that polls the `A2SQueryService` every 5 seconds.
    - [x] Implement the threaded worker using PySide6 `QThread` or Python `threading` with signals to emit data.
    - [x] Ensure tests pass.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Background A2S Query Integration' (Protocol in workflow.md)

## Phase 2: UI "Players" Tab Implementation
- [ ] Task: Create "Players" View Component
    - [ ] Write UI tests (using `pytest-qt`) to verify the existence of a new "Players" tab in the sidebar navigation.
    - [ ] Update the main UI layout to include the "Players" tab navigation item.
    - [ ] Implement the "Players" view with a table or list widget containing columns for Name, Playtime, and Ping/Score.
    - [ ] Ensure UI tests pass.
- [ ] Task: Implement UI Error State
    - [ ] Write UI tests for an "Offline/Unreachable" status indicator within the "Players" tab.
    - [ ] Implement the offline indicator state in the UI.
    - [ ] Ensure UI tests pass.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: UI "Players" Tab Implementation' (Protocol in workflow.md)

## Phase 3: Connect Logic to UI
- [ ] Task: Bind Background Thread Signals to UI
    - [ ] Write integration tests verifying that signals emitted by the background thread update the "Players" view model/table.
    - [ ] Connect the background thread's data signal to the UI table population logic.
    - [ ] Connect the background thread's error signal to the "Offline/Unreachable" UI state.
    - [ ] Ensure all tests pass.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Connect Logic to UI' (Protocol in workflow.md)