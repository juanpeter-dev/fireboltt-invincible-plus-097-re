# Master Evidence Matrix

This document lists every active, verified artifact recovered from the Fire-Boltt Invincible Plus target platform. All claims made across the secondary architectural modules must cite these exact IDs.

| Evidence ID | Artifact Source Location | Technical Description | Specific Observed Data Payload / Reference Strings |
| :--- | :--- | :--- | :--- |
| **E001** | `/Docs/zephyr.map` | Linker map output layout sheet. | Contains core global symbols matching internal kernel definitions: `_kernel`, `k_thread`, `z_tick_sleep`, and `k_sem_init`. |
| **E002** | `/Docs/cyNetLog.txt` | Plain-text mobile application runtime network log trace. | Explicit path parameters tracking Actions Semiconductor SDK frameworks, alongside remote destination server calls (`http://dail.cynet2open.com:10090`). |
| **E003** | `/Docs/cyBleLog.txt` | Plain-text mobile application runtime BLE log trace. | Intercepted device initialization packets capturing the target hardware broadcast address: `F4:4E:FC:44:84:FF`. |
| **E004** | `/Docs/ota_V1.03.11.bin` | Binary file update container package payload. | Raw update patch file payload containing discrete sub-image sectors mapping onto target runtime storage arrays. |
| **E005** | `/Docs/map_cache.db` | Local SQLite 3 runtime database schema structure. | Extracted schema details displaying 4 specific operational tables: `settings`, `resources`, `tiles`, and `pinned_tiles`. |