# Specification: Save File Synchronization (Track: save-sync)

## 1. Overview
The **Save Sync** feature enables two-way synchronization of Icarus world saves (`Prospects`) between the player's local machine and the dedicated server managed by Icarus Sentinel. This allows players to move their progress seamlessly between single-player and dedicated hosting.

## 2. Functional Requirements
- **Requirement 1: SteamID Discovery (Hybrid)**
    - The application must scan `%LocalAppData%\Icarus\Saved\PlayerData\Steam\` to identify folders named with SteamIDs.
    - If multiple SteamIDs are found, provide a dropdown menu in the UI to select the correct one.
    - If only one is found, it should be selected by default.
- **Requirement 2: Sync Direction & Triggers**
    - **Local to Server (Start):** When the "Start Server" button is clicked, the application should compare the local and server save folders and sync the newest files to the server.
    - **Server to Local (Stop):** When the server is stopped, the application should sync the newest files from the server back to the local machine.
    - **Manual Trigger:** A "Sync Now" button in the dedicated "Save Sync" tab will perform a bidirectional sync (newer files overwrite older ones in either direction).
- **Requirement 3: Conflict Policy (Keep Newest)**
    - Synchronization logic must compare file modification timestamps (mtime).
    - The file with the more recent timestamp will always overwrite the older version.
- **Requirement 4: UI/UX Integration**
    - Add a new "Save Sync" tab to the application's tabbed navigation.
    - The tab should include:
        - A SteamID selector (dropdown).
        - A "Manual Sync" button.
        - Status indicators for when the last sync occurred.

## 3. Non-Functional Requirements
- **Safety:** Before overwriting any save file, the application should create a temporary backup (in memory or a hidden folder) to prevent data loss in case of a crash during the copy operation.
- **Non-blocking:** Sync operations should run in a background thread to prevent UI freezing.

## 4. Out of Scope
- Synchronizing character files (these are handled by the Icarus client/cloud).
- Support for cloud storage providers (OneDrive/Dropbox) beyond local file paths.
