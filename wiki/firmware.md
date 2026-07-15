# Firmware Systems & File Registers Analysis

## 1. Operating System Infrastructure
- **Status:** HIGH CONFIDENCE
- **Evidence Reference:** `[E001]` (All lines mapping exported scheduler tables).
- **Observed Data:** Linker map addresses expose exact Zephyr kernel initialization patterns (`z_sched_init`, `k_queue_get`).
- **Interpretation:** The runtime engine functions over a compiled instance of the open-source Zephyr Real-Time Operating System (RTOS).
- **Alternative Interpretation:** The manufacturer built a custom vendor operating system from scratch and intentionally named their internal core functions after Zephyr primitives to maintain toolchain naming standards.
- **What would disprove it:** A physical flash dump showing alternative kernel architecture execution maps running directly beneath the application layer.

## 2. The Smart Digital File System (SDFS) Partition
- **Status:** CONFIRMED
- **Evidence Reference:** `[E004]` (Structural parsing of the `sdfs.bin` payload segment).
- **Observed Data:** Unpacking fixed 32-byte directory entry records yields consistent parameters: 12 to 16 bytes of null-padded ASCII characters tracking filenames, a 4-byte little-endian size integer, and a 4-byte relative offset pointer.
- **Interpretation:** The device uses the Actions Semiconductor proprietary flat-file layout configuration known as the Smart Digital File System (SDFS).
- **Why this matters:** Knowing the exact layout allows us to build automated script parsers that open, modify, and cleanly repack system binaries without introducing structural byte shifts.

## 2.1 OTA Package Structure

- **Status:** HIGH CONFIDENCE
- **Evidence Reference:** `[E006]`, `[E007]`, `[E008]`, `[E009]`
- **Observed Data:**
OTA
├── Block1
│   ├── TEMP.bin
│   └── sdfs_k.bin
│
└── Block2
    ├── app.bin
    └── sdfs.bin

- **Interpretation:** The OTA package contains multiple firmware blocks rather than a single monolithic image. Each block contains either executable firmware or an accompanying SDFS resource partition.
- **What remains unknown:** The execution order and update sequence of these partitions have not yet been confirmed through firmware analysis.

## 3. Peripheral Parameter Arrays (`extcfg.bin`)
- **Status:** HYPOTHESIS
- **Evidence Reference:** Extracted binary block segment from the master SDFS update container file payload `[E004]`.
- **Interpretation:** This file holds device-specific system parameters, driver adjustments, and peripheral initialization mappings used by the Actions hardware abstraction layer.
- **Possible Internal Contents:**
  - Clock frequency dividers for the primary display interface buses (SPI/QSPI configuration parameters).
  - Memory timing bounds for hardware display DMA transfers.
  - Initial configuration codes for the display controller panel.
- **Negative Evidence:** Altering data records within this file and deploying it to target devices has not yet been executed to observe physical changes on the hardware display.
- **What would disprove it:** Re-flashing an altered version of `extcfg.bin` onto the device and observing zero changes in display behavior, interface clocks, screen timing, panel power limits, or visual errors.

## 4. Primary Executable Firmware Image

- **Status:** CONFIRMED
- **Evidence Reference:** `[E001]`, `[E008]`
- **Observed Data:**
  - `Block2_System_app.bin` imports successfully into Ghidra as an ARM Cortex-M firmware image.
  - The interrupt vector table matches the linker map (`zephyr.map`), including the initial stack pointer and the startup entry point (`z_arm_reset`).
  - Cross-referencing with `zephyr.map` confirms the subsequent startup chain (`z_arm_prep_c`, `z_cstart`, `bg_thread_main`, and `main()`).
- **Interpretation:** `Block2_System_app.bin` is confirmed to be the primary executable firmware image contained within the OTA package.
- **What remains unknown:** The relationship between this application image and the remaining firmware partitions (`TEMP.bin`, `sdfs_k.bin`, `sdfs.bin`) has not yet been fully reconstructed.

---

## 5. Firmware Boot Sequence

- **Status:** CONFIRMED
- **Evidence Reference:** `[E001]`, `[E008]`

### Verified execution path

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

### Architectural boundaries

**Architecture-specific startup**
- `z_arm_reset`
- `z_arm_prep_c`

**Generic Zephyr initialization**
- `z_cstart`
- `bg_thread_main`

**Application startup**
- `main()`

**Runtime execution**
- `main_msg_proc()`

### Current understanding

The firmware follows a standard ARM Cortex-M startup sequence before entering the generic Zephyr initialization path. Control is then transferred into the vendor application (`app/libapp.a`), where runtime operation becomes event-driven through `main_msg_proc()`.

### Remaining uncertainty

The underlying implementation of the runtime message framework has not yet been identified. It remains unknown whether `msg_manager_receive_msg()` directly implements the queue or wraps a lower-level messaging primitive.