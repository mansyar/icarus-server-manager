# Implementation Plan: Server Configuration & INI Management

## Phase 1: INI Parsing & Core Logic [checkpoint: 221b3c8]
- [x] Task: Create `tests/test_ini_manager.py` with failing tests for reading, parsing, and saving `ServerSettings.ini`. c594184
- [x] Task: Implement `core/ini_manager.py` using `configparser` to pass tests. c594184
- [x] Task: Update `main.py` (or relevant setup) to initialize `ini_manager` with the correct file path. c594184
- [x] Task: Conductor - User Manual Verification 'Phase 1: INI Parsing & Core Logic' (Protocol in workflow.md) 221b3c8

## Phase 2: Configuration GUI Development [checkpoint: c5bbe74]
- [x] Task: Create `tests/test_config_gui.py` with failing tests for the Configuration tab structure (fields for Name, Password, Admin ID, Port, Update checkbox, Save button). 3b15307
- [x] Task: Implement the "Configuration" tab within CustomTkinter UI to pass structure tests. 3b15307
- [x] Task: Connect GUI fields to `ini_manager` state (two-way binding: populate on load, update on save). 3b15307
- [x] Task: Add failing test for "Save Changes" button triggering `ini_manager.save()`. 3b15307
- [x] Task: Implement the event handler for "Save Changes" button to pass test. 3b15307
- [x] Task: Conductor - User Manual Verification 'Phase 2: Configuration GUI Development' (Protocol in workflow.md) c5bbe74

## Phase 3: Advanced Editor Integration [checkpoint: 1494aae]
- [x] Task: Create `tests/test_advanced_editor.py` with failing tests for Advanced section UI (text area) and its loading/saving mechanism. 7cc574b
- [x] Task: Implement the "Advanced Editor" sub-tab or section in the GUI. 7cc574b
- [x] Task: Connect the text area to read raw text from `ServerSettings.ini` and save back via the "Save Changes" button. 7cc574b
- [x] Task: Conductor - User Manual Verification 'Phase 3: Advanced Editor Integration' (Protocol in workflow.md) 1494aae

## Phase 4: Launch-Time Updates Integration [checkpoint: 9bb6502]
- [x] Task: Create/update `tests/test_server_launch.py` to add failing tests for the "Update on Launch" check before server start. a92ed36
- [x] Task: Modify the "Safe Launch" workflow to read the state of the "Update on Launch" checkbox. a92ed36
- [x] Task: Implement logic to trigger SteamCMD update (`app_update 2089300`) if the checkbox is checked, prior to spawning the server process. a92ed36
- [x] Task: Conductor - User Manual Verification 'Phase 4: Launch-Time Updates Integration' (Protocol in workflow.md) 9bb6502

## Phase: Review Fixes
- [x] Task: Apply review suggestions c20726b