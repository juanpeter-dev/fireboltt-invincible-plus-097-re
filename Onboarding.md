# Technical Contributor Onboarding

## Platform

**Fire-Boltt Invincible Plus (Platform 097)**

---

# 1. Purpose

Welcome to the Fire-Boltt Invincible Plus reverse engineering project.

This repository is an evidence-driven knowledge base documenting the firmware, runtime architecture, communication protocols, and supporting tooling for Platform 097.

The goal is **understanding the platform**, not simply modifying it.

Every technical conclusion should be reproducible and traceable to supporting evidence.

---

# 2. Project Goals

Current long-term objectives include:

- Reconstruct the firmware architecture
- Document the runtime messaging framework
- Reverse engineer the BLE protocol
- Understand the OTA update process
- Build independent tooling
- Investigate firmware modification
- Document the hardware platform

---

# 3. AI Capability Matrix

Different AI models are used for different engineering tasks.

| AI | Primary Role | Best Used For | Avoid |
|:---|:---|:---|:---|
| **Gemini** | Repository Indexer | Large APKs, repository indexing, large logs | Final technical conclusions |
| **Claude** | Firmware Analyst | Ghidra, firmware, embedded systems, architecture | Massive text ingestion |
| **ChatGPT** | Architecture Reviewer | Systems thinking, documentation, planning, experiment design | Large code generation |
| **DeepSeek** | Automation Engineer | Python tooling, parsers, scripting | Project planning |
| **Qwen** | Android Analyst | Java, Android, C/C++ | Firmware architecture |
| **GLM** | Independent Verifier | Cross-checking conclusions | Primary investigation |

No AI should be treated as authoritative.

Conflicting conclusions should be resolved through additional evidence rather than preference.

---

# 4. Repository Navigation

Always begin with:

```
README.md
    ↓
ONBOARDING.md
    ↓
wiki/overview.md
```

Then load documentation relevant to the investigation.

## Architecture

```
Docs/architecture/

boot_sequence.md
runtime_message_framework.md
memory_map.md
scheduler_notes.md
system_overview.md
```

## Firmware

```
Docs/firmware/
```

Subsystem-specific documentation.

## Reverse Engineering

```
Docs/reverse_engineering/
```

Methodology, naming conventions, Ghidra notes, and supporting analysis.

## Wiki

```
wiki/
```

Project overview, evidence index, research log, experiments, BLE, OTA, APK analysis, and glossary.

---

# 5. Evidence Standards

Every conclusion should clearly distinguish between:

- **Direct Firmware Observation**
- **Confirmed by `zephyr.map`**
- **APK Evidence**
- **ARM / Zephyr Architectural Knowledge**
- **Inference / Hypothesis**

Never present inference as confirmed fact.

When evidence is insufficient, state what additional evidence is required.

---

# 6. Investigation Workflow

When investigating a new topic:

1. Review the current project status in `wiki/overview.md`.
2. Search existing documentation before starting new analysis.
3. Gather evidence.
4. Separate observations from hypotheses.
5. Update documentation when a major architectural milestone is reached.
6. Record significant findings in `wiki/research_log.md`.

---

# 7. Documentation Principles

Architecture documents should describe **how the platform works**, not contain raw reverse engineering notes.

Reverse engineering notes should document:

- Ghidra observations
- Decompiled code
- Experiments
- Function naming rationale

Architecture documents should document:

- Boot flow
- Runtime architecture
- Memory map
- Subsystem design

---

# 8. Current Project Milestone

**Application Runtime Reconstruction**

Current objectives:

- Build the runtime message catalog.
- Reverse engineer application lifecycle management.
- Map subsystem ownership.
- Correlate firmware runtime behavior with the Android companion application.

This work builds on the completed reconstruction of the boot sequence and runtime messaging framework.