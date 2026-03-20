# Implementation Plan: Auto-Sync Toggles for Server Start & Stop

## Phase 1: Data Model & Persistence [checkpoint: f5c7c6f]
- [x] Task: Update `ServerProcessManager` State (5dbdf97)
    - Add `auto_sync_on_start`, `auto_sync_on_stop`, and `selected_steam_id` to `ServerProcessManager`.
    - Update `load_state` and `save_state` in `icarus_sentinel/server_manager.py`.
- [x] Task: Update `Controller` Settings Logic (9248c42)
    - Update `save_sentinel_settings` in `icarus_sentinel/controller.py` to handle the new settings.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Data Model & Persistence' (f5c7c6f)

## Phase 2: Core Logic (Auto-Sync Triggers) [checkpoint: 78d0698]
- [x] Task: Implement Sync on Start (52a1992)
    - Modify `MainWindow._on_launch_clicked` in `icarus_sentinel/ui/main_window.py`.
    - If `auto_sync_on_start` is enabled, call `controller.sync_saves` and wait for completion before calling `controller.run_server`.
- [x] Task: Implement Sync on Stop (52a1992)
    - Modify `MainWindow._on_launch_clicked` (stop case) in `icarus_sentinel/ui/main_window.py`.
    - If `auto_sync_on_stop` is enabled, call `controller.sync_saves` after stopping the server.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Core Logic (Auto-Sync Triggers)' (78d0698)

## Phase 3: UI Implementation [checkpoint: c080760]
- [x] Task: Create `ToggleSwitch` Component (151bca3)
    - Create `icarus_sentinel/ui/components.py` with a custom styled toggle switch (orange/charcoal).
- [x] Task: Update `SaveSyncView` UI (f940c14)
    - Add the two toggles and a SteamID selection memory to `icarus_sentinel/ui/save_sync.py`.
    - Ensure the toggles and selection are connected to save their state.
- [x] Task: Conductor - User Manual Verification 'Phase 3: UI Implementation' (c080760)

## Phase 4: Final Verification
- [ ] Task: Unit & Integration Tests
    - Create `tests/test_auto_sync_toggles.py`.
    - Verify settings persistence and trigger logic.
- [ ] Task: Documentation & Cleanup
    - Update documentation if necessary and perform final code review.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Final Verification' (Protocol in workflow.md)
