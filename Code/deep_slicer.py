import os
import struct

def deep_slice_ota(file_path, output_dir="deep_extracted"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"[*] Beginning deep scan of container: {file_path}")
    with open(file_path, "rb") as f:
        data = f.read()

    # Find every single occurrence of the AOTA magic header string
    offset = 0
    container_count = 0
    aota_offsets = []
    
    while True:
        offset = data.find(b"AOTA", offset)
        if offset == -1:
            break
        aota_offsets.append(offset)
        offset += 4 # Move past this header to find the next one

    print(f"[+] Found {len(aota_offsets)} independent AOTA system blocks inside the binary!")
    
    for i, start_offset in enumerate(aota_offsets):
        container_count += 1
        print(f"\n--- Processing Block #{container_count} (Starting at Offset: {hex(start_offset)}) ---")
        
        # The partition index table always sits exactly 0x200 bytes after the AOTA magic word
        table_start = start_offset + 0x200
        table_end = start_offset + 0x400
        entry_size = 32
        
        for table_offset in range(table_start, table_end, entry_size):
            entry = data[table_offset:table_offset + entry_size]
            
            if entry == b'\x00' * entry_size or len(entry) < entry_size:
                continue
                
            try:
                # Extract file storage parameters (relative to this specific AOTA block)
                rel_file_offset = struct.unpack("<I", entry[0:4])[0]
                file_size = struct.unpack("<I", entry[4:8])[0]
                
                # Extract filename characters
                name_bytes = entry[16:32]
                file_name = name_bytes.split(b'\x00')[0].decode('ascii', errors='ignore').strip()
                
                # Sanitize the filename to prevent folder escape issues
                file_name = "".join(c for c in file_name if c.isalnum() or c in "._-")
                
                if file_name and file_size > 0:
                    # Calculate where the file actually sits globally inside our .bin archive
                    abs_file_offset = start_offset + rel_file_offset
                    
                    print(f" [+] Found Index Record: '{file_name}'")
                    print(f"     Global Absolute Position : {hex(abs_file_offset)}")
                    print(f"     Payload Size              : {file_size} Bytes")
                    
                    # Slice the exact payload size window
                    payload = data[abs_file_offset : abs_file_offset + file_size]
                    
                    # Prevent overwriting files with identical names across blocks
                    unique_name = f"block{container_count}_{file_name}"
                    output_path = os.path.join(output_dir, unique_name)
                    
                    with open(output_path, "wb") as out_file:
                        out_file.write(payload)
                    print(f"     Saved file safely to: {output_path}")
            except Exception as e:
                print(f"     [!] Problem parsing index record entry: {e}")

deep_slice_ota("ota_V1.03.11.bin")