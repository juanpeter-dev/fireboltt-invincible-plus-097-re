import os
import struct

sdfs_source = os.path.join("extracted_clean", "Block2_System_sdfs.bin")
output_dir = "unpacked_assets"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print(f"[*] Extracting system configuration files from: {sdfs_source}")
with open(sdfs_source, "rb") as f:
    data = f.read()

# Scan through the index sector 32 bytes at a time
entry_size = 32
table_limit = 256

for offset in range(0, table_limit, entry_size):
    entry = data[offset:offset + entry_size]
    if len(entry) < entry_size or entry == b'\x00' * entry_size:
        continue
        
    # Bytes 0-11: Filename string
    name_bytes = entry[0:12]
    file_name = name_bytes.split(b'\x00')[0].decode('ascii', errors='ignore').strip()
    file_name = "".join(c for c in file_name if c.isalnum() or c in "._-")
    
    try:
        # Bytes 12-15: File Size (4-byte unsigned int)
        file_size = struct.unpack("<I", entry[12:16])[0]
        # Bytes 16-19: Relative Offset Pointer (4-byte unsigned int)
        rel_offset = struct.unpack("<I", entry[16:20])[0]
    except Exception:
        continue
        
    if file_name and file_size > 0:
        print(f" [+] Found Inner File: '{file_name}'")
        print(f"     Target Offset: {hex(rel_offset)} | Size: {file_size} Bytes")
        
        # Guard check to ensure the slice is within the physical file size
        if rel_offset + file_size <= len(data):
            payload = data[rel_offset : rel_offset + file_size]
            
            out_path = os.path.join(output_dir, file_name)
            with open(out_path, "wb") as out_f:
                out_f.write(payload)
            print(f"     Successfully saved to: {out_path}")
        else:
            print(f"     [!] Warning: Slice {hex(rel_offset)} is out of bounds!")

print("\n[SUCCESS] Extraction complete! Check your 'unpacked_assets' folder.")