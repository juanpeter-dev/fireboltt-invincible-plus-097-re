import os

sdfs_file = os.path.join("extracted_clean", "Block2_System_sdfs.bin")

print(f"[*] Analyzing extracted resource file system partition: {sdfs_file}")

if not os.path.exists(sdfs_file):
    print(f"[!] Error: Missing {sdfs_file}. Double check your folder!")
    exit(1)

with open(sdfs_file, "rb") as f:
    sdfs_data = f.read()

print(f"[+] Loaded {len(sdfs_data)} bytes of raw resource stream.")

# Typical asset tags used by Actions Semi graphic systems (GDI, Fonts, Images, XML layouts)
keywords = [b"pic", b"img", b"font", b"ui", b"bg", b"theme", b".res", b".gdi"]

print("\n=== SCANNING FOR INTERNAL ASSET MARKERS ===")
found = False

for kw in keywords:
    offset = 0
    while True:
        offset = sdfs_data.find(kw, offset)
        if offset == -1:
            break
            
        # Grab a small text window around the keyword to see if it's a file path or asset name
        start_win = max(0, offset - 8)
        end_win = min(len(sdfs_data), offset + len(kw) + 12)
        window_bytes = sdfs_data[start_win:end_win]
        
        # Translate to human-readable string characters
        readable_str = "".join(chr(b) if 32 <= b <= 126 else "." for b in window_bytes)
        
        print(f" [+] Found match for '{kw.decode()}': Absolute Position {hex(offset)} -> Context: [{readable_str}]")
        found = True
        offset += len(kw)

if not found:
    print("[-] No immediate raw text asset tags found. The file system might be pure binary headers.")