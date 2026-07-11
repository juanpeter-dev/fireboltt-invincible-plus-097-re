# Research Chronology & Experimental Records

This document acts as our single source of truth for the chronological timeline of our project, alongside deep technical analysis logs for every live experiment executed on the target platform.

## 1. Chronological Research Timeline

### 2026-06-15
- **Discovery:** Parsed the base layer structure of `ota_V1.03.11.bin` `[E004]`.
- **Reasoning:** Identified specific block divisions indicating nested code layers.
- **Impact:** Built custom script extractors (`Code/sub_extractor_fixed.py`) to successfully slice out operational code paths (`app.bin`, `sdfs.bin`).
- **Next Step:** Extract localized configuration files out of the main SDFS data block.

### 2026-07-11
- **Discovery:** Discovered local storage database encryption maps inside `map_cache.db` `[E005]`.
- **Reasoning:** `PRAGMA table_info` columns explicitly listed `metadata_nonce` and `data_nonce` parameters right next to encrypted data blocks.
- **Impact:** Confirmed that directly reading database strings offline on a laptop is a dead end. Shifted our target capture focus to plain-text device log processing loops.
- **Next Step:** Set up a clean, modular repository layout and launch regex binary scanners on our network log files.

---

## 2. Technical Experiments Log
*Note: Granular testing logs, methods, and outcomes are systematically documented inside the dedicated verification vault at `docs/experiments.md` and linked directly to their parent research vectors inside `docs/questions.md`.*

---

## 3. Session Log Appendix (Appended Records Only)

### 2026-07-11 (Update 4)
- Deconstructed the single-file `RESEARCH_LOG.md` layout and successfully deployed the clean, modular `/docs/` architecture matrix.
- Linked all system discoveries directly to explicit identifiers tracked inside the unified `docs/evidence.md` ledger.
- Cleaned technical terminology across the repository, removing speculative phrases like "AES-GCM encrypted database schema" and replacing them with accurate descriptions based on physical evidence: "Observed `metadata_nonce` and `data_nonce` variables indicating the use of AEAD encryption."
- Built a dedicated repository module for decompiled APK tracking analysis (`docs/apk.md`) to guide future mobile application framework analysis.

### 2026-07-11 (Update 5)
- Deployed a completely overhauled onboarding configuration profile, stripping out all theatrical language, roleplay elements, and narrative agent constraints.
- Switched the AI onboarding logic to a lazy-loading, hierarchical context structure to optimize LLM context window spaces.
- Shifted the primary project sprint focus from unencrypted log parsing to targeted Phase 2 Android APK reverse engineering.
- Established a rigorous script renaming layout inside the project roadmap to ensure honest documentation of script capabilities.

### 2026-07-11 (Update 6)
- Replaced model titles ("Project Director", etc.) with a functional, capability-driven AI Optimization Matrix.
- Merged the APK and BLE investigation goals into a unified Phase 2: Application & Protocol Analysis block to reflect real-world code dependencies.
- Deployed a step-by-step Onboarding Operational Decision Tree to guide session startups.
- Established a clean Evidence Confidence Ladder (Level 1 to Level 5) to index technical findings uniformly.
- Created `docs/questions.md` to shift task management from basic todo lists into structured, evidence-driven research questions.

### 2026-07-11 (Update 7)
- Migrated the root-level `AI_Onboarding.md` framework file to `ONBOARDING.md` to shift the workspace to a human-first, contributor-ready onboarding baseline.
- Removed self-evaluating phrases ("completely optimized") across the repository metadata to ensure a strictly objective, empirical technical standard.
- Created `docs/experiments.md` to serve as the project's permanent record for structural code and hardware experimental outcomes, decoupling execution details from the primary roadmap history.