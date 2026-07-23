# Project Task Ledger & Sprint Board

This document tracks active technical backlogs, experimental verification gates, and immediate priorities. Tasks are organized by development phase to guide both human researchers and automated AI agents.

---

## 🟥 Current Sprint Priorities (Immediate Actions)

- [ ] Build a complete runtime message catalog (message IDs, sender, receiver, handler, meaning).
- [ ] Trace every caller of `msg_manager_send_async_msg()`.
- [ ] Reverse engineer `app_switch()`.
- [ ] Reverse engineer `system_app_launch()`.
- [ ] Identify application registration during startup (`msg_manager_add_listener()` call sites).
- [ ] Document the Runtime Messaging & Listener Framework.
- [ ] Continue tracing Bluetooth initialization from `bt_manager_init()`.

---

## 🛠️ Multi-Phase Technical Backlog

### Phase 1: Workspace Stabilization & Validation

- [x] Reorganize raw workspace components into unified `/Code/` and `/Docs/` tracking environments.
- [x] Purge directory filename collisions (duplicate `python read_cache_db.py` asset file names).
- [x] Refactor local parsing script parameters to handle absolute directory locations natively via `os.path.dirname`.
- [x] Map internal SQLite table schemas from the encrypted offline application database file tracking matrices.

---

### Phase 2: Android APK Reverse Engineering

- [ ] Secure clean stock `.apk` binaries of the **FB Invincible Plus / CyFit** companion application.
- [ ] Decompile application packages with JADX.
- [ ] Locate networking interceptors (`okhttp3.Interceptor`).
- [ ] Identify encryption key handling for local database protection.
- [ ] Correlate APK message producers with firmware message handlers.

---

### Phase 3: BLE Protocol Documentation

- [ ] Import captured BLE packet logs (`.pcap`) into Wireshark.
- [ ] Document GATT services and characteristic UUIDs.
- [ ] Reverse engineer time sync, configuration, and notification commands.
- [ ] Identify OTA transfer characteristics.
- [ ] Correlate BLE commands with firmware message IDs.

---

### Phase 4: OTA Container Analysis

- [ ] Reverse engineer `ota_V1.03.11.bin` container layout.
- [ ] Identify checksum / CRC / signature structures.
- [ ] Document image boundaries and alignment.
- [ ] Develop tooling to unpack and rebuild OTA containers.

---

### Phase 5: Firmware Core Reverse Engineering

#### Boot & Runtime Architecture

- [x] Initialize Ghidra environment.
- [x] Verify ARM Cortex-M interrupt vector table.
- [x] Confirm executable firmware image (`Block2_System_app.bin`).
- [x] Reconstruct boot sequence from reset vector to `main()`.
- [x] Reverse engineer `main_msg_proc()`.
- [x] Reconstruct runtime message receive path.
- [x] Reconstruct runtime message send path.
- [x] Reverse engineer listener registration and lookup framework.
- [x] Identify runtime logical addressing (application name → thread ID).
- [ ] Document Runtime Messaging & Listener Framework.
- [ ] Reverse engineer runtime initialization (`os_msg_init()`).
- [ ] Identify subsystem initialization order.
- [ ] Map subsystem ownership (Zephyr, Actions Semiconductor, Fire-Boltt application, third-party libraries).
- [ ] Locate peripheral control loops within `extcfg.bin`.

#### Application Runtime

- [ ] Build complete message catalog.
- [ ] Reverse engineer `app_switch()`.
- [ ] Reverse engineer `system_app_launch()`.
- [ ] Identify application lifecycle.
- [ ] Identify startup listener registration sequence.

#### Memory & Runtime Structures

- [ ] Expand documented memory map.
- [ ] Document mailbox structures.
- [ ] Document listener registry structures.
- [ ] Identify remaining runtime pools and allocators.

---

## 🛑 Blocked & Parked Tasks

| Target Task | Blocked By | Required Remediation Action |
| :--- | :--- | :--- |
| **Parsing `map_cache.db` data rows** | Application AEAD encryption | Complete APK reverse engineering to recover runtime encryption keys. |
| **Direct asset server harvesting** | Gateway API authentication | Recover request headers and authentication flow from companion application. |
| **Display clock register tuning** | Unverified hardware register layout | Continue firmware and configuration reverse engineering. |