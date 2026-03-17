# Implementation Plan: Server Process Management (Track: server-mgmt)

## Phase 1: Core Process Control Logic (TDD) [checkpoint: ea1e840]
- [x] Task: Define the `ServerProcessManager` class and basic state management. (22660ff)
    - [ ] Write tests for `ServerProcessManager` initialization and state loading/saving (server_state.json).
    - [ ] Implement `ServerProcessManager` state logic.
- [x] Task: Implement Start Server functionality. (f1d664b)
    - [ ] Write tests for starting a mock process with specific flags.
    - [ ] Implement `start_server()` using `subprocess.Popen`.
- [x] Task: Implement Stop and Restart functionality. (baf66d7)
    - [ ] Write tests for graceful termination and restart logic.
    - [ ] Implement `stop_server()` (SIGTERM) and `restart_server()`.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Core Process Control Logic' (Protocol in workflow.md) (da9cfe2)

## Phase 2: Monitoring and Output Capture (TDD)
- [ ] Task: Implement Resource Monitoring.
    - [ ] Write tests for `psutil` resource usage capturing (CPU/RAM).
    - [ ] Implement background monitoring loop with 5s interval.
- [ ] Task: Implement Log Output Capture.
    - [ ] Write tests for capturing stdout/stderr from a process.
    - [ ] Implement non-blocking log reader thread.
- [ ] Task: Implement Crash Detection and Recovery.
    - [ ] Write tests for the hybrid auto-restart logic (max 3 retries).
    - [ ] Implement `_on_process_exit()` handler and recovery logic.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Monitoring and Output Capture' (Protocol in workflow.md)

## Phase 3: UI Integration and Polishing
- [ ] Task: Create UI components for server control.
    - [ ] Add Start/Stop/Restart buttons to the main CustomTkinter window.
    - [ ] Add CPU/RAM display labels.
- [ ] Task: Implement Live Console Log UI.
    - [ ] Integrate a scrollable text area for server log output.
    - [ ] Connect `ServerProcessManager` events to update the UI.
- [ ] Task: Final Verification and Integration.
    - [ ] Conduct manual end-to-end testing (Start, Stop, Monitoring, Crash).
    - [ ] Ensure persistence works: close and reopen manager while server is running.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: UI Integration and Polishing' (Protocol in workflow.md)
