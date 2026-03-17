# Specification: Data Protection & Backups

## Overview
Implement an automated backup system for Icarus Sentinel to protect player progress. This feature includes timestamped ZIP backups of the `Prospects` folder, a configurable retention policy, and a one-click restore browser integrated into a new UI tab.

## Functional Requirements
1.  **Backup Triggers:**
    *   **Configurable Timer:** Automatically trigger backups at a user-defined interval (e.g., every 30 minutes).
    *   **On Server Stop:** Automatically create a backup whenever the server is safely stopped.
    *   **Manual Trigger:** Provide a UI button for the user to trigger an immediate backup.
2.  **Retention Policy:**
    *   Implement a "Delete Oldest" policy to enforce a configurable limit on the number of retained backups.
    *   When the limit is reached, permanently delete the oldest backup(s) without prompting to conserve space.
3.  **Backup Browser (UI):**
    *   Create a new "Backups" tab in the main application window.
    *   Display a list of available backups with their timestamps.
    *   Provide a "One-Click Restore" button for each backup.
4.  **Restore Operation:**
    *   Safely extract the selected backup ZIP to overwrite the current `Prospects` directory.
    *   **Failure Handling:** If the restore fails (e.g., due to locked files), abort the operation immediately, leave the existing files intact if possible, and display an error notification to the user.

## Non-Functional Requirements
*   **Performance:** Backup creation should run in a background thread to prevent UI freezing.
*   **Reliability:** The backup process must handle missing directories gracefully.

## Acceptance Criteria
- [ ] A background timer creates ZIP backups of the `Prospects` folder at the configured interval.
- [ ] A backup is automatically created when the server process is stopped.
- [ ] A manual "Backup Now" button functions correctly.
- [ ] The total number of backups does not exceed the configured retention limit; the oldest is deleted automatically.
- [ ] The UI has a "Backups" tab displaying the list of available backups.
- [ ] Clicking "Restore" successfully overwrites the active save data with the backup contents.
- [ ] If a restore fails, an error message is shown, and the application does not crash.

## Out of Scope
*   Cloud backup synchronization (e.g., Google Drive, Dropbox).
*   Delta/incremental backups (only full ZIP backups are supported).