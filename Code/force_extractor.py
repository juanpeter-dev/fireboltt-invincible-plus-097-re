import os
import struct

target_file = "ota_V1.03.11.bin"
output_dir = "extracted_clean"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print(f"[*] Force-extracting partitions from: {target_file}")
with open(target_file, "rb") as f:
    data = f.read()

# Target our two verified unencrypted blocks
targets = [
    {"name": "Block1_Staging", "aota_offset": 0x0},
    {"name": "Block2_System",  "aota_offset": 0x800}
]

for tgt in targets:
    start = tgt["aota_offset"]
    print(f"\n[*] Processing {tgt['name']} at offset {hex(start)}...")
    
    table_start = start + 0x200
    table_end = start + 0x400
    entry_size = 32
    
    for offset in range(table_start, table_end, entry_size):
        entry = data[offset:offset + entry_size]
        if entry == b'\x00' * entry_size or len(entry) < entry_size:
            continue
            
        rel_offset = struct.unpack("<I", entry[0:4])[0]
        file_size = struct.unpack("<I", entry[4:8])[0]
        
        name_bytes = entry[16:32]
        file_name = name_bytes.split(b'\x00')[0].decode('ascii', errors='ignore').strip()
        file_name = "".join(c for c in file_name if c.isalnum() or c in "._-")
        
        if file_name and file_size > 0:
            abs_offset = start + rel_offset
            print(f" [+] Index Entry Found: '{file_name}'")
            print(f"     Target Slice: {hex(abs_offset)} to {hex(abs_offset + file_size)} ({file_size} Bytes)")
            
            # Slice the data, capping it safely at the absolute end of the file if it overflows
            end_slice = min(abs_offset + file_size, len(data))
            payload = data[abs_offset : end_slice]
            
            out_path = os.path.join(output_dir, f"{tgt['name']}_{file_name}")
            with open(out_path, "wb") as out_f:
                out_f.write(payload)
            print(f"     Successfully saved slice to: {out_path}")

print("\n[SUCCESS] Force extraction complete!")