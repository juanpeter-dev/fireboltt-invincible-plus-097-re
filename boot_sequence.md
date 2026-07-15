# Firmware Boot Sequence

## Purpose

This document describes the verified execution path from CPU reset until control enters the Fire-Boltt application.

## Verified Boot Chain

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

## Current Status

Status: HIGH CONFIDENCE

Evidence:
- E001
- E008

Verification:
- Ghidra disassembly
- zephyr.map
- ARM Cortex-M startup sequence

Current Boundary

Architecture-specific startup:
- z_arm_reset
- z_arm_prep_c

Generic Zephyr startup:
- z_cstart
- bg_thread_main

Fire-Boltt application:
- main()

Next research target:
- main_msg_proc()