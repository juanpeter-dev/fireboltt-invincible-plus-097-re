import os

target_file = "ota_V1.03.11.bin"

if not os.path.exists(target_file):
    print(f"[!] Target file '{target_file}' missing.")
    exit(1)

with open(target_file, "rb") as f:
    # Jump straight to the exact byte location we unmasked in your partition table
    f.seek(0x200)
    raw_chunk = f.read(32)

print("=== RAW HEX ANALYSIS ===")
print(f"Bytes (Hex): {raw_chunk.hex().upper()}")
print("\n=== ASCII TEXT VIEW ===")
# Show any printable text characters, substitute unprintable junk with dots
ascii_view = "".join(chr(b) if 32 <= b <= 126 else "." for b in raw_chunk)
print(ascii_view)
