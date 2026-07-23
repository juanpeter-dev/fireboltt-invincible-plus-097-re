# Runtime Messaging & Listener Framework

## Overview

The Fire-Boltt Invincible Plus (Platform 097) firmware implements a message-driven runtime architecture built on top of Zephyr RTOS.

Applications communicate using **logical application names** rather than directly addressing threads. A listener registry maps application names to thread identifiers, allowing the runtime to route messages through a centralized mailbox transport.

The runtime messaging framework consists of three major layers:

1. **Application Layer**
   - Creates messages
   - Sends messages using application names
   - Processes received messages

2. **Listener Framework**
   - Registers application listeners
   - Resolves application names to thread IDs
   - Maintains the listener registry

3. **Transport Layer**
   - Copies messages into an asynchronous slot pool
   - Delivers messages through a Zephyr mailbox
   - Receives messages for dispatch

---

# Architecture Overview

```
Application
        │
        │ "launcher"
        │ "music"
        │ "system"
        ▼
msg_manager_send_async_msg()
        │
        ▼
msg_manager_listener_tid()
        │
        ▼
Listener Registry
        │
        ▼
Thread ID
        │
        ▼
os_send_async_msg()
        │
        ▼
k_mbox_async_put()
        │
===============================
        │
        ▼
k_mbox_get()
        │
        ▼
os_receive_msg()
        │
        ▼
msg_manager_receive_msg()
        │
        ▼
main_msg_proc()
```

---

# Listener Framework

## Overview

Applications never communicate directly using thread identifiers.

Instead, they send messages addressed to logical application names.

The listener framework resolves these names into runtime thread IDs.

---

## Listener Registry

Global registry address:

```
0x182A8C5C
```

Observed layout:

```c
struct listener_list {
    listener_node *head;
    listener_node *tail;
};
```

The registry uses:

- Head pointer
- Tail pointer

allowing O(1) insertion while searches remain linear.

---

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

| Offset | Field | Confidence |
|---------|-------|------------|
| +0 | next | High |
| +4 | name | High |
| +8 | thread ID | High |

---

## Listener Registration

Function:

```
msg_manager_add_listener()
```

Responsibilities:

- Allocate listener node
- Store name
- Store thread ID
- Append node to registry tail

Allocation uses:

```
mem_pool_malloc()
```

The registry is protected using a BASEPRI critical section.

---

## Listener Lookup

Functions:

```
msg_manager_listener_tid()

↓

FUN_100C576C()
```

Lookup process:

1. Traverse linked list
2. Compare application names using strcmp()
3. Return matching thread ID
4. Return 0 if not found

---

# Message Sending

Application entry point:

```
msg_manager_send_async_msg()
```

Responsibilities:

- Resolve application name
- Convert to thread ID
- Temporarily raise thread priority
- Forward message to transport layer

Message size:

```
0x14 bytes
```

No payload copy occurs in this function.

Only the message pointer is forwarded.

---

## Transport

Function:

```
os_send_async_msg()
```

Responsibilities:

- Allocate asynchronous slot
- Copy message into slot
- Submit through mailbox

Observed operations:

- k_sem_take()
- memset()
- memcpy()
- k_mbox_async_put()

---

# Message Receiving

Receive chain:

```
main_msg_proc()

↓

msg_manager_receive_msg()

↓

os_receive_msg()

↓

k_mbox_get()
```

Received messages are eventually dispatched by `main_msg_proc()`.

---

# Message Structure

The firmware contains embedded debug strings identifying message fields.

Observed field names:

```
sender
receiver
owner
type
cmd
reserve
value
callback
sync_sem
```

Known observations:

| Field | Status |
|--------|--------|
| sender | Confirmed by debug strings |
| receiver | Confirmed by debug strings |
| owner | Confirmed by debug strings |
| type | Confirmed |
| cmd | Confirmed |
| reserve | Confirmed |
| value | Confirmed |
| callback | Confirmed |
| sync_sem | Confirmed |

The exact binary layout of every field has not yet been fully reconstructed.

---

# Synchronization

Two different synchronization mechanisms are used.

## Thread-level protection

Observed in:

```
msg_manager_send_async_msg()
```

Mechanism:

```
k_thread_priority_set(-1)
```

Purpose:

Temporarily prevents thread preemption during message submission.

---

## Interrupt-level protection

Observed in:

```
FUN_100C576C()

msg_manager_add_listener()
```

Mechanism:

```
BASEPRI
```

The firmware raises BASEPRI while accessing the listener registry.

This protects the registry from interrupt-context interference.

---

# Evidence Classification

## Direct Firmware Observations

- Listener node layout
- Listener registry layout
- Send path
- Receive path
- BASEPRI critical sections
- Thread priority elevation
- Message size (0x14 bytes)
- Embedded message field names
- Mailbox transport chain

---

## Confirmed by zephyr.map

- Function names
- Object files
- Function addresses
- Function sizes

---

## ARM Architectural Knowledge

- BASEPRI semantics
- Thumb instruction behavior
- Interrupt masking

---

## Zephyr Architectural Knowledge

- Mailbox primitives
- Cooperative thread priorities

---

## Inference

The following remain interpretations rather than direct observations:

- Destination ID 0 likely represents broadcast.
- Listener registry protection indicates interrupt concurrency is considered important.
- Thread-priority elevation acts as a lightweight critical section.

---

# Open Questions

- Exact binary layout of the complete message structure.
- Broadcast implementation for destination ID 0.
- Listener removal mechanism (if one exists).
- Runtime initialization of mailbox infrastructure.
- Complete message catalog.
- Application startup registration sequence.

---

# Related Documents

- `boot_sequence.md`
- `memory_map.md`
- `scheduler_notes.md`
- `system_overview.md`
