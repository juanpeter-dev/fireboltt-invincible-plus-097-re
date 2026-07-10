import os
import re

# Target the staging file extracted by our slicer
temp_path = os.path.join("extracted_ota", "TEMP.bin")

# Fallback check if it's in the root folder
if not os.path.exists(temp_path):
    temp_path = "TEMP.bin"

if not os.path.exists(temp_path):
    print("[!] Error: TEMP.bin was not found. Let's see what is in your folder:")
    if os.path.exists("extracted_ota"):
        print(os.listdir("extracted_ota"))
    exit(1)

print(f"[*] Extracting readable layout strings from {temp_path}...")
with open(temp_path, "rb") as f:
    data = f.read()

# Match clean ASCII sequences at least 5 characters long
ascii_pattern = re.compile(rb'[ -~]{5,}')
found_strings = []

for match in ascii_pattern.finditer(data):
    string_val = match.group().decode('ascii', errors='ignore').strip()
    # Filter out pure numbers to keep the list clean
    if string_val and not string_val.isdigit():
        found_strings.append(string_val)

print(f"\n[+] Discovered {len(found_strings)} text strings inside the patch binary!")
print("=== FIRST 30 STRINGS UNMASKED ===")
for s in found_strings[:30]:
    print(f"  -> {s}")