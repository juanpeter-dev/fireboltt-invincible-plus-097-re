import os
import struct

target_file = "ota_V1.03.11.bin"
output_dir = "extracted_clean"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print(f"[*] Extracting partitions using corrected structural alignment from: {target_file}")
with open(target_file, "rb") as f:
    data = f.read()

# Define our two confirmed unencrypted index points
targets = [
    {"name": "Block1_Staging", "aota_offset": 0x0},
    {"name": "Block2_System",  "aota_offset": 0x800}
]

for tgt in targets:
    start = tgt["aota_offset"]
    print(f"\n[*] Processing partition block: {tgt['name']} ({hex(start)})")
    
    table_start = start + 0x200
    table_end = start + 0x400
    entry_size = 32
    
    for offset in range(table_start, table_end, entry_size):
        entry = data[offset:offset + entry_size]
        if entry == b'\x00' * entry_size or len(entry) < entry_size:
            continue
            
        # Layout Alignment: 
        # Bytes 0-15  -> Filename String
        # Bytes 16-19 -> Relative Offset (4-byte unsigned int)
        # Bytes 20-23 -> File Size (4-byte unsigned int)
        name_bytes = entry[0:16]
        file_name = name_bytes.split(b'\x00')[0].decode('ascii', errors='ignore').strip()
        file_name = "".join(c for c in file_name if c.isalnum() or c in "._-")
        
        try:
            rel_offset = struct.unpack("<I", entry[16:20])[0]
            file_size = struct.unpack("<I", entry[20:24])[0]
        except Exception:
            continue
        
        if file_name and file_size > 0:
            abs_offset = start + rel_offset
            print(f" [+] Found File Record: '{file_name}'")
            print(f"     Location Pointer : {hex(abs_offset)}")
            print(f"     Payload Size     : {file_size} Bytes")
            
            # Slice the binary safely
            end_slice = min(abs_offset + file_size, len(data))
            payload = data[abs_offset : end_slice]
            
            out_path = os.path.join(output_dir, f"{tgt['name']}_{file_name}")
            with open(out_path, "wb") as out_f:
                out_f.write(payload)
            print(f"     Saved file slice to: {out_path}")

print("\n[SUCCESS] Targeted extraction completed cleanly!")