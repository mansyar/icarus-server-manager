# Implementation Plan: Advanced Log Parsing & Desktop Notifications

## Phase 1: Configuration & UI Updates [checkpoint: 226ce66]
- [x] Task: Update Configuration Model 87d3e4b
    - [ ] Write tests for new notification settings in the configuration manager.
    - [ ] Implement default settings and serialization logic for notification preferences.
- [x] Task: Implement Notifications UI in Configuration Tab fae5a59
    - [ ] Write tests to verify new UI toggle switches exist in the Configuration tab.
    - [ ] Implement the UI components (checkboxes for Server Started, Player Join/Leave, Crash/Error).
    - [ ] Connect UI signals to the configuration manager to save preferences on toggle.
- [x] Task: Conductor - User Manual Verification 'Configuration & UI Updates' (Protocol in workflow.md) 226ce66

## Phase 2: Console Color-Coding
- [x] Task: Enhance Persistent Console Widget fae5a59
    - [ ] Write tests to verify HTML/styled text injection into the console widget.
    - [ ] Implement color-coding logic (e.g., wrap incoming server logs in orange span tags, Sentinel logs in blue span tags).
    - [ ] Ensure auto-scrolling works seamlessly with styled text.
- [x] Task: Conductor - User Manual Verification 'Console Color-Coding' (Protocol in workflow.md) fae5a59

## Phase 3: Log Parsing & Notifications
- [x] Task: Implement Log Parser 3958f89
    - [ ] Write tests to simulate incoming server log strings and verify correct event extraction (Started, Join/Leave, Crash).
    - [ ] Implement non-blocking parser logic to read the `IcarusServer.exe` output stream.
- [x] Task: Integrate `winotify` 3958f89
    - [ ] Write tests/mocks for the notification dispatcher to ensure it triggers correctly.
    - [ ] Implement the notification sender using `winotify` to trigger native Windows toasts.
    - [ ] Connect the log parser events to the notification dispatcher, checking user configuration preferences first.
- [x] Task: Conductor - User Manual Verification 'Log Parsing & Notifications' (Protocol in workflow.md) 3958f89

## Phase: Review Fixes
- [x] Task: Apply review suggestions b590768