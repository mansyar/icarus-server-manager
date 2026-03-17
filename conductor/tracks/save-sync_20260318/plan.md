# Implementation Plan: Save File Synchronization (Track: save-sync)

## Phase 1: Core Save Sync Logic (TDD) [checkpoint: 75a03dd]
- [x] Task: Implement `SaveSyncManager` for path resolution and file discovery. daa900e
    - [x] Write tests for identifying local SteamID folders.
    - [x] Implement `list_local_steam_ids()` and `get_local_save_path()`.
- [x] Task: Implement Bidirectional Sync Logic with Conflict Policy. 003fd11
    - [x] Write tests for comparing file timestamps and determining "newest" file.
    - [x] Implement `sync_prospects(local_path, server_path, direction)` logic.
    - [x] Ensure safe copy (temporary backup during overwrite).
- [x] Task: Conductor - User Manual Verification 'Phase 1: Core Save Sync Logic' (Protocol in workflow.md) 75a03dd

## Phase 2: Application Workflow Integration
- [ ] Task: Integrate Save Sync with Server Lifecycle.
    - [ ] Modify `app.py` to trigger sync from Local to Server on "Start Server".
    - [ ] Modify `app.py` to trigger sync from Server to Local on "Stop Server".
    - [ ] Ensure sync operations run in background threads to keep UI responsive.
- [ ] Task: Implement Manual Sync Trigger and Status Tracking.
    - [ ] Add `perform_manual_sync()` method to `App` class.
    - [ ] Track `last_sync_timestamp` in `server_state.json`.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Application Workflow Integration' (Protocol in workflow.md)

## Phase 3: UI Development: "Save Sync" Tab
- [ ] Task: Create the "Save Sync" tab in CustomTkinter.
    - [ ] Implement the UI layout with a dropdown for SteamID selection and a "Sync Now" button.
    - [ ] Add a "Last Sync" label and status indicator.
- [ ] Task: Connect UI to `SaveSyncManager` and State.
    - [ ] Populate the SteamID dropdown on app launch.
    - [ ] Wire the "Sync Now" button to the manual sync logic.
- [ ] Task: Final End-to-End Verification and Polishing.
    - [ ] Conduct E2E testing for all triggers (Start, Stop, Manual).
    - [ ] Verify non-blocking behavior during large file copies.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: UI Development: "Save Sync" Tab' (Protocol in workflow.md)

## Phase: Review Fixes
- [ ] Task: Apply review suggestions
