import os
import struct

target_file = "ota_V1.03.11.bin"
output_dir = "extracted_clean"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print(f"[*] Extracting verified containers from: {target_file}")
with open(target_file, "rb") as f:
    data = f.read()

# Explicitly target our two verified unencrypted AOTA blocks
targets = [
    {"name": "Block1_Staging", "aota_offset": 0x0},
    {"name": "Block2_System",  "aota_offset": 0x800}
]

for tgt in targets:
    start = tgt["aota_offset"]
    print(f"\n[*] Processing verified {tgt['name']} at offset {hex(start)}...")
    
    # Read the precise file indices at +0x200
    table_start = start + 0x200
    table_end = start + 0x400
    entry_size = 32
    
    for offset in range(table_start, table_end, entry_size):
        entry = data[offset:offset + entry_size]
        if entry == b'\x00' * entry_size or len(entry) < entry_size:
            continue
            
        # Parse layout markers
        rel_offset = struct.unpack("<I", entry[0:4])[0]
        file_size = struct.unpack("<I", entry[4:8])[0]
        
        # Read file name string
        name_bytes = entry[16:32]
        file_name = name_bytes.split(b'\x00')[0].decode('ascii', errors='ignore').strip()
        file_name = "".join(c for c in file_name if c.isalnum() or c in "._-")
        
        if file_name and file_size > 0:
            abs_offset = start + rel_offset
            
            # Bound check to prevent running into ghost sections
            if abs_offset + file_size <= len(data):
                print(f" [+] Found Valid File: '{file_name}'")
                print(f"     Absolute Location: {hex(abs_offset)} | Size: {file_size} Bytes")
                
                payload = data[abs_offset : abs_offset + file_size]
                out_path = os.path.join(output_dir, f"{tgt['name']}_{file_name}")
                
                with open(out_path, "wb") as out_f:
                    out_f.write(payload)
                print(f"     Saved to: {out_path}")

print("\n[SUCCESS] Clean extraction loop completed!")