# Specification: Advanced Resource Management (Track: resource-mgmt)

## 1. Overview
This track implements advanced resource monitoring and management for the Icarus Dedicated Server, focusing on performance stability and automated maintenance (Requirements 2.2, 2.3, and 2.4 from `product.md`).

## 2. Functional Requirements
*   **Threshold Alerts (Requirement 2.2):**
    *   Monitor `IcarusServer.exe` RAM usage every 5 seconds.
    *   Trigger alerts if usage exceeds 16GB (or a configurable threshold).
    *   **Alert Channels:** Update UI label/icon (Warning state), send a Windows system notification (toast), and append a warning to the manager log.
*   **Smart Idle Restart (Requirement 2.3):**
    *   Allow the user to set a specific daily "Maintenance Time" (e.g., 4:00 AM).
    *   At the set time, the manager will query the server (A2S_INFO or RCON) to check the player count.
    *   **Logic:** If player count is **0**, initiate a server restart. If player count is **>0**, skip the restart and log the event.
*   **Pre-flight Optimization (Requirement 2.4):**
    *   Before launching the server, check system RAM availability (< 10% free threshold).
    *   **Recommendations:** If low, prompt the user with a UI dialog suggesting:
        *   Closing high-RAM applications (e.g., Chrome, Discord).
        *   Restarting the Icarus Server (if it was already running poorly).

## 3. Non-Functional Requirements
*   **Reliability:** The A2S query must handle timeouts gracefully without crashing the manager.
*   **UX:** System notifications should not spam the user (throttle to once per alert state).

## 4. Acceptance Criteria
*   [ ] Manager UI displays a warning when RAM usage exceeds the threshold.
*   [ ] Windows system notification is received upon threshold breach.
*   [ ] Smart restart occurs correctly at the scheduled time when the server is empty.
*   [ ] Smart restart is deferred if at least one player is connected.
*   [ ] Pre-flight dialog appears correctly when system RAM is low.

## 5. Out of Scope
*   Modifying Icarus game files for performance.
*   Automatic closing of other applications (suggestions only).
