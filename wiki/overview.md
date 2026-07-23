# Project Overview & Core Dashboard

## 1. Project Dashboard

- **Current Development Phase:** Application Runtime Reconstruction
- **Highest Priority Task:** Build a complete runtime message catalog by tracing every caller of `msg_manager_send_async_msg()` and identifying the meaning of each message.
- **Biggest Technical Blocker:** The semantics of runtime messages (message IDs, sender/receiver relationships, application lifecycle) remain largely undocumented despite the messaging infrastructure now being reconstructed.
- **Most Uncertain Area:** Application startup sequencing and subsystem ownership during runtime initialization.
- **Most Likely Upcoming Breakthrough:** Reconstructing the application lifecycle (`app_switch()`, `system_app_launch()`) and mapping runtime message semantics.
- **Immediate Next Experiment:** Enumerate all callers of `msg_manager_send_async_msg()` and begin constructing the runtime message catalog.

---

## 2. Global Project Milestones Matrix

| Milestone Objective | Technical Prerequisites | Phase Status | Evidence |
| :--- | :--- | :--- | :--- |
| **Reconstruct Boot & Runtime Architecture** | Boot sequence, dispatcher, messaging framework, listener registry. | **Completed** | `[E_BOOT][E_RUNTIME]` |
| **Reconstruct Application Runtime** | Message catalog, application lifecycle, subsystem ownership. | **In Progress** | `[E_RUNTIME]` |
| **Deconstruct BLE Protocol** | Document GATT services, commands, notifications, and OTA transport. | **In Progress** | `[E_BLE]` |
| **Map OTA Container Format** | Reverse engineer OTA layout, verification, and tooling. | **In Progress** | `[E_OTA]` |
| **Extract Firmware Partitions** | Parse firmware images and supporting configuration partitions. | **Completed** | `[E_FW]` |
| **Modify Watch Assets** | Understand SDFS assets and rebuild modified firmware images. | **Planned** | None |
| **Firmware Modification** | Memory map, patch locations, firmware tooling, validation. | **Planned** | None |

---

## 3. Current Architectural State

### Completed

- Boot sequence reconstructed from reset vector to `main()`.
- Runtime message receive path reconstructed.
- Runtime message send path reconstructed.
- Listener registration and lookup framework reconstructed.
- Logical application addressing (application name → thread ID) reconstructed.
- Runtime mailbox transport identified.

### Active Investigation

- Runtime message semantics.
- Application lifecycle.
- Startup initialization ordering.
- Subsystem ownership.
- Bluetooth initialization.

### Pending

- Complete message structure reconstruction.
- Complete memory map.
- Peripheral initialization.
- Firmware modification feasibility.

---

## 4. Core Structural Questions Tracker

| Question | Status | Notes |
| :--- | :--- | :--- |
| **How are applications started and switched?** | **In Progress** | Requires analysis of `app_switch()` and `system_app_launch()`. |
| **What does each runtime message represent?** | **In Progress** | Build a complete message catalog from message producers and handlers. |
| **Can custom firmware be produced?** | **Unknown** | Depends on OTA verification, image format, and patch feasibility. |
| **Can watch faces be replaced?** | **In Progress** | Requires complete understanding of SDFS assets and OTA deployment. |
| **Can OTA verification be bypassed or recreated?** | **Unknown** | Verification routines have not yet been fully reconstructed. |
| **Can display timing or refresh behaviour be modified?** | **Unknown** | Requires reverse engineering of display and configuration subsystems. |
| **Can hidden runtime features be enabled?** | **Unknown** | Depends on understanding application framework and runtime messaging. |
| **Can a serial/debug interface be exposed?** | **Unknown** | No firmware evidence yet of an accessible runtime shell or debug console. |

---

## 5. Next Major Milestone

**Application Runtime Reconstruction**

Current focus:

1. Build the runtime message catalog.
2. Reverse engineer `app_switch()`.
3. Reverse engineer `system_app_launch()`.
4. Identify application startup sequence.
5. Map subsystem ownership.
6. Correlate firmware messages with companion APK behaviour.

Completion of this milestone will transition the project from reconstructing **how the firmware communicates** to understanding **what the firmware actually does**.