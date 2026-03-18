# Implementation Plan: Mod Management (Feature)

## Phase 1: Core Mod Logic (TDD)
- [ ] Task: Create `tests/test_mod_manager.py` with failing tests for directory resolution, folder creation, installation (copy/extract), listing, and removal.
- [ ] Task: Implement `core/mod_manager.py` with `ModManager` class handling `install_mod`, `remove_mod`, and `list_mods`.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Core Mod Logic' (Protocol in workflow.md)

## Phase 2: UI Integration (TDD)
- [ ] Task: Create `tests/test_mod_gui.py` with failing tests for tab structure, list display, and sync warning visibility.
- [ ] Task: Implement the "Mods" tab and connect it to `ModManager`.
- [ ] Task: Implement file picker dialog with `.pak` and `.zip` filters.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: UI Integration' (Protocol in workflow.md)

## Phase 3: Final Verification and Polishing
- [ ] Task: Run full test suite for the Mod Management feature.
- [ ] Task: Manually verify the end-to-end flow: Select Mod -> Install (Auto-create folder) -> List -> Remove.
- [ ] Task: Ensure feedback and the "Client Sync Warning" are prominent and accurate.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Final Verification and Polishing' (Protocol in workflow.md)