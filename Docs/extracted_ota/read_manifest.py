import os

manifest_path = os.path.join("extracted_ota", "ota.xml")

print(f"[*] Reading raw manifest data from: {manifest_path}")

if not os.path.exists(manifest_path):
    print(f"[!] Error: Cannot find {manifest_path}. Did sdfs_slicer.py run successfully?")
    exit(1)

with open(manifest_path, "r", encoding="utf-8", errors="ignore") as f:
    text_content = f.read()

# Let's pull out any lines that look like XML tags or file configurations
lines = text_content.splitlines()
print("\n=== DECODED MANIFEST MOUNT POINTS ===")

printed_lines = 0
for line in lines:
    clean_line = line.strip()
    # Look for file indicators, partition names, or size configs
    if any(keyword in clean_line.lower() for keyword in ["file", "name", "id", "type", "partition", "am_sdfs"]):
        print(clean_line)
        printed_lines += 1

if printed_lines == 0:
    print("[!] No standard XML text lines found. The file might be compressed binary data.")
    print(f"[*] Showing first 200 raw characters instead:\n{text_content[:200]}")