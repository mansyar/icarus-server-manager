# Icarus Sentinel (Server Manager)

![Project Icon Placeholder](assets/app_icon.png)

## Executive Summary
**Icarus Sentinel** is a lightweight, Python-based desktop application designed to simplify the deployment and maintenance of a dedicated Icarus server. The goal is to offload game logic from the client to a dedicated process to improve FPS and stability, while automating weekly updates, save-game security, and memory optimization.

### Goals & Objectives
*   **Performance:** Offload heavy CPU/RAM calculations to a dedicated background process.
*   **Automation:** Eliminate manual SteamCMD maintenance and directory navigation.
*   **Data Integrity:** Protect player progress via automated, timestamped backups.
*   **Resource Optimization:** Active monitoring and smart-restarts to combat memory bloat.

### Target Audience
*   Solo players and small groups (2-8 players) hosting on local or secondary Windows machines.

---

## Quick Start Guide

### Prerequisites
*   Windows 10/11
*   Python 3.11+ (only if running from source)

### Installation & Launch

#### Option A: Pre-compiled Release (Recommended)
1.  **Download:** Head to the [GitHub Releases](https://github.com/mansyar/icarus-server-manager/releases) page and download the latest `IcarusSentinel.zip`.
2.  **Extract:** Unzip the archive to a folder of your choice.
3.  **Launch:** Double-click `IcarusSentinel.exe` to start the manager.

#### Option B: Running from Source
1.  **Clone:** `git clone https://github.com/mansyar/icarus-server-manager.git`
2.  **Setup Environment:**
    ```bash
    # Create and activate virtual environment
    python -m venv .venv
    .\.venv\Scripts\activate
    # Install dependencies
    pip install -r requirements.txt
    ```
3.  **Launch:** Run `python -m icarus_sentinel`.

### First Run Setup
1.  **Initialize SteamCMD:** The manager will automatically check for `steamcmd.exe`. If missing, it will download it from Valve's CDN.
2.  **Install Server:** Select an installation directory and click "Install/Update Server" to download the Icarus Dedicated Server files (15GB+).
3.  **Configure:** Use the "Configuration" tab to set your server name, password, and port.
4.  **Start:** Once installation is complete, click the "Start Server" button.

---

## Technical Stack & Architecture

### Core Technologies
*   **Language:** Python 3.11+
*   **UI Framework:** PySide6 (High-Fidelity Industrial Dashboard)
*   **Monitoring:** `psutil`
*   **Networking:** `python-a2s` (Valve A2S Protocol)
*   **Notifications:** `winotify`

### Architecture Highlights
*   **Modular Design:** No single source file exceeds 500 lines of code.
*   **Controller-View Pattern:** Business logic is decoupled from UI components.
*   **Automated Release:** CI/CD pipeline via GitHub Actions for automated Windows executable builds and versioning.

---

## Core Workflows

### 1. Safe Launch
Ensures the server is up-to-date and the system has sufficient resources before execution. Includes pre-flight RAM checks and optional "Update on Launch."

### 2. Smart Backup
Automated, timestamped ZIP backups of world saves every 30 minutes and upon shutdown. Features a configurable retention policy to manage disk space.

### 3. Save Sync
Bidirectional synchronization of world saves between local single-player and the dedicated server. Uses a "Keep Newest" conflict policy to ensure no progress is lost.

### 4. Player Tracking
Real-time monitoring of connected players, playtime, and server metrics via the A2S protocol, with integrated Windows desktop notifications for key events.

---

## Project Structure Overview

```text
icarus-server-manager/
├── .github/                 # GitHub Actions CI/CD workflows
├── assets/                  # Project icons and branding
├── conductor/               # Spec-driven development documentation
├── icarus_sentinel/         # Main application package
│   ├── core/                # Business logic (Save Sync, Mods, INI)
│   ├── ui/                  # PySide6 view components
│   ├── resources/           # Static assets and QRC
│   ├── main.py              # Application entry point
│   └── controller.py        # Orchestration layer
├── scripts/                 # Build and utility scripts
├── tests/                   # Automated test suite (pytest)
└── README.md                # (This file)
```

---

## Visual Previews

### Dashboard
![Dashboard Placeholder](https://via.placeholder.com/800x450/222222/FF9900?text=Icarus+Sentinel+Dashboard)

### Configuration
![Configuration Placeholder](https://via.placeholder.com/800x450/222222/FF9900?text=Industrial+Config+UI)

### Workflow Diagram
![Workflow Placeholder](https://via.placeholder.com/800x450/222222/FF9900?text=Safe+Launch+Logic+Flow)

---

## License
Distributed under the MIT License. See `LICENSE` (placeholder) for more information.

---
*Built with ❤️ for the Icarus community.*
