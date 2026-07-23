# Firmware Boot Sequence

## Purpose

This document describes the verified execution path from CPU reset until control enters the Fire-Boltt runtime.

Detailed runtime behavior after `main()` is documented in `runtime_message_framework.md`.

---

## Verified Boot Chain

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

---

## Boot Stages

| Stage | Primary Function | Purpose |
|--------|------------------|---------|
| CPU Reset | `z_arm_reset()` | ARM Cortex-M reset handling |
| Architecture Init | `z_arm_prep_c()` | Early runtime initialization |
| Kernel Startup | `z_cstart()` | Zephyr kernel initialization |
| Main Thread Switch | `arch_switch_to_main_thread()` | Enter normal runtime |
| Background Thread | `bg_thread_main()` | Final runtime initialization |
| Application Entry | `main()` | Enter Fire-Boltt application |
| Runtime Dispatcher | `main_msg_proc()` | Begin message-driven execution |

---

## Architectural Boundary

```
ARM Startup
    ↓
Zephyr Kernel
    ↓
Fire-Boltt Runtime
```

---

## Verification Status

**Status:** High Confidence

Evidence:

- Ghidra disassembly
- `zephyr.map`
- ARM Cortex-M startup sequence

---

## Related Documents

- `runtime_message_framework.md`
- `memory_map.md`
- `scheduler_notes.md`