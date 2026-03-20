# Initial Concept

# Product Requirements Document: Icarus Sentinel (Server Manager)
**Project Status:** Draft v1.2 | **Target Platform:** Windows 10/11 | **Tech Stack:** Python

---

## 1. Executive Summary
**Icarus Sentinel** is a lightweight, Python-based desktop application designed to simplify the deployment and maintenance of a dedicated Icarus server. The goal is to offload game logic from the client to a dedicated process to improve FPS and stability, while automating weekly updates, save-game security, and memory optimization.

---

## 2. Goals & Objectives
* **Performance:** Offload heavy CPU/RAM calculations to a dedicated background process.
* **Automation:** Eliminate manual SteamCMD maintenance and directory navigation.
* **Data Integrity:** Protect player progress via automated, timestamped backups.
* **Resource Optimization:** Active monitoring and smart-restarts to combat memory bloat.

---

## 3. Target Audience
* Solo players and small groups (2-8 players) hosting on local or secondary Windows machines.

---
## 4. Functional Requirements

### 4.1 Server Lifecycle Management
* **Requirement 1.1:** Auto-install/update server via SteamCMD (AppID: 2089300).
* **Requirement 1.2:** One-click Start/Stop/Restart functionality.
* **Requirement 1.3:** Optional "Update on Launch" check.
* **Requirement 1.4:** Crash detection with optional auto-restart.

### 4.2 Smart Resource Management
* **Requirement 2.1:** Real-time RAM/CPU tracking for the `IcarusServer.exe` process.
* **Requirement 2.2:** Threshold alerts (e.g., Warning at 16GB RAM usage).
* **Requirement 2.3:** "Smart Idle Restart": Auto-restart at a set time ONLY if player count is zero.
* **Requirement 2.4:** Pre-flight system RAM check and performance optimization tips.

### 4.3 Configuration & Backup
* **Requirement 3.1:** GUI for basic settings (Name, Password, Admin ID, Port).
* **Requirement 3.2:** Advanced tab for direct `.ini` file manipulation.
* **Requirement 3.3:** Automated `.zip` backups every 30m and upon shutdown.
* **Requirement 3.4:** Backup browser with one-click restore (overwrite current save with backup).

### 4.4 Save File Synchronization
* **Requirement 4.1:** Two-way synchronization of world saves between local and server.
* **Requirement 4.2:** "Keep Newest" conflict policy based on file modification timestamps.
* **Requirement 4.3:** Automatic sync triggers on server Start (Local -> Server) and Stop (Server -> Local).
* **Requirement 4.4:** Manual sync trigger with SteamID discovery.

### 4.5 Mod Management
* **Requirement 5.1:** Dedicated "Mods" tab for installing and listing server mods.
* **Requirement 5.2:** Support for manual selection of `.pak` and `.zip` mod files.
* **Requirement 5.3:** Automatic extraction of `.pak` files from `.zip` archives.
* **Requirement 5.4:** Automatic creation of the server's mod directory if missing.
* **Requirement 5.5:** "Client Sync Warning" to inform users about mod version matching.

### 4.6 Advanced Logging & Notifications
* **Requirement 6.1:** Real-time log parsing for key server events:
    * **Server Started:** Detection of successful server initialization.
    * **Player Activity:** Detection of player join and leave events.
    * **Server Errors:** Detection of crashes or fatal log entries.
* **Requirement 6.2:** Native Windows desktop notifications (toasts) for all parsed events.
* **Requirement 6.3:** User-configurable notification toggles within the Settings tab.
* **Requirement 6.4:** Color-coded console output to distinguish between Sentinel (Blue) and Server (Orange) logs.

---

## 5. Core Workflows (The Logic Flow)

### 5.1 The "First Run" Workflow
1. User launches `IcarusSentinel.exe`.
2. Manager checks for `steamcmd.exe` in its working directory.
    * *If missing:* Manager downloads SteamCMD from Valve's official CDN.
3. Manager prompts user for an install directory.
4. Manager executes SteamCMD to download the 15GB+ Icarus Dedicated Server files.
5. Once complete, the "Start Server" button is enabled.

### 5.2 The "Safe Launch" Workflow
1. User clicks "Start Server".
2. Manager checks if "Update on Launch" is enabled.
    * *If yes:* Runs `app_update 2089300` and waits for completion.
3. Manager checks current System RAM.
    * *If < 10% free:* Alerts user of potential stability issues.
4. Manager executes the server process with specific flags (`-Log`, `-Port`, etc.).
5. Manager begins the **Monitoring Loop** (fetching CPU/RAM stats every 5 seconds).

