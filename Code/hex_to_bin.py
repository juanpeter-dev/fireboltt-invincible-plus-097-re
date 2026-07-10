import os

def convert_intel_hex_to_bin(hex_input_path, bin_output_path):
    print(f"[*] Parsing Intel HEX container: {hex_input_path}")
    
    current_upper_address = 0
    memory_dict = {}
    
    with open(hex_input_path, "r") as hex_file:
        for line_num, line in enumerate(hex_file, 1):
            line = line.strip()
            if not line.startswith(':'):
                continue
                
            try:
                # Parse Intel HEX fields
                byte_count = int(line[1:3], 16)
                address_offset = int(line[3:7], 16)
                record_type = int(line[7:9], 16)
                
                # Type 00: Data Record
                if record_type == 0:
                    data_bytes = bytes.fromhex(line[9:9 + (byte_count * 2)])
                    # Compute absolute target memory location
                    absolute_address = (current_upper_address << 16) + address_offset
                    
                    for i, byte in enumerate(data_bytes):
                        memory_dict[absolute_address + i] = byte
                        
                # Type 04: Extended Linear Address (Changes the target memory bank pointer)
                elif record_type == 4:
                    current_upper_address = int(line[9:13], 16)
                    
                # Type 01: End of File
                elif record_type == 1:
                    print(f"[+] Reached EOF marker at line {line_num}.")
                    break
            except ValueError:
                print(f"[!] Warning: Skipping malformed formatting on line {line_num}")
                continue

    if not memory_dict:
        print("[!] Error: No valid data sectors mapped from the HEX container.")
        return

    # Find boundaries of the compiled code space
    min_addr = min(memory_dict.keys())
    max_addr = max(memory_dict.keys())
    total_span = max_addr - min_addr + 1
    
    print(f"[+] Binary spans from address {hex(min_addr)} to {hex(max_addr)}")
    print(f"[*] Flattening code arrays into raw component output ({total_span} bytes)...")
    
    # Pack memory dictionary map sequentially into a flat file chunk array
    output_buffer = bytearray(total_span)
    for addr, byte_val in memory_dict.items():
        output_buffer[addr - min_addr] = byte_val
        
    with open(bin_output_path, "wb") as bin_file:
        bin_file.write(output_buffer)
        
    print(f"[SUCCESS] Flat binary exported flawlessly: '{bin_output_path}' ({os.path.getsize(bin_output_path)} bytes)")

# Kick off processing loop
convert_intel_hex_to_bin("zephyr.hex", "zephyr_pure_code.bin")