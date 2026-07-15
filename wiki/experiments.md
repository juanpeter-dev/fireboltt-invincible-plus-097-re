# Technical Experiments Log

This repository module preserves chronological entries of all direct technical experiments executed on the Fire-Boltt Invincible Plus target platform. Every experiment must link back to a parent Question ID tracked in `docs/questions.md`.

---

## Experiment E0001: Local Cache Table Row Interrogation
* **Parent Question Target:** `Q001` (Watch face asset cache storage paths)
* **Goal:** Extract plaintext asset download links and host configuration arrays directly from offline application storage files.
* **Tools Used:** Python 3.12, localized SQLite3 driver configurations.
* **Files Used:** `/Docs/map_cache.db`
* **Procedure:** Developed `Code/read_cache_db.py` to open the local database, read the internal master schema data, and dump rows from the `resources` table.
* **Expected Result:** Clean parsing of plaintext JSON data blocks mapping watch face files to active download directories.
* **Observed Result:** Script executed successfully and dumped 18 rows, but all string paths and metadata fields returned cryptographically scrambled byte matrices bound to initialization variables (`metadata_nonce`, `data_nonce`).
* **Interpretation & Lessons Learned:** The companion application implements an AEAD encryption-at-rest scheme (likely AES-GCM or SQLCipher) before serializing network states to the disk layer. Interrogating the local database file directly on a host laptop without live memory access keys is an inefficient vector.
* **Future Follow-up Action:** Shift focus to static APK decompilation to trace key derivations, and run packet captures to intercept assets in transit before encryption takes place.

---

## Experiment E0002: Executable Firmware Verification

* **Parent Question Target:** `Q002` (Identify the primary executable firmware image)
* **Goal:** Determine whether `Block2_System_app.bin` contains the primary executable firmware.
* **Tools Used:** Ghidra 12.1.2, `zephyr.map`
* **Files Used:** `/Docs/extracted_clean/Block2_System_app.bin`, `/Docs/zephyr.map`
* **Procedure:** Imported the firmware image into Ghidra, configured the ARM Cortex-M image, and cross-referenced the interrupt vector table with `zephyr.map`.
* **Expected Result:** Confirm that the extracted image contains executable firmware.
* **Observed Result:** The firmware contains a valid Cortex-M interrupt vector table. The initial stack pointer, reset vector, and startup symbols match the linker map.
* **Interpretation & Lessons Learned:** `Block2_System_app.bin` is confirmed as the primary executable firmware image contained within the OTA package.
* **Future Follow-up Action:** Reconstruct the firmware boot sequence.

---

## Experiment E0003: Firmware Boot Sequence Reconstruction

* **Parent Question Target:** `Q003` (Reconstruct the firmware execution path)
* **Goal:** Reconstruct the complete execution path from reset through application startup.
* **Tools Used:** Ghidra 12.1.2, `zephyr.map`, Claude, GLM
* **Files Used:** `/Docs/extracted_clean/Block2_System_app.bin`, `/Docs/zephyr.map`
* **Procedure:** Sequentially analyzed the firmware startup functions (`z_arm_reset`, `z_arm_prep_c`, `z_cstart`, `bg_thread_main`, `main()`) using Ghidra. Cross-referenced every function with `zephyr.map`. Independently verified key architectural conclusions using GLM to distinguish direct observations from architectural inference.
* **Expected Result:** Identify the complete firmware startup chain and determine where execution enters the application layer.
* **Observed Result:** Reconstructed the verified execution path:

```text
Reset Vector
    ↓
z_arm_reset
    ↓
z_arm_prep_c
    ↓
z_cstart
    ↓
arch_switch_to_main_thread
    ↓
bg_thread_main
    ↓
main()
    ↓
main_msg_proc()
```

* **Interpretation & Lessons Learned:** The firmware follows a standard ARM Cortex-M → Zephyr RTOS startup sequence before entering the Fire-Boltt application layer. Runtime execution is driven by `main_msg_proc()`, which functions as the application's primary message dispatcher.
* **Independent Verification:** GLM independently analyzed the runtime dispatcher from stripped firmware and reached the same high-level architectural conclusion: runtime operation is message-driven rather than based on direct subsystem loops. GLM also independently confirmed that the underlying queue implementation cannot yet be determined from the currently analyzed functions.
* **Future Follow-up Action:** Reverse engineer the runtime message framework by tracing `msg_manager_receive_msg()` and identifying the underlying queue implementation.