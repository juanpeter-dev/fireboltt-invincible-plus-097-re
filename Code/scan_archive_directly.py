import os
import re

target_file = "ota_V1.03.11.bin"

if not os.path.exists(target_file):
    print(f"[!] Error: Cannot find '{target_file}' in this folder.")
    print(f"Current folder contents: {os.listdir('.')}")
    exit(1)

print(f"[*] Scanning {target_file} directly for readable system strings...")
with open(target_file, "rb") as f:
    data = f.read()

# Match clean ASCII text sequences that are at least 5 characters long
ascii_pattern = re.compile(rb'[ -~]{5,}')
found_strings = []

for match in ascii_pattern.finditer(data):
    string_val = match.group().decode('ascii', errors='ignore').strip()
    # Filter out pure numbers and standard XML tags we already saw
    if string_val and not string_val.isdigit() and "ota_firmware" not in string_val:
        found_strings.append(string_val)

print(f"\n[+] Discovered {len(found_strings)} strings inside the binary archive!")
print("=== FIRMWARE STRING SNAPSHOT (First 40 Strings) ===")
for s in found_strings[:40]:
    print(f"  -> {s}")