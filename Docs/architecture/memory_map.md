# Firmware Memory Map

## Purpose

This document records verified memory regions, global runtime objects, and important addresses identified during firmware reverse engineering.

Only evidence-backed observations are included.

---

# Memory Regions

| Address Range | Description | Status |
|--------------|-------------|--------|
| `0x10000000` | Firmware image (Flash) | Confirmed |
| `0x18000000` | Runtime RAM / PSRAM region | Confirmed |

---

# Boot Structures

| Address | Object | Evidence |
|---------|--------|----------|
| `0x10000000` | Interrupt vector table | Confirmed |

---

# Runtime Objects

## Listener Registry

| Address | Object | Status |
|---------|--------|--------|
| `0x182A8C5C` | Listener registry (head + tail pointers) | Confirmed |

Observed layout:

```c
struct listener_list {
    listener_node *head;
    listener_node *tail;
};
```

---

## Mailbox

| Address | Object | Status |
|---------|--------|--------|
| `0x1800C734` | Global mailbox object | Confirmed |

Used by:

- `k_mbox_async_put()`
- `k_mbox_get()`

---

## Async Message Pool

| Address | Object | Status |
|---------|--------|--------|
| `0x18009128` | Async message slot pool | Confirmed |

Used by:

- `os_send_async_msg()`

---

# Runtime Structures

## Listener Node

Observed layout:

```c
struct listener_node {
    struct listener_node *next;
    char *name;
    uint32_t tid;
};
```

Size:

```
0x0C bytes
```

---

# Known Function Entry Points

## Boot

| Function | Address |
|----------|---------|
| `z_arm_reset` | `0x1008481C` |
| `z_arm_prep_c` | `0x100840C8` |
| `z_cstart` | `0x10112ECC` |
| `bg_thread_main` | `0x10112E64` |
| `main` | `0x100315AC` |

---

## Runtime Dispatcher

| Function | Address |
|----------|---------|
| `main_msg_proc` | `0x10031230` |

---

## Messaging

| Function | Address |
|----------|---------|
| `msg_manager_send_async_msg` | `0x100C590C` |
| `msg_manager_receive_msg` | `0x1012CC58` |
| `os_send_async_msg` | `0x1008001C` |
| `os_receive_msg` | `0x100800FC` |
| `k_mbox_async_put` | `0x101136C4` |
| `k_mbox_get` | `0x10113724` |

---

## Listener Framework

| Function | Address |
|----------|---------|
| `msg_manager_listener_tid` | `0x1012CC4C` |
| `FUN_100C576C` | `0x100C576C` |
| `msg_manager_add_listener` | `0x100C5850` |

---

# Open Questions

The following addresses or regions remain under investigation:

| Item | Status |
|------|--------|
| Runtime initialization (`os_msg_init`) | Not analyzed |
| Complete RAM layout | Incomplete |
| Heap / allocator regions | Incomplete |
| Peripheral register mappings | Unknown |
| `extcfg.bin` runtime structures | Under investigation |

---

# Related Documents

- `boot_sequence.md`
- `runtime_message_framework.md`
- `system_overview.md`