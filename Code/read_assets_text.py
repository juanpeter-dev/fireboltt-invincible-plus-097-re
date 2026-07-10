import os

target_path = os.path.join("unpacked_assets", "sdfs.txt")

print(f"[*] Reading unmasked configuration script: {target_path}\n")

if not os.path.exists(target_path):
    print(f"[!] Error: Missing '{target_path}'. Check your 'unpacked_assets' folder!")
    exit(1)

with open(target_path, "rb") as f:
    raw_bytes = f.read()

print("=== RAW BYTES VIEW ===")
print(raw_bytes.hex().upper())
print("\n" + "="*40 + "\n")

try:
    # Attempt to decode it as plain text
    decoded_text = raw_bytes.decode("utf-8", errors="ignore").strip()
    print("=== DECODED CONFIGURATION STRINGS ===")
    if decoded_text:
        print(decoded_text)
    else:
        print("[-] File contains data but returned an empty text string.")
except Exception as e:
    print(f"[!] Error decoding text string: {e}")