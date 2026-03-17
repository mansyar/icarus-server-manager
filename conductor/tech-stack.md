# Technology Stack

## 1. Core Language
* **Python (3.11+)**
  * Chosen for its rapid development capabilities and rich ecosystem of system management libraries.

## 2. Desktop UI Framework
* **CustomTkinter**
  * Recommended because it provides a modern, dark-mode native look while remaining significantly more lightweight (<100MB footprint) than alternatives like PyQt, perfectly aligning with the project's efficiency goals.

## 3. System Management & Core Libraries
* **psutil** & **subprocess**
  * `psutil` will be used for real-time monitoring of CPU and RAM usage.
  * `subprocess` will handle executing SteamCMD and the Icarus Dedicated Server process.

## 4. Data Storage & Configuration
* **JSON / INI files**
  * Standard `.ini` files will be used to manipulate the server's own configuration directly.
  * Application-specific settings (like backup retention limits) will be stored in lightweight `JSON` files.