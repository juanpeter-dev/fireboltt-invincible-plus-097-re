import os
import struct

def unpack_sdfs_container(ota_path):
    print(f"[*] Scanning OTA container for SDFS filesystem blocks: {ota_path}")
    
    if not os.path.exists(ota_path):
        print(f"[!] Error: {ota_path} not found in workspace.")
        return

    with open(ota_path, "rb") as f:
        data = f.read()

    # Look for the Actions Magic Header "AOTA" (41 4F 54 41)
    header_offset = data.find(b"AOTA")
    if header_offset == -1:
        print("[!] Could not locate valid 'AOTA' firmware signature header.")
        return
        
    print(f"[+] Found AOTA firmware boundary at offset: {hex(header_offset)}")
    
    # Let's search for embedded file signatures like "ota.xml" or ".bin" structures
    # to find where the resource blocks start
    targets = [b"ota.xml", b"sdfs_k.bin", b"TEMP.bin"]
    
    print("\n[*] Mapping internal file partition table components...")
    for target in targets:
        offset = data.find(target)
        if offset != -1:
            print(f" [+] Found component target '{target.decode()}': Absolute Offset {hex(offset)}")
            
            # Print a small hex window around the filename to inspect the partition details
            window = data[offset - 16 : offset + 32]
            print(f"     Context Hex: {window.hex().upper()}")
        else:
            print(f" [-] Component target '{target.decode()}' not discovered in this image block.")

unpack_sdfs_container("ota_V1.03.11.bin")