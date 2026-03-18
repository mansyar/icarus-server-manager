# Implementation Plan: GUI Refactor - Icarus Sentinel Dashboard

## Phase 1: Foundation (Theme, Layout)
- [x] **Task: Setup Style Configuration (`style_config.py`)** dcfd3f7
    - [ ] Create `style_config.py` with hex colors and theme settings (Background, Sidebar, Accents, Typography).
    - [ ] Write tests for `style_config.py`.
    - [ ] Implement and verify style constants.
- [x] **Task: Rewrite Main Application Class (`App`)** 20b7011
    - [ ] Refactor the main entry point to use a new `App` class inheriting from `customtkinter.CTk`.
    - [ ] Write tests for `App` initialization and core structure.
    - [ ] Implement the base grid layout (Sidebar, Main Content, Bottom Console).
- [x] **Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)** 6a983eb

## Phase 2: Core UI Components Implementation
- [x] **Task: Implement Sidebar Navigation** 4536b7e
    - [ ] Implement the left-aligned `SidebarFrame` with navigation buttons (Dashboard, Settings, Backups, etc.).
    - [ ] Write tests for sidebar button interactions.
    - [ ] Style the sidebar background and buttons.
- [x] **Task: Implement Dashboard Center Metrics** a2cc55a
    - [ ] Implement `MetricsFrame` with styled horizontal `CTkProgressBar` widgets for CPU and RAM.
    - [ ] Write tests for metrics display updates.
    - [ ] Style labels and progress bars with accent colors.
- [x] **Task: Implement Server Control & Massive Button** a2cc55a
    - [ ] Implement `ControlFrame` featuring the massive "Initiate Orbital Launch" button.
    - [ ] Write tests for button callback functionality.
    - [ ] Style the button with large padding, bold fonts, and accent colors.
- [x] **Task: Implement Bottom Console** a8ae26b
    - [ ] Create a persistent `CTkTextbox` at the bottom of the window for real-time console logs.
    - [ ] Write tests for console log insertion and auto-scrolling.
    - [ ] Style the console with a pitch-black background and bright orange monospace text.
- [x] **Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)** 9c0c6dd

## Phase 3: Integration & Styling Refinement
- [x] **Task: Final Styling and Padding Adjustments** 9c0c6dd
    - [ ] Apply `corner_radius` (10-15px) to all frames and components.
    - [ ] Refine padding (`padx`, `pady`) across all sections for a clean, uncrowded feel.
    - [ ] Verify hover effects and visual feedback.
- [x] **Task: Responsive Layout Verification** 9c0c6dd
    - [ ] Ensure the UI handles resizing gracefully with appropriate weight distributions.
    - [ ] Write tests for window geometry and layout persistence.
- [x] **Task: Cleanup and Documentation** 9c0c6dd
- [x] **Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)** 7cdbb1d

## Phase: Review Fixes
- [x] Task: Apply review suggestions f90ad54
