# Technology Stack

## 1. Core Language
* **Python (3.11+)**
  * Chosen for its rapid development capabilities and rich ecosystem of system management libraries.
  * **Virtual Environment (`venv`):** A standard Python virtual environment is used to isolate project-specific dependencies and ensure consistency across development environments.

## 2. Desktop UI Framework
* **CustomTkinter**
  * Recommended because it provides a modern, dark-mode native look while remaining significantly more lightweight (<100MB footprint) than alternatives like PyQt, perfectly aligning with the project's efficiency goals.

## 3. System Management & Core Libraries
* **psutil** & **subprocess**
  * `psutil` will be used for real-time monitoring of CPU and RAM usage.
  * `subprocess` will handle executing SteamCMD and the Icarus Dedicated Server process.
* **winotify**
  * Used for sending Windows system notifications (toasts) for threshold alerts.
* **shutil** & **os.path**
  * Used for robust file operations and path resolution in save synchronization.
* **python-a2s**
  * Used for querying the Icarus Dedicated Server via the Valve A2S protocol to fetch real-time player counts.

## 4. Data Storage & Configuration
* **JSON / INI files**
  * Standard `.ini` files will be used to manipulate the server's own configuration directly.
  * Application-specific settings (like backup retention limits) will be stored in lightweight `JSON` files.