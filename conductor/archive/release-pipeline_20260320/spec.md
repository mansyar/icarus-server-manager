# Specification: Release Pipeline

## 1. Overview
This track implements an automated release pipeline for the Icarus Sentinel (Server Manager) application. The goal is to streamline the compilation, packaging, and distribution of the Windows desktop application to end-users using GitHub Actions.

## 2. Functional Requirements
* **Requirement 1:** Set up a GitHub Actions workflow that triggers automatically when a new Git tag (e.g., `v1.0.0`) is pushed to the repository.
* **Requirement 2:** The workflow must extract the version number from the Git tag and dynamically inject it into the application build process (e.g., updating a `version_info.txt` or a Python version file) so the resulting `.exe` correctly reports the released version.
* **Requirement 3:** The workflow must build the Python application into a standalone Windows executable (`.exe`) using PyInstaller, consistent with the tech stack.
* **Requirement 4:** The workflow must package the compiled `.exe` along with any required external assets (if applicable) into a `.zip` archive.
* **Requirement 5:** The workflow must automatically create a new GitHub Release corresponding to the pushed tag and upload both the `.exe` and the `.zip` archive as release assets.

## 3. Non-Functional Requirements
* **Platform Match:** The build environment must run on a Windows runner (`windows-latest`) since the target platform is Windows 10/11.
* **Efficiency:** Caching should be utilized where possible for pip dependencies to speed up the workflow execution time.

## 4. Acceptance Criteria
* Pushing a new version tag triggers the release workflow.
* The workflow completes without errors.
* The application reads and displays the dynamically injected version correctly.
* A GitHub Release is created automatically with the correct tag name.
* The `.exe` and `.zip` files are attached to the GitHub Release.
* Downloading and running the `.exe` on a clean Windows machine successfully launches the Icarus Sentinel application.

## 5. Out of Scope
* Linux or macOS builds.
* Automated testing within the release pipeline (testing should be handled in a separate PR/CI pipeline prior to release tagging).