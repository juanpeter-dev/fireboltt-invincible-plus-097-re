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