### 5.3 The "Smart Backup" Workflow
1. **Trigger A (Timer):** Every 30 minutes.
2. **Trigger B (Manual):** User clicks "Stop Server."
3. Manager identifies the `/Saved/PlayerData/DedicatedServer/Prospects` folder.
4. Manager creates a timestamped ZIP (e.g., `Prospects_2026-03-17_1200.zip`).
5. Manager checks the "Retention Limit" (e.g., keep only the last 50 backups) and deletes the oldest if necessary.

### 5.4 The "Save Sync" Workflow
1. **Trigger A (Start):** User clicks "Start Server". Manager syncs newest local saves to the server.
2. **Trigger B (Stop):** User clicks "Stop Server". Manager syncs newest server saves back to local.
3. **Trigger C (Manual):** User clicks "Sync Now" in the Save Sync tab.
4. Manager scans `%LocalAppData%\Icarus\Saved\PlayerData` for SteamIDs.
5. Manager performs bidirectional sync, overwriting older files with newer ones.
6. Safe copy mechanism ensures backups are created before overwriting.

---

## 6. Non-Functional Requirements
* **Efficiency:** Manager RAM usage < 100MB.
* **Portability:** Single executable/folder distribution (compiled via PyInstaller, no Python install required).
* **Independence:** Server process continues running even if the Manager UI is closed.

---

## 7. Technical Architecture
* **Language:** Python 3.11+.
* **UI:** PySide6 (High-Fidelity Industrial / Skeuomorphic Aesthetic).
* **Core Libs:** `psutil` (Monitoring), `subprocess` (SteamCMD), `shutil/zipfile` (Backups), `python-a2s` (Player Query).

---

# Refined Product Guide

## 1. Executive Summary
**Icarus Sentinel** is a lightweight, Python-based desktop application designed to simplify the deployment and maintenance of a dedicated Icarus server. The goal is to offload game logic from the client to a dedicated process to improve FPS and stability, while automating weekly updates, save-game security, and memory optimization.

---

## 2. Goals & Objectives
* **Performance:** Offload heavy CPU/RAM calculations to a dedicated background process.
* **Automation:** Eliminate manual SteamCMD maintenance and directory navigation.
* **Data Integrity:** Protect player progress via automated, timestamped backups.
* **Resource Optimization:** Active monitoring and smart-restarts to combat memory bloat.

---

## 3. Target Audience
* Solo players and small groups (2-8 players) hosting on local or secondary Windows machines.

---
## 4. Functional Requirements

### 4.1 Server Lifecycle Management
* **Requirement 1.1:** Auto-install/update server via SteamCMD (AppID: 2089300).
* **Requirement 1.2:** One-click Start/Stop/Restart functionality.
* **Requirement 1.3:** Optional "Update on Launch" check with real-time log streaming.
* **Requirement 1.4:** Crash detection with optional auto-restart. Specifically, implement a **Hybrid** recovery system that auto-restarts the server up to 3 times before prompting the user if failures continue.

### 4.2 Smart Resource Management
* **Requirement 2.1:** Real-time RAM/CPU tracking for the `IcarusServer.exe` process.
* **Requirement 2.2:** Threshold alerts (e.g., Warning at 16GB RAM usage).
* **Requirement 2.3:** "Smart Idle Restart": Auto-restart at a set time ONLY if player count is zero.
* **Requirement 2.4:** Pre-flight system RAM check and performance optimization tips.

### 4.3 Configuration & Backup
* **Requirement 3.1:** GUI for basic settings (Name, Password, Admin ID, Port).
* **Requirement 3.2:** Advanced tab for direct `.ini` file manipulation.
* **Requirement 3.3:** Automated `.zip` backups every 30m and upon shutdown.
* **Requirement 3.4:** Backup browser with one-click restore (overwrite current save with backup).
* **Requirement 3.5:** Backup Retention: Permanently **Delete Oldest** backups when the retention limit is reached to save space.

### 4.4 UI/UX Experience
* **Requirement 4.1:** **Detailed Feedback:** Display real-time console output from SteamCMD and server initialization within a persistent, monospace orange-on-black textbox anchored at the bottom of the window.
* **Requirement 4.2:** **Sidebar-Driven Navigation:** Utilize a fixed left-aligned sidebar for primary navigation, separating functional views (Dashboard, Configuration, Save Sync, etc.) without top-level tabs. Use color-coded legend (Sentinel, Server, Success, Error) for the console.
* Requirement 4.3: **Brand Visual Identity:** Apply a consistent dark charcoal and orange brand theme across the application, featuring massive, bold action buttons and horizontal progress bars for resource metrics.
* **Requirement 4.4.1:** **Unified Iconography:** Use the official rocket icon (`assets/app_icon.png`) as the window icon, taskbar identifier, and within the UI (About dialog, Splash Screen) to solidify brand identity.
* Requirement 4.4: **About & Versioning:** Clearly display the application version and provide an "About" dialog for credits and system information.

