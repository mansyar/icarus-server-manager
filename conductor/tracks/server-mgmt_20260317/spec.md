# Specification: Server Process Management (Track: server-mgmt)

## Overview
Implement the core logic and UI components to start, stop, and monitor the Icarus Dedicated Server process. This track focuses on reliable process lifecycle management, resource monitoring, and a transparent user interface for server status.

## Functional Requirements
- **Process Lifecycle:**
    - Start the `IcarusServer.exe` process with configurable flags (`-Log`, `-Port`, `-QueryPort`, etc.).
    - Gracefully stop the server using `SIGTERM` (standard termination signal).
    - Maintain a persistent state (JSON) of the server's running status (PID, status) to allow recovery if the manager is restarted.
- **Monitoring & Recovery:**
    - Implement a monitoring loop (default interval: 5 seconds) using `psutil` to track CPU and RAM usage of the server process.
    - Implement a hybrid auto-restart system: Automatically restart the server up to 3 times upon crash before prompting the user for intervention.
- **Logging:**
    - Capture and display the real-time console output (stdout/stderr) from the server process within the manager UI.

## UI/UX Requirements
- **Control Buttons:** Implementation of "Start", "Stop", and "Restart" buttons in the manager UI.
- **Resource Stats:** Dynamic display (labels or progress bars) showing current CPU (%) and RAM (GB) usage of the server process.
- **Console Output:** A scrollable, read-only text area that displays the live log output from the server.

## Technical Implementation Details
- **Libraries:** `subprocess.Popen` for process execution, `psutil` for monitoring.
- **State Storage:** `server_state.json` in the application root or a designated data folder.
- **Thread Management:** Monitoring and log capturing should run in background threads to keep the UI responsive.

## Acceptance Criteria
1. The user can start the Icarus server from the UI, and the console log begins to populate.
2. The UI correctly displays real-time CPU and RAM usage for the server process.
3. Clicking "Stop" gracefully shuts down the server.
4. If the server crashes, the manager attempts to restart it automatically (up to 3 times).
5. If the manager is closed and reopened while the server is running, it correctly identifies the existing process and resumes monitoring.

## Out of Scope
- Server installation/updating (handled in a separate track).
- Backup and restore logic (handled in a separate track).
- Advanced .ini file editing UI.
