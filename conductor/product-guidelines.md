# Product Guidelines

## 1. Core Principles
* **Empower the User:** Make server management accessible to everyone, regardless of their technical background.
* **Keep it Clean:** Avoid overwhelming the user with unnecessary data on the main screens.

## 2. Tone and Voice
* **Style:** Casual & Friendly
* **Guidelines:** 
  * Speak to the user like a helpful friend. 
  * Avoid overly dense technical jargon when plain English suffices.
  * Use encouraging language, especially during the initial setup phase.

## 3. Visual Branding & Theme
* **Style:** Charcoal & Orange (Modern Industrial)
* **Guidelines:**
  * Base Palette: Use `#141414` for app background and `#1A1A1A` for sidebars.
  * Accents: Use bright orange (`#FF8C00`) for primary action buttons, progress bar fills, and console text.
  * Geometry: Apply rounded corners (`10px` - `15px`) to all container frames and buttons for a modern feel.

## 4. User Experience (UX) Layout
* **Style:** Sidebar Navigation
* **Guidelines:**
  * Segment features into functional views toggled by a persistent left-aligned sidebar.
  * Ensure the "Dashboard" view provides an immediate, high-impact view of server metrics and the primary "Orbital Launch" control.
  * Use scrollable frames for dashboard views to maintain usability across various window sizes.

## 5. Error Handling & Messaging
* **Style:** Empathetic & Helpful
* **Guidelines:**
  * When errors occur, clearly explain *what* happened without blaming the user.
  * Always provide an actionable solution or a "Next Step" button (e.g., "SteamCMD failed to download. Check your internet connection and [Retry]").
  * Hide raw stack traces behind an "Advanced Details" or "View Log" button rather than displaying them immediately.