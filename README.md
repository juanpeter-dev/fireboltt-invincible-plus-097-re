# Fire-Boltt Invincible Plus (Platform 097) Reverse Engineering

An open-source reverse engineering project focused on understanding the Fire-Boltt Invincible Plus (Platform 097) firmware, runtime architecture, communication protocols, and hardware platform.

The long-term goal is to build independent tools, documentation, and firmware knowledge that are not dependent on the official companion application.

---

# Project Goals

This project is driven by evidence rather than assumptions.

Current long-term objectives include:

- Reverse engineer the firmware architecture
- Document the runtime messaging framework
- Decode the Bluetooth Low Energy (BLE) protocol
- Understand the OTA update process
- Build independent firmware tooling
- Investigate custom watch face support
- Explore firmware modification possibilities
- Document the underlying hardware platform

---

# Current Progress

## Completed

- Firmware partitions extracted
- Boot sequence reconstructed
- Runtime messaging framework reconstructed
- Listener registration and lookup architecture reconstructed
- Runtime mailbox transport identified

## In Progress

- Application runtime reconstruction
- Runtime message catalog
- BLE protocol analysis
- OTA validation and update process
- Memory map expansion

## Planned

- Firmware patching
- Custom watch face tooling
- Independent OTA tooling
- Community SDK

---

# Repository Structure

```text
fireboltt-invincible-plus-097-re/

├── README.md
├── ONBOARDING.md
├── TODO.md

├── Code/
│   ├── ...
│
├── Docs/
│   ├── architecture/
│   │   ├── boot_sequence.md
│   │   ├── runtime_message_framework.md
│   │   ├── memory_map.md
│   │   ├── scheduler_notes.md
│   │   └── system_overview.md
│   │
│   ├── firmware/
│   └── reverse_engineering/
│
└── wiki/
    ├── overview.md
    ├── evidence.md
    ├── research_log.md
    ├── experiments.md
    ├── firmware.md
    ├── apk.md
    ├── ble.md
    ├── ota.md
    └── glossary.md
```

---

# Documentation Guide

The repository separates documentation into two categories.

## `Docs/`

Evidence-backed technical documentation.

Examples:

- Boot sequence
- Runtime messaging framework
- Memory map
- Reverse engineering methodology
- Firmware subsystem documentation

## `wiki/`

Project-level documentation.

Examples:

- Project overview
- Evidence index
- Research log
- Experiments
- BLE progress
- OTA progress

---

# Toolchain

Current reverse engineering workflow:

- **Firmware Analysis:** Ghidra
- **Binary Inspection:** ImHex
- **APK Analysis:** JADX, Apktool
- **Packet Analysis:** Wireshark, PCAPdroid
- **Automation:** Python 3.12+

---

# Evidence Standards

Every technical conclusion is classified according to its source.

- **Direct Firmware Observation** — Visible in firmware disassembly or data.
- **Confirmed by `zephyr.map`** — Symbol names, addresses, and ownership.
- **APK Evidence** — Confirmed from the Android companion application.
- **Architecture Knowledge** — ARM Cortex-M or Zephyr RTOS behavior.
- **Inference** — Reasoned conclusion that has not yet been directly verified.

Hypotheses are never treated as confirmed facts.

---

# Contributing

When contributing to the project:

1. Read `ONBOARDING.md`.
2. Review the current project status in `wiki/overview.md`.
3. Check the evidence index before drawing conclusions.
4. Clearly distinguish observations from hypotheses.
5. Record significant findings in `wiki/research_log.md`.

---

# Current Reverse Engineering Focus

The current milestone is **Application Runtime Reconstruction**.

Active work includes:

- Building the runtime message catalog
- Reverse engineering application lifecycle management
- Mapping subsystem ownership
- Correlating firmware runtime behavior with the Android companion application

This milestone builds on the completed reconstruction of the firmware boot sequence and runtime messaging architecture.