* **Requirement 4.5:** **Player Activity Tracking:**
    * **Requirement 4.5.1:** Implement a background A2S query service to fetch real-time server metrics (ping, player count) and player lists.
    * **Requirement 4.5.2:** Dedicated "Players" tab for displaying connected player names, playtime, and scores.
    * **Requirement 4.5.3:** Automatic UI updates every 5 seconds without blocking the main thread.
    * **Requirement 4.5.4:** Graceful handling of offline or unreachable server states with clear UI feedback.
* **Requirement 4.6:** **Desktop Notifications:** Integrated Windows toast notifications for server lifecycle and player events, configurable by the user.

### 4.7 Automated Release Pipeline
* **Requirement 7.1:** Automated build and packaging of the application into a standalone Windows executable.
* **Requirement 7.2:** Dynamic version injection into the executable and application metadata from Git tags.
* **Requirement 7.3:** Automated GitHub Release creation with attached artifacts (EXE and ZIP) upon tagging a new version (e.g., `v1.2.3`).

### 4.6 Mod Management
* **Requirement 5.1:** Dedicated "Mods" tab for installing and listing server mods.
* **Requirement 5.2:** Support for manual selection of `.pak` and `.zip` mod files.
* **Requirement 5.3:** Automatic extraction of `.pak` files from `.zip` archives.
* **Requirement 5.4:** Automatic creation of the server's mod directory if missing.
* **Requirement 5.5:** "Client Sync Warning" to inform users about mod version matching.

---

## 5. Core Workflows (The Logic Flow)

### 5.1 The "First Run" Workflow
1. User launches `IcarusSentinel.exe`.
2. Manager checks for `steamcmd.exe` in its working directory.
    * *If missing:* Manager downloads SteamCMD from Valve's official CDN.
3. Manager prompts user for an install directory.
4. Manager executes SteamCMD to download the 15GB+ Icarus Dedicated Server files.
5. Once complete, the "Start Server" button is enabled.

### 5.2 The "Safe Launch" Workflow
1. User clicks "Start Server".
2. Manager checks if "Update on Launch" is enabled.
    * *If yes:* Runs `app_update 2089300` and waits for completion.
3. Manager checks current System RAM.
    * *If < 10% free:* Alerts user of potential stability issues.
4. Manager executes the server process with specific flags (`-Log`, `-Port`, etc.).
5. Manager begins the **Monitoring Loop** (fetching CPU/RAM stats every 5 seconds).

### 5.3 The "Smart Backup" Workflow
1. **Trigger A (Timer):** Every 30 minutes.
2. **Trigger B (Manual):** User clicks "Stop Server."
3. Manager identifies the `/Saved/PlayerData/DedicatedServer/Prospects` folder.
4. Manager creates a timestamped ZIP (e.g., `Prospects_2026-03-17_1200.zip`).
5. Manager checks the "Retention Limit" (e.g., keep only the last 50 backups) and deletes the oldest if necessary.

### 5.4 The "Save Sync" Workflow
1. **Trigger A (Start):** User clicks "Start Server". Manager syncs newest local saves to the server.
2. **Trigger B (Stop):** User clicks "Stop Server". Manager syncs newest server saves back to local.
3. **Trigger C (Manual):** User clicks "Sync Now" in the Save Sync tab.
4. Manager scans `%LocalAppData%\Icarus\Saved\PlayerData` for SteamIDs.
5. Manager performs bidirectional sync, overwriting older files with newer ones.
6. Safe copy mechanism ensures backups are created before overwriting.

---

## 6. Non-Functional Requirements
* **Efficiency:** Manager RAM usage < 100MB.
* **Portability:** Single executable/folder distribution (compiled via PyInstaller, no Python install required).
* **Independence:** Server process continues running even if the Manager UI is closed.

---

## 7. Technical Architecture
* **Language:** Python 3.11+.
* **UI:** PySide6 (High-Fidelity Industrial / Skeuomorphic Aesthetic).
* **Core Libs:** `psutil` (Monitoring), `subprocess` (SteamCMD), `shutil/zipfile` (Backups), `python-a2s` (Player Query).

---

## 8. Future Roadmap
* **Auto-Discovery:** Automatically find the server executable without manual pathing.
