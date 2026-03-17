# Implementation Plan: Data Protection & Backups

## Phase 1: Automated Backup Engine (TDD) [checkpoint: c30d96a]
- [x] Task: Define `BackupManager` class and trigger logic [8d5a4fc]
    - [ ] Write tests for background timer interval execution and manual trigger
    - [ ] Implement `BackupManager` background thread and timer logic
- [x] Task: Implement Folder Zipping [3da0bae]
    - [ ] Write tests for archiving the `Prospects` folder using `shutil` or `zipfile`
    - [ ] Implement the archiving function, ensuring non-blocking execution
- [x] Task: Server Stop Trigger [3b117fc]
    - [ ] Write tests to verify the `BackupManager` is called when the server shuts down safely
    - [ ] Implement integration between `ServerProcessManager` (or equivalent) and `BackupManager`
- [x] Task: Conductor - User Manual Verification 'Phase 1: Automated Backup Engine' (Protocol in workflow.md) [c30d96a]

## Phase 2: Retention Policy Management (TDD)
- [x] Task: Implement 'Delete Oldest' Logic [9e045ac]
    - [ ] Write tests for identifying and deleting the oldest backup files based on a limit
    - [ ] Implement `BackupManager` logic to enforce the configurable retention limit
- [ ] Task: UI Configuration for Retention & Interval
    - [ ] Write tests for saving/loading backup settings (interval, retention limit)
    - [ ] Implement UI elements in settings to configure the backup interval and maximum backups to keep
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Retention Policy Management' (Protocol in workflow.md)

## Phase 3: Backup Browser & Restore UI (TDD)
- [ ] Task: Create 'Backups' Tab UI
    - [ ] Implement the CustomTkinter "Backups" tab in the main window
    - [ ] Implement the list view of available backups with timestamps
- [ ] Task: Implement One-Click Restore Logic
    - [ ] Write tests for extracting a backup and handling errors (e.g., locked files) safely
    - [ ] Implement the extraction logic to overwrite the active `Prospects` folder
- [ ] Task: Integrate Restore with UI
    - [ ] Wire the "Restore" button to the extraction logic and show appropriate success/error notifications
    - [ ] Add a "Backup Now" manual trigger button to the UI
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Backup Browser & Restore UI' (Protocol in workflow.md)