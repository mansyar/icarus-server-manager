# Specification: Server Configuration & INI Management

## 1. Overview
This track implements the core server configuration interface (Requirements 3.1 and 3.2) and launch-time update functionality (Requirement 1.3) for Icarus Sentinel. It provides a user-friendly GUI to manage server settings, synchronizes these settings with the game's native `.ini` files, offers an advanced text-based editor, and integrates an update check before server launch.

## 2. Functional Requirements

### 2.1 Server Settings GUI (Req 3.1)
*   **Location:** Implement a new "Configuration" tab within the main application window.
*   **Fields:** Provide input fields for:
    *   Server Name
    *   Server Password
    *   Admin Password/ID
    *   Server Port
*   **Update Checkbox (Req 1.3):** Place the "Update on Launch" checkbox within this "Configuration" tab.
*   **Saving:** Implement an explicit "Save Changes" button to persist modifications.

### 2.2 INI Synchronization (Req 3.2)
*   **Parsing Strategy:** Use Python's built-in `configparser` module to read and write the server's `.ini` files (specifically `ServerSettings.ini`).
*   **Two-Way Sync:** Ensure that the GUI fields accurately reflect the current state of the `.ini` file upon load, and that saving the GUI fields writes correctly back to the file without disrupting unmanaged settings.

### 2.3 Advanced Editor (Req 3.2)
*   **Implementation:** Add an "Advanced" section (e.g., a sub-tab or distinct area within the Configuration tab).
*   **Functionality:** Display the raw `.ini` file contents in a built-in CustomTkinter text box.
*   **Editing:** Allow users to directly edit the text and save the changes back to the file using the explicit "Save Changes" button.

### 2.4 Launch-Time Updates Integration (Req 1.3)
*   **Logic:** Modify the "Safe Launch" workflow. If the "Update on Launch" checkbox is enabled, execute the SteamCMD update process (`app_update 2089300`) and await completion before spawning the server process.

## 3. Non-Functional Requirements
*   **UI Consistency:** Match the existing Modern Dark Mode aesthetic using CustomTkinter.
*   **Robustness:** Handle cases where the `.ini` file is missing or malformed gracefully.

## 4. Acceptance Criteria
*   [ ] "Configuration" tab is visible and accessible.
*   [ ] Modifying basic settings in the GUI and clicking "Save" correctly updates the `.ini` file.
*   [ ] Loading the app accurately populates the GUI from an existing `.ini` file.
*   [ ] "Advanced Editor" displays raw `.ini` text and allows direct editing and saving.
*   [ ] Checking "Update on Launch" and starting the server successfully triggers a SteamCMD update check before the server starts.
*   [ ] Unchecking "Update on Launch" bypasses the update check on launch.

## 5. Out of Scope
*   Managing other `.ini` files beyond core server settings (e.g., advanced engine tweaks).
*   Real-time validation of specific port numbers beyond basic numeric checks.