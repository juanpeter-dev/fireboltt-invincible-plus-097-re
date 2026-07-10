import os

# Define path to the extracted SDFS data partition file
sdfs_path = os.path.join("extracted_ota", "sdfs_k.bin")

print(f"[*] Scanning SDFS system partition image: {sdfs_path}")

if not os.path.exists(sdfs_path):
    print(f"[!] Error: Missing file {sdfs_path}. Run your previous slicer first!")
    exit(1)

with open(sdfs_path, "rb") as f:
    sdfs_data = f.read()

print(f"[+] Successfully loaded SDFS cluster data ({len(sdfs_data)} bytes)")

# Typical file extension tags used inside Actions Semi SDFS resource partitions
resource_keys = [b".res", b".bin", b".gdi", b".fnt", b".png", b".xml"]

print("\n=== DETECTED INTERNAL SDFS RESOURCE BLOCKS ===")
found_any = False

for key in resource_keys:
    offset = 0
    while True:
        offset = sdfs_data.find(key, offset)
        if offset == -1:
            break
            
        # Extract a small context window around where the file extension was discovered
        # to try to capture the full file name text string
        start_win = max(0, offset - 12)
        end_win = min(len(sdfs_data), offset + len(key) + 4)
        context = sdfs_data[start_win:end_win]
        
        # Clean up text display
        clean_name = "".join(chr(b) if 32 <= b <= 126 else "" for b in context).strip()
        
        if len(clean_name) > len(key):
            print(f" [+] Found asset hook matching '{key.decode()}' at Absolute Offset: {hex(offset)} -> Context: [{clean_name}]")
            found_any = True
            
        offset += len(key)

if not found_any:
    print("[!] No obvious raw ASCII asset strings found. The system image might use a structured lookup table header.")