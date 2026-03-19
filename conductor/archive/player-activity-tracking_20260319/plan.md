# Implementation Plan: Player Activity Tracking & A2S Integration

## Phase 1: Background A2S Query Integration [checkpoint: c926347]
- [x] Task: Implement A2S Querying Logic 580b7b0
    - [x] Write failing unit tests for fetching server metrics and player list using `python-a2s` (mocking the server response).
    - [x] Implement the `A2SQueryService` to fetch and parse Name, Playtime, and Ping/Score.
    - [x] Ensure tests pass and the service gracefully handles network timeouts.
- [x] Task: Implement Background Query Thread 84fb096
    - [x] Write failing tests for a background worker thread that polls the `A2SQueryService` every 5 seconds.
    - [x] Implement the threaded worker using PySide6 `QThread` or Python `threading` with signals to emit data.
    - [x] Ensure tests pass.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Background A2S Query Integration' (Protocol in workflow.md)

## Phase 2: UI "Players" Tab Implementation [checkpoint: a308cb7]
- [x] Task: Create "Players" View Component 461b447
    - [x] Write UI tests (using `pytest-qt`) to verify the existence of a new "Players" tab in the sidebar navigation.
    - [x] Update the main UI layout to include the "Players" tab navigation item.
    - [x] Implement the "Players" view with a table or list widget containing columns for Name, Playtime, and Ping/Score.
    - [x] Ensure UI tests pass.
- [x] Task: Implement UI Error State 461b447
    - [x] Write UI tests for an "Offline/Unreachable" status indicator within the "Players" tab.
    - [x] Implement the offline indicator state in the UI.
    - [x] Ensure UI tests pass.
- [x] Task: Conductor - User Manual Verification 'Phase 2: UI "Players" Tab Implementation' (Protocol in workflow.md)

## Phase 3: Connect Logic to UI [checkpoint: 6673831]
- [x] Task: Bind Background Thread Signals to UI 4b40549
    - [x] Write integration tests verifying that signals emitted by the background thread update the "Players" view model/table.
    - [x] Connect the background thread's data signal to the UI table population logic.
    - [x] Connect the background thread's error signal to the "Offline/Unreachable" UI state.
    - [x] Ensure all tests pass.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Connect Logic to UI' (Protocol in workflow.md)