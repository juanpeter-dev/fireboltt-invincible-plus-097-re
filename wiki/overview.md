# Project Overview & Core Dashboard

## 1. Project Dashboard
- **Current Development Phase:** Runtime Architecture Reconstruction
- **Highest Priority Task:** Reverse engineer the runtime message framework by tracing how messages are produced, queued, and dispatched through `main_msg_proc`.
- **Biggest Technical Blocker:** SQLite database tables inside `map_cache.db` utilize cryptographically wrapped storage fields at rest, preventing direct offline extraction of server JSON payloads.
- **Most Uncertain Area:** The internal peripheral initialization parameters and clock tree parameters allocated inside `extcfg.bin`.
- **Most Likely Upcoming Breakthrough:** Identifying the underlying message queue implementation and mapping how subsystem events enter the runtime dispatcher.
- **Immediate Next Experiment:** Analyze `msg_manager_receive_msg()` and trace the underlying queue implementation if it is a wrapper.

## 2. Global Project Milestones Matrix

| Milestone Objective | Technical Prerequisites | Phase Status | Sourced Evidence |
| :--- | :--- | :--- | :--- |
| **Deconstruct BLE Protocol** | Map out commands, notifications, and device syncing handshakes over Bluetooth characteristics. | **In Progress** | `[E003]` |
| **Map OTA Archive Format** | Unpack nested file segments out of the vendor's update file layout structures. | **Verified** | `[E004]` |
| **Extract Firmware Partitions** | Parse the flat SDFS system layout arrays to access localized configuration blocks. | **Verified** | `[E006][E007][E008][E009]` |
| **Modify Watch Assets** | Rebuild an SDFS binary asset cluster with custom image assets and deploy to hardware. | **Unverified** | None |
| **Tweak Display Timing Parameters** | Locate display timing registers inside the configuration tables to adjust refresh rates. | **In Progress** | `[E001]` |

## 3. Core Structural Questions Tracker
- **Can we replace watch faces?** *Status: Unverified.* Requires isolating a raw watch face binary packet from network logs to verify our custom SDFS insertion code works.
- **Can we bypass OTA container checks?** *Status: Unknown.* We haven't located the validation code routines (like checksums or cryptographic signatures) inside the watch's internal bootloader code yet.
- **Can we change screen refresh clocks?** *Status: Unverified.* We have not conclusively linked specific register bytes in `extcfg.bin` directly to the display controller hardware hardware pipelines.
- **Can we access a serial shell console?** *Status: Unknown.* No serial debugging shell or interface listeners have been exposed via system software connections yet.