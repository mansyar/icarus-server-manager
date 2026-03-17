# Implementation Plan: Refactor Folder Structure and Git Cleanup

## Phase 1: Refactor Codebase Structure
- [ ] Task: Audit current directory structure
    - [ ] List all Python files currently at the project root or misplaced.
    - [ ] Ensure `icarus_sentinel/` and `tests/` directories exist, creating them if necessary.
- [ ] Task: Relocate application code
    - [ ] Move main application Python files into the `icarus_sentinel/` package directory.
    - [ ] Ensure all test files are properly placed within the `tests/` directory.
- [ ] Task: Clean up legacy folders
    - [ ] Verify that the old `src/` folder is empty or only contains moved files.
    - [ ] Delete the `src/` folder completely.
- [ ] Task: Update Internal Imports
    - [ ] Search for all Python files that may have broken internal imports.
    - [ ] Refactor import statements to correctly reference the `icarus_sentinel.` package or relative imports as appropriate.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Refactor Codebase Structure' (Protocol in workflow.md)

## Phase 2: Git Tracking Cleanup
- [ ] Task: Update `.gitignore`
    - [ ] Add rules to ignore `magicmock` generated files and directories.
    - [ ] Ensure `.pytest_cache/` is also properly ignored.
- [ ] Task: Clear git cache
    - [ ] Execute `git rm -r --cached` targeting the magicmock files to untrack them.
    - [ ] Verify via `git status` that the files are removed from the git index but remain on the local disk.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Git Tracking Cleanup' (Protocol in workflow.md)

## Phase 3: Final Testing and Validation
- [ ] Task: Run automated test suite
    - [ ] Execute the test suite from the project root to ensure the new folder structure works seamlessly.
    - [ ] Verify that the application can still be launched properly from the project root.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Final Testing and Validation' (Protocol in workflow.md)