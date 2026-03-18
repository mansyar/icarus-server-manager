# Specification: GUI Overhaul - PySide6 Industrial Transition

## Overview
This track involves a complete rewrite of the Icarus Sentinel GUI, transitioning from CustomTkinter to PySide6. The primary objective is to achieve a high-fidelity, "Industrial/Skeuomorphic" visual standard identical to the provided dashboard mockup (`gui_mockup/dashboard_mockup.png`), utilizing Qt's advanced styling (QSS or QML as needed).

## Goals
- Fully migrate all application views (Dashboard, Settings, Backups, Save Sync, Mods) to PySide6.
- Accurately recreate the visual identity of the mockup, including metallic textures, glowing borders, and stylized components.
- Replace the existing UI testing suite with new PySide6-compatible tests (e.g., using `pytest-qt`) and remove obsolete CustomTkinter tests.
- Maintain existing core business logic and controller functionality during the UI swap.

## Required Assets
The following visual assets are required from the user to achieve the exact look of the mockup:
1.  **Background Texture:** Deep space/starfield background image.
2.  **Metal Plate Backgrounds:** High-resolution images (preferably 9-patch sliceable) of the metallic panels with bolts.
3.  **Action Button Texture:** The caution-striped texture for the "Initiate Orbital Launch" button.
4.  **Icons:** The "Rocket" status icon, and specific SVG icons for the sidebar navigation (Dashboard, Settings, Backups, Save Sync, Logs).
5.  **Decorative Elements:** The hex-grid background overlay and glowing orange accents (if not achievable purely via QSS/shaders).

## Functional Requirements
- **FR1: PySide6 Foundation:** Implement the main application window and core layout grid (Sidebar, Content Area) using PySide6.
- **FR2: MVC Architecture Update:** Ensure the existing `Controller` logic correctly binds to the new PySide6 view components.
- **FR3: Full View Migration:** Re-implement all functional tabs (Dashboard, Server Settings, Backups, Save Sync) within the new framework.
- **FR4: Theming and Styling:** Apply the required styling (using pure Python with QSS or QML as determined best during implementation) and user-provided graphical assets to match the target industrial aesthetic.
- **FR5: Threading Modernization:** Refactor existing background threading logic to use `QThread` and Qt signals/slots for safe UI updates.
- **FR6: UI Test Suite Replacement:** Write new unit tests to verify the functionality of the new PySide6 components. Remove all legacy Tkinter-based UI tests.

## Non-Functional Requirements
- **NFR1: Performance:** The UI must remain responsive and leverage hardware acceleration where appropriate for complex visuals.
- **NFR2: Modularity:** The new UI codebase should maintain the strict 500-line limit per file and clear separation of concerns established in previous refactoring.
- **NFR3: Visual Fidelity:** The final result must be a 1:1 visual match with the provided mockup (accounting for dynamic data).

## Out of Scope
- Adding new server management features (e.g., Player Analytics).
- Altering the core backup, steam, or resource monitoring logic, except to emit signals for the new UI.