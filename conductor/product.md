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

---

## 5. Core Workflows (The Logic Flow)

### 5.1 The "First Run" Workflow
1. User launches `IcarusSentinel.exe`.
2. Manager checks for `steamcmd.exe` in the root folder.
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

---

## 6. Non-Functional Requirements
* **Efficiency:** Manager RAM usage < 100MB.
* **Portability:** Single executable/folder distribution (No Python install required).
* **Independence:** Server process continues running even if the Manager UI is closed.

---

## 7. Technical Architecture
* **Language:** Python 3.11+.
* **UI:** CustomTkinter (Modern Dark Mode).
* **Core Libs:** `psutil` (Monitoring), `subprocess` (SteamCMD), `shutil/zipfile` (Backups).

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
* **Requirement 1.3:** Optional "Update on Launch" check.
* **Requirement 1.4:** Crash detection with optional auto-restart. Specifically, implement a **Hybrid** recovery system that auto-restarts the server up to 3 times before prompting the user if failures continue.

### 4.2 Smart Resource Management
* **Requirement 2.1:** Real-time RAM/CPU tracking for the `IcarusServer.exe` process.
* **Requirement 2.2:** Threshold alerts (e.g., Warning at 16GB RAM usage).
* **Requirement 2.3:** "Smart Idle Restart": Auto-restart at a set time ONLY if player count is zero.
* **Requirement 2.4:** Pre-flight system RAM check and performance optimization tips.

### 4.3 Configuration & Backup
* **Requirement 3.1:** GUI for basic settings (Name, Password, Admin ID, Port).
* **Requirement 3.2:** Advanced tab for direct `.ini` file manipulation.
* **Requirement 3.3:** Automated `.zip backups every 30m and upon shutdown.
* **Requirement 3.4:** Backup browser with one-click restore (overwrite current save with backup).
* **Requirement 3.5:** Backup Retention: Permanently **Delete Oldest** backups when the retention limit is reached to save space.

### 4.4 UI/UX Experience
* **Requirement 4.1:** **Detailed Feedback:** Display real-time console output from SteamCMD and server initialization within a persistent scrollable text box at the bottom of the application window.
* **Requirement 4.2:** **Tabbed Navigation:** Use a tabbed interface to separate core server management from advanced features like the backup browser.

---

## 5. Core Workflows (The Logic Flow)

### 5.1 The "First Run" Workflow
1. User launches `IcarusSentinel.exe`.
2. Manager checks for `steamcmd.exe` in the root folder.
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

---

## 6. Non-Functional Requirements
* **Efficiency:** Manager RAM usage < 100MB.
* **Portability:** Single executable/folder distribution (No Python install required).
* **Independence:** Server process continues running even if the Manager UI is closed.

---

## 7. Technical Architecture
* **Language:** Python 3.11+.
* **UI:** CustomTkinter (Modern Dark Mode).
* **Core Libs:** `psutil` (Monitoring), `subprocess` (SteamCMD), `shutil/zipfile` (Backups).

---

## 8. Future Roadmap
* **Mod Management:** Support for installing and updating Icarus server mods directly within the manager.
* **Player Activity Tracking:** Track player join/leave events and display a live player list in the UI.