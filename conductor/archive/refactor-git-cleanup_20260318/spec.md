# Specification: Refactor Folder Structure and Git Cleanup

## Overview
This track addresses two primary maintenance tasks for the Icarus Sentinel project:
1.  **Refactoring the Codebase Structure**: Organizing the project using a simple flat layout with a dedicated top-level package folder (`icarus_sentinel/` at the project root).
2.  **Git Tracking Cleanup**: Addressing accidental tracking of `magicmock` files by updating `.gitignore` and clearing them from the git cache.

## Scope
*   **Code Structure Refactoring:**
    *   Ensure the main application code is properly structured within an `icarus_sentinel/` package directory at the project root.
    *   Maintain a dedicated `tests/` folder at the project root.
    *   Update any incorrect imports to align with the flat layout.
*   **Git Cleanup:**
    *   Update `.gitignore` to explicitly ignore `magicmock` files/directories and `.pytest_cache`.
    *   Execute `git rm -r --cached` to remove currently tracked `magicmock` instances without deleting local copies.

## Out of Scope
*   Transitioning to a `src/` layout.
*   Changing existing application functionality or adding new features.
*   Refactoring code logic beyond import path corrections.

## Acceptance Criteria
- [ ] Application codebase uses an `icarus_sentinel/` package at the project root.
- [ ] Tests reside in a `tests/` directory at the project root.
- [ ] All tests pass successfully.
- [ ] The application runs successfully from the root directory.
- [ ] `magicmock` files and directories are ignored in `.gitignore`.
- [ ] `magicmock` files are no longer tracked in the git repository (verified via `git status`).