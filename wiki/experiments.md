# Technical Experiments Log

This repository module preserves chronological entries of all direct technical experiments executed on the Fire-Boltt Invincible Plus target platform. Every experiment must link back to a parent Question ID tracked in `docs/questions.md`.

---

## Experiment E0001: Local Cache Table Row Interrogation
* **Parent Question Target:** `Q001` (Watch face asset cache storage paths)
* **Goal:** Extract plaintext asset download links and host configuration arrays directly from offline application storage files.
* **Tools Used:** Python 3.12, localized SQLite3 driver configurations.
* **Files Used:** `/Docs/map_cache.db`
* **Procedure:** Developed `Code/read_cache_db.py` to open the local database, read the internal master schema data, and dump rows from the `resources` table.
* **Expected Result:** Clean parsing of plaintext JSON data blocks mapping watch face files to active download directories.
* **Observed Result:** Script executed successfully and dumped 18 rows, but all string paths and metadata fields returned cryptographically scrambled byte matrices bound to initialization variables (`metadata_nonce`, `data_nonce`).
* **Interpretation & Lessons Learned:** The companion application implements an AEAD encryption-at-rest scheme (likely AES-GCM or SQLCipher) before serializing network states to the disk layer. Interrogating the local database file directly on a host laptop without live memory access keys is an inefficient vector.
* **Future Follow-up Action:** Shift focus to static APK decompilation to trace key derivations, and run packet captures to intercept assets in transit before encryption takes place.