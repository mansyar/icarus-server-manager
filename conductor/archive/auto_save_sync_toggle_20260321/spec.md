# Specification: Auto-Sync Toggles for Server Start & Stop

## Overview
This feature introduces two user-configurable toggles to enable or disable the automatic synchronization of save files when the Icarus server starts or stops. This track adds these toggles to the **Save Sync** tab to give users control over the behavior defined in Requirement 4.3 of the Product Definition.

## Functional Requirements
1. **User Interface**:
   - Add two "Auto-Sync" toggle switches to the **Save Sync** tab:
     - **Sync on Start**: Controls sync when starting the server.
     - **Sync on Stop**: Controls sync when stopping the server.
   - Use high-fidelity orange/charcoal toggle switches consistent with the industrial brand identity.
2. **Core Logic**:
   - **Independent Control**: Each toggle independently controls its respective sync event.
   - **Default State (Both ON)**: Both toggles are enabled by default.
   - **Start Sync Logic**: If "Sync on Start" is ON, trigger local-to-server sync on server launch.
   - **Stop Sync Logic**: If "Sync on Stop" is ON, trigger server-to-local sync on server shutdown.
3. **Configuration Persistence**:
   - Store both toggle states in the application's settings file.
   - Ensure the settings persist across application restarts.

## Acceptance Criteria
- Two new toggle switches are present in the **Save Sync** tab.
- When a toggle is OFF, its respective server event does NOT trigger a save sync.
- When a toggle is ON (default), the corresponding server event triggers the sync operation.
- Both toggle states are correctly saved and loaded between application sessions.

## Out of Scope
- Changes to the manual "Sync Now" button functionality.
- Modifying other sync behaviors (e.g., conflict policy).
