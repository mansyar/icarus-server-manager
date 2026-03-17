# Implementation Plan: Advanced Resource Management (Track: resource-mgmt)

## Phase 1: Threshold Alerts & UI Feedback (TDD) [checkpoint: ]
- [x] Task: Extend `ServerProcessManager` to handle threshold alerts. (0add448)
    - [x] Write tests for `ServerProcessManager` monitoring logic with thresholds.
    - [x] Implement threshold monitoring and state update (Warning state).
- [x] Task: Implement Windows Notification Support. (e8b215a)
    - [x] Write tests for `NotificationManager` (mocking system toast calls).
    - [x] Implement system notifications for threshold breaches.
- [ ] Task: Update UI for Threshold States.
    - [ ] Add visual indicators (color/icon change) for RAM threshold alerts.
    - [ ] Connect threshold state to the manager log.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Threshold Alerts & UI Feedback' (Protocol in workflow.md)

## Phase 2: Smart Idle Restart & Active Query (TDD) [checkpoint: ]
- [ ] Task: Implement A2S Query Client for Player Count.
    - [ ] Write tests for querying a mock A2S_INFO server.
    - [ ] Implement `A2SClient` to fetch current player count.
- [ ] Task: Implement Smart Restart Scheduler.
    - [ ] Write tests for scheduled restart logic (time comparison, player count check).
    - [ ] Implement background timer/scheduler for maintenance time checks.
- [ ] Task: UI for Smart Restart Configuration.
    - [ ] Add time selection widget (e.g., dropdowns for HH:MM) to the manager settings.
    - [ ] Add a toggle for 'Enable Smart Idle Restart'.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Smart Idle Restart & Active Query' (Protocol in workflow.md)

## Phase 3: Pre-flight Optimization Dialogs (TDD) [checkpoint: ]
- [ ] Task: Implement System RAM Pre-flight Check.
    - [ ] Write tests for checking system RAM percentage and thresholds.
    - [ ] Implement `check_system_ram()` logic.
- [ ] Task: Create Optimization UI Dialog.
    - [ ] Design and implement a CustomTkinter dialog for RAM recommendations.
    - [ ] Trigger dialog if system RAM is < 10% before server launch.
- [ ] Task: Final Integration and Performance Verification.
    - [ ] Conduct E2E testing: Threshold alerts, scheduled restart (with/without players), and low-RAM pre-flight.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Pre-flight Optimization Dialogs' (Protocol in workflow.md)
