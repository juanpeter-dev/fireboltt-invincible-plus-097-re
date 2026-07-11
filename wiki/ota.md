# Custom Update Containers (Project Nickname: AOTA)

## 1. Structure Specifications
- **Container Format Classification:** Custom multi-image vendor container layout format (**Project Nickname: AOTA** / Official Format Name: *Unknown*).
- **Status:** CONFIRMED
- **Evidence Reference:** `[E004]` (Direct byte parsing via custom Python extractor code).
- **Observed Data:** The container file layout starts with a structured index block followed by alignment markers that map out separate code tracks for `app.bin` and `sdfs.bin`.
- **Why this matters:** Mapping these structural boundaries allows us to safely inject modified sub-images back into the firmware package without corrupting file offsets.

## 2. Validation & Security Trailing Elements
- **Hypothesis:** The update verification routine relies on fixed checksum trailing blocks or cryptographic signatures attached to the end of the package archive.
- **Negative Evidence:** Deployed scripts have not yet encountered or tripped active signature verification locks because we haven't attempted to flash an altered binary to the physical watch hardware.
- **What would disprove it:** Modifying a single structural byte inside an OTA container, pushing the update to the watch via Bluetooth, and seeing it install cleanly without triggering signature block rejections.
- **Future Research Vector:** Locate the specific software component in the update app layer that processes new firmware packages, and look for verification codes matching standard hashing or signing functions (like CRC32, MD5, SHA256, or RSA algorithms).