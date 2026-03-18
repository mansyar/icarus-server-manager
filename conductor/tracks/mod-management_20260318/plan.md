# Implementation Plan: Mod Management (Feature)

## Phase 1: Core Mod Logic (TDD) [checkpoint: 69ae324]
- [x] Task: Create `tests/test_mod_manager.py` with failing tests for directory resolution, folder creation, installation (copy/extract), listing, and removal. 64bfccd
- [x] Task: Implement `core/mod_manager.py` with `ModManager` class handling `install_mod`, `remove_mod`, and `list_mods`. 64bfccd
- [x] Task: Conductor - User Manual Verification 'Phase 1: Core Mod Logic' (Protocol in workflow.md) 69ae324

## Phase 2: UI Integration (TDD) [checkpoint: 6a9f8f2]
- [x] Task: Create `tests/test_mod_gui.py` with failing tests for tab structure, list display, and sync warning visibility. d608184
- [x] Task: Implement the "Mods" tab and connect it to `ModManager`. d608184
- [x] Task: Implement file picker dialog with `.pak` and `.zip` filters. d608184
- [x] Task: Update `install_mod_ui` to support multiple file selection via `askopenfilenames`. 691f74a
- [x] Task: Conductor - User Manual Verification 'Phase 2: UI Integration' (Protocol in workflow.md) 6a9f8f2

## Phase 3: Final Verification and Polishing
- [ ] Task: Run full test suite for the Mod Management feature.
- [ ] Task: Manually verify the end-to-end flow: Select Mod -> Install (Auto-create folder) -> List -> Remove.
- [ ] Task: Ensure feedback and the "Client Sync Warning" are prominent and accurate.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Final Verification and Polishing' (Protocol in workflow.md)