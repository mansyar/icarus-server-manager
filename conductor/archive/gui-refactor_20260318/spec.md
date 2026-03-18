# Specification: GUI Refactor - Icarus Sentinel Dashboard

## 1. Overview
Refactor and revamp the existing CustomTkinter GUI codebase to match the style, structural layout, and overall design language of the provided reference image (`dashboard_mockup.png`). The goal is to capture the vibe, color palette, typography, and structural layout using native CustomTkinter capabilities.

## 2. Design Guidelines (Extracted from Mockup)
*   **Color Palette:**
    *   App Background: Very Dark Grey / Near Black (e.g., `#0F0F0F` or `#141414`).
    *   Sidebar Background: Dark Grey (e.g., `#1A1A1A`).
    *   Frame/Card Backgrounds: Dark Grey / Charcoal (e.g., `#222222` or `#2A2A2A`) with subtle borders.
    *   Primary Text: Light Grey / White (`#E0E0E0`).
    *   Accent/Action Color: Bright Orange (e.g., `#FF8C00` or `#F99B1C`).
    *   Console Text: Bright Orange (Terminal style).
*   **Typography:** Clean, modern Sans-serif font (e.g., 'Roboto', 'Segoe UI') for main UI. Monospace font (e.g., 'Consolas', 'Courier New') for the console.
*   **Corner Radius:** Smooth rounded corners for frames and buttons (approx. `10px` - `15px`).
*   **Progress Bars:** Thick, styled horizontal `CTkProgressBar` widgets (orange fill, dark track).

## 3. Functional Requirements
1.  **Global Styles:** Establish and apply a global color theme and typography settings based on the extracted palette.
2.  **Application Structure:** Rewrite the main CustomTkinter application class to support the new layout.
3.  **Base Grid Layout:**
    *   **Sidebar (Left):** Left-aligned navigation tab area with a distinct background color.
    *   **Main Dashboard (Center):** Large, clear UI area with generous padding (`padx`, `pady`).
    *   **Persistent Console (Bottom):** Anchored at the bottom of the main content area (or spanning full width).
4.  **Component Styling:**
    *   **Frames (`CTkFrame`):** Encapsulate logical groupings (System Status, CPU, RAM) with the defined corner radius and background colors.
    *   **Buttons (`CTkButton`):** Style with accent colors. The main "Start Server" / "Initiate Orbital Launch" button must be massive, bold, and prominent.
    *   **Meters (`CTkProgressBar`):** Use horizontal progress bars for CPU Core Load and Memory Bank Allocation to match the mockup's visual weight.
    *   **Console (`CTkTextbox`):** Pitch-black background (`#000000`), monospace font, bright terminal text color.

## 4. Non-Functional Requirements
*   **Constraint Adherence:** Strictly work within the native capabilities and constraints of `CustomTkinter`. Do not aim for a 1:1 pixel-perfect match if it requires complex custom canvas drawing that degrades maintainability.
*   **Responsiveness:** The layout should handle window resizing gracefully, keeping the sidebar fixed and expanding the main content and console areas.

## 5. Out of Scope
*   Implementing new backend logic (this track is purely a UI refactor).
