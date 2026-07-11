# Fire-Boltt Invincible Plus (Platform 097) Reverse Engineering Project

An open-source, multi-agent reverse engineering knowledge base and toolchain ecosystem dedicated to analyzing the firmware, communication protocols, memory partitions, and hardware architectures of the Fire-Boltt Invincible Plus (097 variant) smart watch platform.

---

## 📋 Project Philosophy & Core Objective

This project aims to systematically map the undocumented implementation rules of the 097 hardware ecosystem. The primary objective is to reverse engineer the device parameters deeply enough to enable, modify, or restore functionality that is manufacturer-disabled or closed.

### Technical Research Goals:
* **Custom Watch Faces:** Build an open compiler pipeline to repack custom user interface bitmap grids into SDFS asset sectors.
* **Firmware Customization:** Locate peripheral register parameters inside structural system tables to audit display behaviors (such as vertical refresh bounds).
* **Wireless Protocol Mapping:** Decode local Bluetooth Low Energy (BLE) payload schemas to write independent tools decoupled from official cloud apps.
* **Decoupled OTA Infrastructure:** Reverse engineer advanced container check mechanisms to allow reliable system flashing over independent local interfaces.
* **Platform Open SDK:** Accumulate low-level documentation to ultimately compile a community hardware abstraction library for similar Actions Semiconductor platforms.

---

## 📂 Repository Structural Layout

The workspace is organized into isolated, self-contained functional environments to maintain absolute scannability:

```text
fireboltt-invincible-plus-097-re/
├── ONBOARDING.md          # Multi-model onboarding blueprint and agent capability matrix
├── README.md              # Project portal landing page (This file)
├── TODO.md                # Task roadmap tracker and developer sprint boards
├── Code/                  # Extraction scripts, parsing pipelines, and automation code utilities
├── Docs/                  # Raw binary storage artifacts, logs, and capture data files
└── wiki/                  # Granular Technical Wiki Modules
    ├── overview.md        # Current phase dashboard and system milestones tracker
    ├── evidence.md        # Master Evidence Matrix mapping verified system artifacts
    ├── research_log.md    # Chronological session logs and appendix history
    ├── experiments.md     # Engineering testing outputs and trial results
    ├── firmware.md        # Zephyr RTOS symbol parameters and SDFS partition layouts
    ├── apk.md             # Decompiled mobile app frameworks and database crypto schemas
    ├── ble.md             # Radio service handle maps and characteristic specifications
    ├── ota.md             # Multi-image update package containers and validation loops
    └── glossary.md        # Standardized vocabulary definitions for technical terms

🛠️ Operational Toolchain Environment

Replication of the parsing pipelines inside this repository utilizes the following environmental toolchains:

    Core Runtime: Python 3.12+ (Binary data slicing, sqlite processing blocks)

    Application Decompilers: JADX-GUI / Apktool (Companion Android app auditing)

    Wireless Sniffers: PCAPdroid / Wireshark Desktop (Packet stream harvesting)

    Binary Analysis: ImHex / Ghidra Disassembler (Firmware asset mapping)

🚀 Collaborating & Contribution Protocol

This repository leverages an array of specialized artificial intelligence agents running alongside human researchers within a unified, evidence-indexed environment.

To join development or use an AI assistant with this repository:

    Review the absolute communication rules defined inside AI_Onboarding.md to initialize your model constraints.

    Read the global ledger mapping values inside docs/evidence.md to identify verified system assets.

    Classify all findings under the precision tiers (Confirmed, High Confidence, Hypothesis, Disproved) established inside the project's documentation standards.

    Append any execution records, test cases, or string findings chronologically at the absolute bottom of docs/research_log.md. Never rewrite historical dates.