# Specification: Advanced Log Parsing & Desktop Notifications

## 1. Overview
Enhance the persistent console widget by adding logic to parse the live Icarus server logs for key events. When detected, use the `winotify` library to send native Windows desktop notifications. This ensures administrators are instantly alerted to critical server state changes, even when Icarus Sentinel is running in the background. Additionally, the persistent console output will be color-coded to differentiate between server-generated logs and Sentinel manager logs.

## 2. Functional Requirements
### 2.1 Log Parsing Logic
- Parse the incoming console output stream from the `IcarusServer.exe` process.
- Detect specific string patterns indicative of the following events:
  - **Server Started:** Log indicating the server is fully initialized and ready to accept players.
  - **Player Join/Leave:** Log indicating a player has connected or disconnected.
  - **Crash/Error:** Log indicating a fatal error or unexpected shutdown.

### 2.2 Desktop Notifications (`winotify`)
- Integrate the `winotify` Python library to generate native Windows 10/11 toast notifications.
- Notifications must be sent for the configured events regardless of the Icarus Sentinel window's current focus state (always send).
- The notification should include an appropriate icon/logo (e.g., the Icarus Sentinel logo), a clear title (e.g., "Icarus Server Alert"), and a concise message (e.g., "Player 'Bob' has connected.").

### 2.3 Color-Coded Console Output
- Apply formatting/styling to the persistent console widget text to visually distinguish log sources.
- **Server Logs:** E.g., displayed in orange text.
- **Sentinel Logs:** E.g., displayed in blue text.
- Provide a clear, readable color palette for error states (e.g., red) versus informational states (e.g., green).

### 2.4 Configuration Interface
- Add a new "Notifications" section within the existing **Configuration** tab in the UI.
- Provide toggle switches (checkboxes) to enable/disable notifications for each supported event type individually.
- Default state for new installations:
  - Server Started: **Enabled**
  - Player Join/Leave: **Enabled**
  - Crash/Error: **Enabled**
- Persist these settings to the application's configuration file (e.g., `settings.json` or `config.ini`).

## 3. Non-Functional Requirements
- **Performance:** Log parsing and UI color-coding must be efficient and non-blocking, ensuring it does not slow down the UI or the background monitoring loop. Use asynchronous or threaded processing if necessary.
- **Reliability:** Notifications should fail gracefully if the OS does not support them or if the library encounters an error, without crashing the main application.

## 4. Acceptance Criteria
- [ ] Log output is correctly parsed in real-time without missing key events.
- [ ] Windows toast notifications appear correctly when configured events occur.
- [ ] Toggling notification settings in the Configuration tab updates the behavior immediately.
- [ ] Notification settings persist across application restarts.
- [ ] Application remains responsive while parsing heavy log output.
- [ ] The console text is visually distinct, separating Sentinel logs (e.g., blue) from Server logs (e.g., orange).

## 5. Out of Scope
- Support for non-Windows operating systems (macOS/Linux).
- Email, Discord, or SMS notifications (this track is strictly for native desktop notifications).
- Customizing notification sound or appearance beyond what `winotify` provides by default.