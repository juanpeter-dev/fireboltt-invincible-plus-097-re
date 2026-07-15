# Project Task Ledger & Sprint Board

This document tracks active technical backlogs, experimental verification gates, and immediate priorities. Tasks are organized by development phase to guide both human researchers and automated AI agents.

---

## 🟥 Current Sprint Priorities (Immediate Actions)
- [ ] Reverse engineer main_msg_proc()
- [ ] Identify runtime message dispatch architecture.
- [ ] Map subsystem ownership.
- [ ] Locate vendor-specific initialization.
- [ ] Begin tracing Bluetooth initialization from bt_manager_init().


---

## 🛠️ Multi-Phase Technical Backlog

### Phase 1: Workspace Stabilization & Validation
* [x] Reorganize raw workspace components into unified `/Code/` and `/Docs/` tracking environments.
* [x] Purge directory filename collisions (duplicate `python read_cache_db.py` asset file names).
* [x] Refactor local parsing script parameters to handle absolute directory locations natively via `os.path.dirname`.
* [x] Map internal SQLite table schemas from the encrypted offline application database file tracking matrices.

### Phase 2: Android APK Reverse Engineering
* [ ] Secure clean stock `.apk` binaries of the **FB Invincible Plus / CyFit** mobile companion framework.
* [ ] Decompile the application packages via JADX-GUI to extract plain-text Java source classes.
* [ ] Isolate networking interceptor routines (`okhttp3.Interceptor`) to locate HTTP custom request properties.
* [ ] Trace security references to extract the local encryption key configurations used to wrap database fields.

### Phase 3: BLE Protocol Documentation
* [ ] Import captured raw wireless packet logs (`.pcap`) into the Wireshark protocol environment.
* [ ] Chart the active configuration handles and specific service UUID boundaries mapping to the device.
* [ ] Document hex command sequences used for wireless time syncing, configuration states, and handshake runs.
* [ ] Isolate the specific BLE characteristic that processes firmware blocks during live update flows.

### Phase 4: OTA Container Analysis
* [ ] Map out structural boundary fields, segment size allocation variables, and alignment pads within `ota_V1.03.11.bin`.
* [ ] Locate the verification block (CRC, checksum array, or cryptographic signature tail) appended to container images.
* [ ] Develop an automated testing utility to test custom multi-image container configurations.

### Phase 5: Firmware Core Reversing

* [x] Initialize Ghidra environment.
* [x] Verify ARM Cortex-M interrupt vector table.
* [x] Confirm executable firmware image (`Block2_System_app.bin`).
* [x] Reconstruct the firmware boot sequence from reset vector to `main()`.
* [ ] Reverse engineer `main_msg_proc()` and document the runtime message architecture.
* [ ] Identify subsystem initialization ordering during application startup.
* [ ] Map ownership of runtime components (Zephyr, Actions Semiconductor, Fire-Boltt application, third-party libraries).
* [ ] Locate peripheral control loops within `extcfg.bin`.

## 🛑 Blocked & Parked Tasks

| Target Task Task | Blocked By | Required Remediation Action |
| :--- | :--- | :--- |
| **Parsing `map_cache.db` Data Rows** | Application AEAD Data Encryption | Complete Phase 2 APK decompilation to extract runtime keys from the Keystore module. |
| **Direct Asset Server Harvesting** | Gateway API Server Connection Timeouts | Isolate valid User-Agent strings and security headers directly from the app's network classes. |
| **Display Clock Register Tuning** | Unverified Hardware Address Layouts | Run complete differential validation loops across matching hardware configuration files. |