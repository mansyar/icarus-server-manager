# Implementation Plan: Server Configuration & INI Management

## Phase 1: INI Parsing & Core Logic [checkpoint: 221b3c8]
- [x] Task: Create `tests/test_ini_manager.py` with failing tests for reading, parsing, and saving `ServerSettings.ini`. c594184
- [x] Task: Implement `core/ini_manager.py` using `configparser` to pass tests. c594184
- [x] Task: Update `main.py` (or relevant setup) to initialize `ini_manager` with the correct file path. c594184
- [x] Task: Conductor - User Manual Verification 'Phase 1: INI Parsing & Core Logic' (Protocol in workflow.md) 221b3c8

## Phase 2: Configuration GUI Development
- [ ] Task: Create `tests/test_config_gui.py` with failing tests for the Configuration tab structure (fields for Name, Password, Admin ID, Port, Update checkbox, Save button).
- [ ] Task: Implement the "Configuration" tab within CustomTkinter UI to pass structure tests.
- [ ] Task: Connect GUI fields to `ini_manager` state (two-way binding: populate on load, update on save).
- [ ] Task: Add failing test for "Save Changes" button triggering `ini_manager.save()`.
- [ ] Task: Implement the event handler for "Save Changes" button to pass test.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Configuration GUI Development' (Protocol in workflow.md)

## Phase 3: Advanced Editor Integration
- [ ] Task: Create `tests/test_advanced_editor.py` with failing tests for Advanced section UI (text area) and its loading/saving mechanism.
- [ ] Task: Implement the "Advanced Editor" sub-tab or section in the GUI.
- [ ] Task: Connect the text area to read raw text from `ServerSettings.ini` and save back via the "Save Changes" button.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Advanced Editor Integration' (Protocol in workflow.md)

## Phase 4: Launch-Time Updates Integration
- [ ] Task: Create/update `tests/test_server_launch.py` to add failing tests for the "Update on Launch" check before server start.
- [ ] Task: Modify the "Safe Launch" workflow to read the state of the "Update on Launch" checkbox.
- [ ] Task: Implement logic to trigger SteamCMD update (`app_update 2089300`) if the checkbox is checked, prior to spawning the server process.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Launch-Time Updates Integration' (Protocol in workflow.md)