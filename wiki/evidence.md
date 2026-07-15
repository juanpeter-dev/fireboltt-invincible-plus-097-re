## External Reference Material

Some firmware artifacts used in this project were obtained from the following external repository for independent analysis:

- https://github.com/herocoder14/fireboltt097

These files are treated as third-party reference material. Any conclusions drawn from them must be independently verified before being promoted to project evidence.


# Master Evidence Matrix

This document lists every active, verified artifact recovered from the Fire-Boltt Invincible Plus target platform. All claims made across the secondary architectural modules must cite these exact IDs.

| Evidence ID | Artifact Source Location | Technical Description | Specific Observed Data Payload / Reference Strings |
| :--- | :--- | :--- | :--- |
| **E001** | `/Docs/zephyr.map` | Linker map output layout sheet. | Contains core global symbols matching internal kernel definitions: `_kernel`, `k_thread`, `z_tick_sleep`, and `k_sem_init`. |
| **E002** | `/Docs/cyNetLog.txt` | Plain-text mobile application runtime network log trace. | Explicit path parameters tracking Actions Semiconductor SDK frameworks, alongside remote destination server calls (`http://dail.cynet2open.com:10090`). |
| **E003** | `/Docs/cyBleLog.txt` | Plain-text mobile application runtime BLE log trace. | Intercepted device initialization packets capturing the target hardware broadcast address: `F4:4E:FC:44:84:FF`. |
| **E004** | `/Docs/ota_V1.03.11.bin` | Binary file update container package payload. | Raw update patch file payload containing discrete sub-image sectors mapping onto target runtime storage arrays. |
| **E005** | `/Docs/map_cache.db` | Local SQLite 3 runtime database schema structure. | Extracted schema details displaying 4 specific operational tables: `settings`, `resources`, `tiles`, and `pinned_tiles`. |
| **E006** | `/Docs/extracted_clean/Block1_Staging_ota.xml` | OTA manifest extracted from the firmware update package. | Identifies board `D900`, firmware version `1.00_2304042028`, and partition metadata for the staging image. |
| **E007** | `/Docs/extracted_clean/Block1_Staging_sdfs_k.bin` | Extracted SDFS filesystem image. | Contains structured directory entries and resource records consistent with an SDFS filesystem rather than executable code. |
| **E008** | `/Docs/extracted_clean/Block2_System_app.bin` | Extracted application firmware image candidate. | Begins with values consistent with an ARM Cortex-M interrupt vector table (initial stack pointer followed by Thumb-mode function addresses). Ghidra verification pending. |
| **E009** | `/Docs/extracted_clean/Block2_System_sdfs.bin` | Secondary SDFS filesystem image. | Contains configuration resources including `usrcfg.bin`, `extcfg.bin`, `defcfg.bin`, `cfg_mic.bin`, `bt_rf.bin`, and related firmware configuration files. |
| **E010** | Ghidra analysis of `/Docs/extracted_clean/Block2_System_app.bin` | Verified ARM Cortex-M executable firmware image. | Interrupt vector table, `z_arm_reset`, `z_arm_prep_c`, `z_cstart`, `bg_thread_main`, and `main()` all correlate with `zephyr.map`. |
| **E011** | `Block2_System_app.bin` + `zephyr.map` + Ghidra | Firmware boot execution chain | Verified execution path from Cortex-M reset vector through `main_msg_proc`, including `z_arm_reset`, `z_arm_prep_c`, `z_cstart`, `bg_thread_main`, `main`, and the runtime dispatcher. |