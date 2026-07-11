# CyFit Framework Application Analysis

The mobile application wrapper (**FB Invincible Plus**) serves as our primary soft window into the hidden operational rules of the watch hardware. Reversing this codebase is our highest-value path to understanding the device's encryption steps and network requests.

## 1. Target Package Architecture
- **Primary Package Space:** `com.app.cy.fireboltt`
- **Underlying SDK Substructure:** Core frameworks rely heavily on the **CyFit platform layout**, a shared architecture used across multiple health and lifestyle smart devices built on Actions chips.

## 2. High-Value Code Targets for Reverse Engineering

### Network Layer & API Routings
- **Target Target Classes:** Look for HTTP frameworks like `retrofit2.Retrofit` or implementations using `okhttp3.OkHttpClient`.
- **Core Goal:** Locate the exact interceptor classes that append custom HTTP headers to outgoing requests. If we can map out how these headers are created, we can stop anonymous connection drops on our Python scripts and pull down watch assets freely.

### Local Cache Cryptographic Schemes
- **Evidence Reference:** `[E005]`
- **Observed Data:** Database parsing exposed fields named `metadata_nonce` and `data_nonce` right next to encrypted BLOB columns inside `map_cache.db`.
- **Interpretation:** The application uses Authenticated Encryption with Associated Data (AEAD) layers to secure data at rest.
- **Possible Implementations:**
  - Android Jetpack Security (`EncryptedSharedPreferences` / `EncryptedFile` wrappers).
  - Custom SQLCipher integration layered over the core SQLite database driver frameworks.
  - AES-GCM or ChaCha20-Poly1305 cipher routines run manually before database insertion.
- **Future Research Vector:** Use JADX to decompile the application jar archives and trace search filters for keyword sequences matching `Cipher.getInstance` or `javax.crypto.spec` to pinpoint the exact encryption routines.

## 3. Artifact Wishlist for APK Analysis
- **Decompiled Java Source Tree (via JADX-GUI):** Crucial to read the plaintext networking modules and learn how to reproduce authentic API queries.
- **JNI Native Library Mapping (`.so` files):** Checking native components like `libcyfit.so` or similar libraries will show us if the security handshakes or update validation hashes are handled by compiled C/C++ code blocks rather than Java classes.