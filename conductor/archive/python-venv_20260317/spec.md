# Specification: Implement Python Virtual Environment

## 1. Overview
Set up a standard Python virtual environment for the `icarus-server-manager` project to isolate dependencies, ensure consistency across environments, and simplify local development.

## 2. Functional Requirements
*   **Requirement 1:** Initialize a local Python virtual environment using the built-in `venv` module.
*   **Requirement 2:** Generate an initial `requirements.txt` file containing the core libraries defined in the Tech Stack (e.g., `customtkinter`, `psutil`, `winotify`, `python-a2s`).
*   **Requirement 3:** Create helper script(s) (e.g., `run_dev.ps1`) to automatically activate the environment and launch the application.

## 3. Non-Functional Requirements
*   **Maintainability:** The virtual environment directory (e.g., `.venv`) must be ignored by Git to prevent committing system-specific binaries and dependencies.
*   **Portability:** The setup must work natively on Windows, aligning with the project's target platform.

## 4. Acceptance Criteria
*   [ ] A `.venv` directory exists in the project root containing the isolated Python environment.
*   [ ] The `.venv` directory is explicitly added to `.gitignore`.
*   [ ] A `requirements.txt` file is present with the required core dependencies.
*   [ ] A `run_dev.ps1` script exists and successfully activates the environment (and can run a dummy main script if the app isn't built yet).

## 5. Out of Scope
*   Implementation of the application logic itself.
*   Setup of CI/CD pipelines for dependency management.