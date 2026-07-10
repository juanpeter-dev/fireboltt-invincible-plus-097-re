import os

target_file = "ota_V1.03.11.bin"

if not os.path.exists(target_file):
    print(f"[!] Error: Cannot find {target_file}")
    exit(1)

# The exact AOTA block offsets found by your deep scan
block_offsets = [0x0, 0x800, 0xdf758]

with open(target_file, "rb") as f:
    data = f.read()

print("=== DEEP INDEX TABLE ANALYSIS ===")

for i, start in enumerate(block_offsets):
    print(f"\n[Block #{i+1} Table Snapshot (AOTA position: {hex(start)})]")
    
    # Read the 64 bytes where the first two file index records should live
    # (+0x200 bytes past the AOTA string)
    table_index = start + 0x200
    table_bytes = data[table_index:table_index + 64]
    
    print(f"  Raw Hex:  {table_bytes.hex().upper()}")
    
    # Show it as readable ASCII characters to see if we can spot the cipher text
    ascii_view = "".join(chr(b) if 32 <= b <= 126 else "." for b in table_bytes)
    print(f"  ASCII:    {ascii_view}")