import re

def extract_strings_from_bin(bin_path, output_txt_path, min_length=4):
    print(f"[*] Analyzing flat code blocks inside: {bin_path}")
    
    # Standard regex pattern to catch clean, human-readable ASCII strings
    ascii_pattern = re.compile(rb'[ -~]{' + bytes(str(min_length), 'utf-8') + rb',}')
    
    found_strings = []
    
    with open(bin_path, "rb") as f:
        data = f.read()
        
    # Scan through the entire uncompressed binary address space
    for match in ascii_pattern.finditer(data):
        offset = match.start()
        string_val = match.group().decode('ascii', errors='ignore').strip()
        
        if string_val:
            found_strings.append(f"Offset [{hex(offset)}]: {string_val}")
            
    print(f"[+] Successfully extracted {len(found_strings)} string sequences.")
    print(f"[*] Exporting catalog report to: {output_txt_path}")
    
    with open(output_txt_path, "w", encoding="utf-8") as out:
        out.write("\n".join(found_strings))
        
    print("[SUCCESS] String extraction report complete!")

# Run the string parsing extraction loop
extract_strings_from_bin("zephyr_pure_code.bin", "extracted_zephyr_strings.txt")