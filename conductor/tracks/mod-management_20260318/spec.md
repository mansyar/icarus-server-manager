# Specification: Mod Management (Feature)

## Overview
This feature adds a new "Mods" tab to the Icarus Sentinel UI, allowing users to manually select local mod files (specifically `.pak` files or `.zip` archives containing them) and have the manager automatically install them into the server's mod directory.

## Functional Requirements
- **Requirement 1:** A new top-level "Mods" tab in the CustomTkinter UI.
- **Requirement 2:** A "Select Mod" button with a file picker supporting multiple `.pak` and `.zip` files.
- **Requirement 3:** **Automatic Installation:** 
    - Create the `\Icarus\Content\Paks\mods` directory if it does not exist.
    - If a `.zip` file is selected, extract the `.pak` file(s) from it.
    - Move/Copy the `.pak` files into the `mods` directory.
- **Requirement 4:** A list view displaying currently installed `.pak` files in the server's `mods` directory.
- **Requirement 5:** An "Uninstall" or "Remove" button to delete specific `.pak` files.
- **Requirement 6:** **User Warning:** Display a clear warning in the UI that players joining the server must have the exact same `.pak` files installed locally to prevent version mismatch crashes.

## Acceptance Criteria
1. User can click a "Mods" tab.
2. User can select a `.pak` or `.zip` file from their local disk.
3. Clicking "Install" successfully places the `.pak` file in `[ServerRoot]\Icarus\Content\Paks\mods`.
4. The manager creates the `mods` folder if it's missing.
5. Installed mods are correctly listed in the UI.
6. Clicking "Remove" deletes the mod file from the server's directory.
7. A sync warning is clearly visible to the user.

## Out of Scope
- Automatic version checking from websites (Nexus, CurseForge, etc.).
- Mod conflict detection.
- Mod dependency management.