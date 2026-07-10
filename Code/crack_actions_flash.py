import usb.core
import usb.backend.libusb1
import os
import sys
import time

script_dir = os.path.dirname(os.path.abspath(__file__))
dll_path = os.path.join(script_dir, "libusb-1.0.dll")
backend = usb.backend.libusb1.get_backend(find_library=lambda x: dll_path)

dev = usb.core.find(idVendor=0x10D6, idProduct=0x10D6, backend=backend)
if dev is None:
    print("[!] Watch beacon not found. Re-verify device presence!")
    sys.exit(1)

try:
    dev.set_configuration()
except:
    pass

ep_out = dev[0][(0,0)][1] # Endpoint 0x02
ep_in = dev[0][(0,0)][0]  # Endpoint 0x81

print("[*] Forcing ADFU chip memory control registers...")

# Step 1: Force a core reset command directly to the bootloader pipeline
init_packet = bytearray(16)
init_packet[0] = 0x01 # Reset mapping context
init_packet[1] = 0x02 # Sub-type 0x02: Explicitly switch target to System Flash ROM
ep_out.write(init_packet, timeout=2000)
time.sleep(0.5)
try:
    ep_in.read(16, timeout=1000) # Clear response wrapper
except:
    pass

# Step 2: Custom raw Flash Block Read command sequence (Bypassing SCSI USBS)
def make_hardware_flash_read(offset_blocks, count_blocks):
    cmd = bytearray(16)
    cmd[0] = 0x02  # Main Opcode: Read Direct
    cmd[1] = 0x04  # Sub-Opcode 0x04: TARGET HARDWARE SPI DIRECT RAW SECTORS (Crucial bypass!)
    
    # Map the address into the sector configuration bytes
    cmd[2] = (offset_blocks >> 24) & 0xFF
    cmd[3] = (offset_blocks >> 16) & 0xFF
    cmd[4] = (offset_blocks >> 8) & 0xFF
    cmd[5] = offset_blocks & 0xFF
    
    cmd[8] = count_blocks & 0xFF # Number of 512-byte blocks to pull at once
    return cmd

# Let's extract the first 1MB where the core boot images and sdfs reside
TOTAL_SIZE = 1 * 1024 * 1024 
BLOCK_SIZE = 512
blocks_to_read = TOTAL_SIZE // BLOCK_SIZE

print("[*] Extracting raw chip partitions... Looking for 'AOTA' / 'sdfs' structural vectors.")
bytes_saved = 0

with open("actions_raw_flash_cracked.bin", "wb") as f:
    for block in range(blocks_to_read):
        try:
            # Request 1 raw physical block at a time
            cmd_payload = make_hardware_flash_read(block, 1)
            ep_out.write(cmd_payload, timeout=2000)
            
            # Read out the raw sector array
            data = ep_in.read(BLOCK_SIZE, timeout=2000)
            f.write(data)
            
            bytes_saved += len(data)
            print(f"\rRead progress: {bytes_saved}/{TOTAL_SIZE} Bytes", end="")
            
        except usb.core.USBError as e:
            print(f"\n[!] Read stopped at block {block}: {e}")
            break

print("\n\n[+] Dump complete. Run this file through HxD right now!")