import os
import struct

sdfs_source = os.path.join("extracted_clean", "Block2_System_sdfs.bin")
output_dir = "unpacked_assets"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print(f"[*] Extracting internal system configuration sheets from: {sdfs_source}")
with open(sdfs_source, "rb") as f:
    data = f.read()

# Scan through the index sector (first 256 bytes handles the asset file definitions)
entry_size = 32
table_limit = 256

for offset in range(0, table_limit, entry_size):
    entry = data[offset:offset + entry_size]
    if len(entry) < entry_size or entry == b'\x00' * entry_size:
        continue
        
    # Read Name
    name_bytes = entry[0:16]
    file_name = name_bytes.split(b'\x00')[0].decode('ascii', errors='ignore').strip()
    file_name = "".join(c for c in file_name if c.isalnum() or c in "._-")
    
    # Read pointers
    try:
        rel_offset = struct.unpack("<I", entry[16:20])[0]
        file_size = struct.unpack("<I", entry[20:24])[0]
    except Exception:
        continue
        
    if file_name and file_size > 0:
        print(f" [+] Found Inner Configuration Block: '{file_name}'")
        print(f"     Relative Offset: {hex(rel_offset)} | Length: {file_size} Bytes")
        
        # Slice payload
        payload = data[rel_offset : rel_offset + file_size]
        
        out_path = os.path.join(output_dir, file_name)
        with open(out_path, "wb") as out_f:
            out_f.write(payload)
        print(f"     Saved file to: {out_path}")

print("\n[SUCCESS] Internal asset configuration extraction cycle completed!")