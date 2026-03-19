# Specification: About Dialog & Versioning System

## Overview
Create a dedicated "About" section accessible from the application's sidebar. This fulfills the requirement to provide application versioning, developer credits, and basic system information to the user, making it easier to provide bug reports and verify the environment.

## Functional Requirements
- **Integration:** The About section must be implemented as an integrated view within the main `QStackedWidget`, acting as a new page accessible via a dedicated sidebar button.
- **Version Sourcing:** The application version must be dynamically read from an existing file (e.g., `version_info.txt` or `metadata.json`) rather than hardcoded in the UI.
- **System Information:** The view must display a basic overview of the user's system, specifically:
  - Operating System Name
  - Total RAM
  - CPU Model/Name
- **Developer Credits:** Clearly display the developer credits within the view.

## UI/UX Requirements
- **Sidebar Navigation:** Add an "About" button to the existing PySide6 sidebar.
- **Styling:** Adhere to the established PySide6 industrial/skeuomorphic dark charcoal and orange brand theme.

## Non-Functional Requirements
- Maintain lightweight performance; fetching basic system information should not noticeably block the UI.

## Acceptance Criteria
- [ ] Clicking the "About" button in the sidebar switches the main view to the About page.
- [ ] The correct application version is displayed, sourced dynamically from a configuration or version file.
- [ ] Developer credits are visible.
- [ ] Accurate basic system information (OS, Total RAM, CPU) is displayed.

## Out of Scope
- Detailed real-time hardware monitoring.
- Advanced diagnostic logging or bug report export features.