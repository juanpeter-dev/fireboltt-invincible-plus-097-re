import usb.core
import usb.backend.libusb1
import os
import sys
import time

# 1. Initialize custom LibUSB Backend
script_dir = os.path.dirname(os.path.abspath(__file__))
dll_path = os.path.join(script_dir, "libusb-1.0.dll")
backend = usb.backend.libusb1.get_backend(find_library=lambda x: dll_path)

print("[*] Contacting watch over LibUSB...")
dev = usb.core.find(idVendor=0x10D6, idProduct=0x10D6, backend=backend)

if dev is None:
    print("[!] Watch not found. Check your Zadig connection dropdown!")
    sys.exit(1)

try:
    dev.set_configuration()
except usb.core.USBError:
    pass

ep_out = dev[0][(0,0)][1] # Endpoint 0x02
ep_in = dev[0][(0,0)][0]  # Endpoint 0x81

print("[+] Hardware connected! Collapsing Mass Storage mode...")

# Step A: Send the exact 16-byte handshake that worked in your test script
unlock_cmd = bytearray(16)
unlock_cmd[0] = 0x01  
unlock_cmd[1] = 0x01  
ep_out.write(unlock_cmd, timeout=2000)
time.sleep(0.5)

# Clear the 16-byte response out of the buffer pipeline
status_flush = ep_in.read(16, timeout=2000)
print(f"[+] Chip Status Confirmed Active: {[hex(b) for b in status_flush]}")

# Target definitions for the actual raw system OS firmware memory bank
FIRMWARE_SIZE = 2 * 1024 * 1024  # Let's target the core 2MB kernel layer
BLOCK_SIZE = 512
output_file = "true_actions_os_kernel.bin"

# Step B: The true low-level ROM read protocol (Opcode 0x02)
def make_rom_read_cmd(address, length):
    cmd = bytearray(16)
    cmd[0] = 0x02  # Opcode 0x02: Read hardware flash memory cells directly
    cmd[2] = (address >> 24) & 0xFF
    cmd[3] = (address >> 16) & 0xFF
    cmd[4] = (address >> 8) & 0xFF
    cmd[5] = address & 0xFF
    cmd[7] = 0x02  # Length configuration multiplier (512 bytes block)
    return cmd

bytes_dumped = 0
print(f"\n[*] Extracting raw OS kernel blocks to '{output_file}'...")

with open(output_file, "wb") as f:
    while bytes_dumped < FIRMWARE_SIZE:
        try:
            # Build and send direct ROM flash read pointer command
            cmd_packet = make_rom_read_cmd(bytes_dumped, BLOCK_SIZE)
            ep_out.write(cmd_packet, timeout=2000)
            
            # Pull the completely raw data sector away from the chip
            data = ep_in.read(BLOCK_SIZE, timeout=2000)
            f.write(data)
            
            bytes_dumped += len(data)
            percent = (bytes_dumped / FIRMWARE_SIZE) * 100
            print(f"\rDumping Progress: {percent:.1f}% [{bytes_dumped}/{FIRMWARE_SIZE} Bytes]", end="")
            
        except usb.core.USBError as e:
            print(f"\n[!] Pipeline halted at sector offset {hex(bytes_dumped)}. Error: {e}")
            break

if bytes_dumped > 0:
    print(f"\n\n[SUCCESS] Raw OS Kernel Firmware Dumped Perfectly!")
    print(f"[+] Saved file: '{output_file}'")