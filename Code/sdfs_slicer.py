import os
import struct

def extract_all_partitions(ota_path, output_dir="extracted_ota"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    print(f"[*] Opening target package: {ota_path}")
    with open(ota_path, "rb") as f:
        data = f.read()
        
    # The partition index area resides between 0x200 and 0x400
    table_start = 0x200
    table_end = 0x400
    entry_size = 32
    
    print("[*] Slicing firmware compartments based on index table markers...")
    
    for offset in range(table_start, table_end, entry_size):
        entry = data[offset:offset + entry_size]
        
        # If the entry is empty padding, skip it
        if entry == b'\x00' * entry_size or len(entry) < entry_size:
            continue
            
        # Extract metadata pointers
        file_offset = struct.unpack("<I", entry[0:4])[0]
        file_size = struct.unpack("<I", entry[4:8])[0]
        
        # Read the file name string (up to 16 bytes long)
        name_bytes = entry[16:32]
        file_name = name_bytes.split(b'\x00')[0].decode('ascii', errors='ignore').strip()
        
        if file_name and file_size > 0:
            print(f"\n[+] Found Index Record: '{file_name}'")
            print(f"    Data Offset Threshold : {hex(file_offset)}")
            print(f"    Data Stream Length    : {file_size} Bytes")
            
            # Slice the data chunk out of the main container
            file_payload = data[file_offset : file_offset + file_size]
            
            output_path = os.path.join(output_dir, file_name)
            with open(output_path, "wb") as out_file:
                out_file.write(file_payload)
                
            print(f"    Saved successfully to: {output_path}")

extract_all_partitions("ota_V1.03.11.bin")