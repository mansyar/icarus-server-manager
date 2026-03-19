# Specification: Player Activity Tracking & A2S Integration

## 1. Overview
The goal of this track is to implement real-time player activity tracking for the Icarus server using the `python-a2s` library. This feature provides server administrators with immediate visibility into who is currently playing, their playtime, and connection quality without needing to launch the game client.

## 2. Functional Requirements
*   **Requirement 1:** Implement a background thread dedicated to querying the running Icarus server using the Valve A2S protocol.
*   **Requirement 2:** Fetch real-time server metrics (ping, player count) and a list of currently connected players.
*   **Requirement 3:** Extract and format the following information for each connected player: Name, Playtime, and Ping/Score.
*   **Requirement 4:** Introduce a new "Players" tab in the PySide6 sidebar navigation.
*   **Requirement 5:** Display the extracted player information in a real-time updating list or table within the "Players" tab.
*   **Requirement 6:** The background A2S querying thread must poll the server every 5 seconds (aligning with the existing Monitoring Loop frequency).
*   **Requirement 7:** Gracefully handle offline or unreachable server states without crashing the application.

## 3. Non-Functional Requirements
*   **Performance:** The background A2S queries should be extremely lightweight, utilizing UDP to fetch data. Running asynchronously or on a separate thread ensures 0 UI freeze. The impact on the game server is negligible (few bytes per query).
*   **Reliability:** Network timeouts or invalid A2S responses must be caught and logged, optionally displaying an "Offline" or "Unreachable" status in the UI.

## 4. Acceptance Criteria
*   [ ] A new "Players" tab is visible and accessible from the sidebar.
*   [ ] When the Icarus server is running, the "Players" tab displays a real-time list of connected players, showing their Name, Playtime, and Ping/Score.
*   [ ] The player list updates automatically every 5 seconds.
*   [ ] If the server is offline, the "Players" tab clearly indicates that the server is currently unreachable.
*   [ ] The application UI remains responsive while the server is being queried.

## 5. Out of Scope
*   Managing (kicking/banning) players from the UI.
*   Tracking historical player data or saving play sessions to a database.