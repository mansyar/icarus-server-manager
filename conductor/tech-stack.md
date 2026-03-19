# Technology Stack

## 1. Core Language
* **Python (3.11+)**
  * Chosen for its rapid development capabilities and rich ecosystem of system management libraries.
  * **Virtual Environment (`venv`):** A standard Python virtual environment is used to isolate project-specific dependencies and ensure consistency across development environments.

## 2. Desktop UI Framework
* **PySide6**
  * Chosen for its advanced styling capabilities (QSS/QML), robust signal/slot mechanism, and high-fidelity UI controls that accurately match the project's industrial dashboard mockup. It provides a more powerful and flexible foundation for professional-grade desktop applications than basic Tkinter.
  * **pytest-qt:** Used for automated UI testing of PySide6 components.

## 3. System Management & Core Libraries
* **psutil** & **subprocess**
  * `psutil`: Real-time monitoring of CPU and RAM usage.
  * `subprocess`: Executing SteamCMD and the Icarus Dedicated Server process.
* **PyInstaller**
  * Compiles the Python application into a standalone Windows executable (`.exe`).
* **winotify**
  * Used for sending Windows system notifications (toasts) for threshold alerts.
* **shutil** & **os.path**
  * Used for robust file operations and path resolution in save synchronization.
* **python-a2s**
  * Used for querying the Icarus Dedicated Server via the Valve A2S protocol to fetch real-time player counts.

## 4. Data Storage & Architecture
* **Modular Architecture**
  * The application follows a strict modular design to ensure maintainability.
  * **File Size Limit:** No single source file shall exceed 500 lines of code.
  * **Separation of Concerns:** UI components are isolated into dedicated view modules (`icarus_sentinel/ui/`), while business logic is orchestrated by a centralized `Controller`.
  * **Data Storage:** Standard `.ini` files are used for server configuration, and application-specific state is stored in lightweight `JSON` files.