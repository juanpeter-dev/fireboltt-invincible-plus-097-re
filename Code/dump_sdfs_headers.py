import os

sdfs_file = os.path.join("extracted_clean", "Block2_System_sdfs.bin")

if not os.path.exists(sdfs_file):
    print(f"[!] Error: Missing file {sdfs_file}")
    exit(1)

print(f"[*] Hex-dumping header coordinates of: {sdfs_file}\n")
with open(sdfs_file, "rb") as f:
    header_data = f.read(128)

print("Offset (Hex)  | Raw Binary Hex Bytes                              | ASCII View")
print("-" * 78)

# Read the data in clean 16-byte rows
for offset in range(0, len(header_data), 16):
    chunk = header_data[offset:offset+16]
    
    # Format the raw bytes into clean two-digit hex characters
    hex_string = " ".join(f"{b:02X}" for b in chunk)
    # Ensure proper row spacing if the file ends prematurely
    hex_string = hex_string.ljust(47)
    
    # Build the matching printable text column
    ascii_string = "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk)
    
    print(f"0x{offset:08X}    | {hex_string} | {ascii_string}")