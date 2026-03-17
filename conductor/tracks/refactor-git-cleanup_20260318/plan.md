# Implementation Plan: Refactor Folder Structure and Git Cleanup

## Phase 1: Refactor Codebase Structure
- [x] Task: Audit current directory structure
    - [x] List all Python files currently at the project root or misplaced.
    - [x] Ensure `icarus_sentinel/` and `tests/` directories exist, creating them if necessary.
- [x] Task: Relocate application code
    - [x] Move main application Python files into the `icarus_sentinel/` package directory.
    - [x] Ensure all test files are properly placed within the `tests/` directory.
- [x] Task: Clean up legacy folders
    - [x] Verify that the old `src/` folder is empty or only contains moved files.
    - [x] Delete the `src/` folder completely.
- [x] Task: Update Internal Imports
    - [ ] Search for all Python files that may have broken internal imports.
    - [ ] Refactor import statements to correctly reference the `icarus_sentinel.` package or relative imports as appropriate.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Refactor Codebase Structure' (Protocol in workflow.md)

## Phase 2: Git Tracking Cleanup
- [x] Task: Update `.gitignore`
    - [x] Add rules to ignore `magicmock` generated files and directories.
    - [x] Ensure `.pytest_cache/` is also properly ignored.
- [x] Task: Clear git cache
    - [x] Execute `git rm -r --cached` targeting the magicmock files to untrack them.
    - [x] Verify via `git status` that the files are removed from the git index but remain on the local disk.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Git Tracking Cleanup' (Protocol in workflow.md)

## Phase 3: Final Testing and Validation
- [x] Task: Run automated test suite
    - [x] Execute the test suite from the project root to ensure the new folder structure works seamlessly.
    - [x] Verify that the application can still be launched properly from the project root.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Final Testing and Validation' (Protocol in workflow.md)