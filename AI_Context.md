# Project
Fire-Boltt Invincible Plus (Actions Semiconductor D900/Leopard) Firmware Reverse Engineering

# Objective
Extract, unpack, and modify the watch's internal Smart Digital File System (SDFS) resource filesystem to swap out stock graphics assets with custom user images, and locate/alter extended hardware configuration registers to change the User Interface transition animation limits from 30FPS to 60FPS.

# Current Stage
Asset Extraction and Host Network Hunting (Post-App Sandbox Analysis)

# Confirmed Facts
- **Hardware Platform:** The watch uses an Actions Semiconductor D900 / Leopard hardware chipset variant platform.
- **Firmware Update Style:** The standalone firmware package file (`ota_V1.03.11.bin`) is an update patch container configured with an "AOTA" structural signature format.
- **Internal Operating System Matrix:** The firmware updates deploy on top of a Zephyr RTOS kernel alongside an Actions-proprietary applications framework layer (`app.bin`).
- **File Registry Construction:** The system resources use a proprietary binary file layout configuration known as SDFS (Smart Digital File System).
- **Partition Record Architecture:** AOTA/SDFS indexing tables use a uniform 32-byte layout pattern where the entry parameters are aligned sequentially: 12 to 16 bytes for the ASCII filename string, followed by a 4-byte little-endian unsigned integer for File Size, and a 4-byte little-endian unsigned integer for the Relative Offset Pointer.
- **Companion Application Profile:** The official phone app (**FB Invincible Plus**) is built directly on top of the third-party **CyFit framework**.
- **Data Footprint:** The local app cache database files (`map_cache.db`, `map_cache.db-shm`, `map_cache.db-wal`) use heavily encrypted BLOB storage matrix formatting.
- **Official Database Infrastructure:** The backend manufacturing server endpoint resolves to an open network domain via `HTTP` port `10090`.

# Hypotheses
- **Asset Isolation Logic:** The `ota_V1.03.11.bin` archive file is a highly restricted "delta patch" containing code modifications, while the true multi-megabyte user interface graphic assets catalog (`sdfs_k.bin`) resides inside the watch's permanent, untouched factory flash partitions.
- **Frame Rate Regulation:** Screen frame boundaries, refresh frequencies, and DMA canvas updates are regulated by structural parameters mapped directly inside the hardware register file `extcfg.bin`.
- **Server Verification Filters:** The endpoint `dail.cynet2open.com:10090` requires specific custom HTTP header parameters (such as an app-signature string or encryption token) to process remote anonymous queries safely, causing standard Python scripts to time out.

# Hardware & Tools
- Samsung J7 Nxt (Running custom Resurrection Remix OS, Android 10)
- Windows Laptop running Visual Studio Code (VSC)
- Python 3.12 Environment (with `struct`, `re`, and `sqlite3` modules)
- Wireshark Desktop Packet Analyzer
- PCAPdroid Android Network Sniffer

# Current Problem
Bypassing anonymous network timeouts to capture the target uncompressed graphics asset filesystem bundle directly, or locating it cached inside the local Android directory structure.

# Experiments Completed
- Developed brute-force and targeted partition slicing tools (`deep_slicer.py`, `clean_extractor.py`) to map AOTA container sectors.
- Successfully corrected structural header maps to cleanly slice `Block2_System_app.bin` ($1.7\text{ MB}$) and `Block2_System_sdfs.bin` ($36\text{ KB}$) from the update payload.
- Extracted inner system binary tables out of `sdfs.bin` (`usrcfg.bin`, `extcfg.bin`, `defcfg.bin`, `bt_rf.bin`, `callring.act`).
- Dumped private Android application log sandboxes (`Android/data/com.app.cy.fireboltt/`), uncovering plaintext network operation logs (`cyNetLog.txt`) and Bluetooth operations records (`cyBleLog.txt`).
- Executed packet captures on Android via PCAPdroid while performing active watch functions (changing faces, sync triggers), capturing raw unencrypted destination requests (`GET /api/firmware/getNewVersion.html`).

# Next Experiments
- Run `find_cached_assets.py` on the complete phone app cache directory (`/cache/diskcache/`) to isolate unencrypted temporary watch face assets.
- Open Wireshark packet logs, filter for `dns`, track requests to `dail.cynet2open.com`, and track companion file stream handshakes to pull download assets manually via browser.
- Decompile/Scan `extcfg.bin` and `usrcfg.bin` to isolate byte locations regulating frame rates.

# Open Questions
- What exact encryption key or header array does the CyFit framework pass to `dail.cynet2open.com:10090` to unlock the dial market database listing?
- Does `extcfg.bin` accept simple hex value overrides to change the UI frame rate target, or will altering it break system validation check sequences?

# Recent Discoveries
- **Exposed Backend Infrastructure URL:** Discovered the core domain mapping for all over-the-air resources: `http://dail.cynet2open.com:10090`.
- **Discovered API Paths:** Unmasked the direct endpoint used to call watch face lists: `/api/clockDial/page.html?page=1&limit=999&typeId=`.
- **Identified Hardware Log Key:** Discovered the hardware MAC target of the watch platform: `F4:4E:FC:44:84:FF`.

# Session Log History
### 2026-06-15
- Initial analysis of `ota_V1.03.11.bin`.
- Wrote initial binary scanning and slicing tools.
- Discovered multiple `AOTA` headers and nested files inside the update bundle.
- Recovered target system configurations (`extcfg.bin`, `usrcfg.bin`) via structural byte realignment.
- Intercepted encrypted phone network traffic via PCAPdroid.
- Located plain-text developer tracking logs (`cyNetLog.txt` and `cyBleLog.txt`) inside the rooted Samsung J7 Android application sandbox directory.
- Mapped out official open manufacturing servers (`dail.cynet2open.com:10090`) using Wireshark DNS handshake captures.
- Encountered connection dropouts when attempting anonymous script pings to the database API.
- Project paused for 1 month.

### 2026-07-11
- Workspace resumed. 
- Structured the workspace directory hierarchy (`Code/`, `Docs/`, `Photos/`, `Videos/`).
- Initialized `AI_Context.md` to serve as a persistent cross-agent memory ledger.

### 2026-07-11 (Update)
- Finalized project repository and workspace folder name convention: `fireboltt-invincible-plus-097-re`.
- Cleaned the root directory by migrating all runtime configuration assets (`map_cache.db`, `ota_V1.03.11.bin`, and compiler `zephyr.map`) into the unified `/Docs/` folder.