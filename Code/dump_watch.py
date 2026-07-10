import usb.core
import usb.backend.libusb1
import os
import sys
import time

# 1. Force Backend Binding
script_dir = os.path.dirname(os.path.abspath(__file__))
dll_path = os.path.join(script_dir, "libusb-1.0.dll")
backend = usb.backend.libusb1.get_backend(find_library=lambda x: dll_path)

print("[*] Locating watch in ADFU state...")
dev = usb.core.find(idVendor=0x10D6, idProduct=0x10D6, backend=backend)

if dev is None:
    print("[!] Watch not found. Make sure it is plugged in and the screen is blank.")
    sys.exit(1)

print("[+] Watch found! Initializing raw USB interface...")

try:
    dev.set_configuration()
except usb.core.USBError as e:
    pass

cfg = dev.get_active_configuration()
intf = cfg[(0,0)]
ep_out = dev[0][(0,0)][1] # Endpoint 0x02
ep_in = dev[0][(0,0)][0]  # Endpoint 0x81

# 2. Raw ADFU Target Parameters
# We target the standard base execution mapping address for Actions systems (0xbfc00000)
# to completely bypass the storage controllers.
START_ADDRESS = 0xbfc00000 
DUMP_SIZE = 2 * 1024 * 1024 # Let's pull a 2MB core chunk first
BLOCK_SIZE = 512 
output_file = "actions_mass_storage_partition.bin"

print(f"\n[*] Sending Raw Memory Access requests to bypass mass storage...")
print(f"[*] Dumping to '{output_file}'...")

# Raw ADFU Memory Read Protocol Array (Bypasses USBS controllers completely)
def read_raw_memory_packet(address, length):
    cmd = bytearray(16)
    cmd[0] = 0x06       # Opcode 0x06: Raw SRAM/NOR Flash Address space access
    cmd[2] = (address >> 24) & 0xFF
    cmd[3] = (address >> 16) & 0xFF
    cmd[4] = (address >> 8) & 0xFF
    cmd[5] = address & 0xFF
    cmd[6] = (length >> 24) & 0xFF
    cmd[7] = (length >> 16) & 0xFF
    cmd[8] = (length >> 8) & 0xFF
    cmd[9] = length & 0xFF
    return cmd

bytes_dumped = 0
current_target_address = START_ADDRESS

with open(output_file, "wb") as f:
    while bytes_dumped < DUMP_SIZE:
        try:
            command_packet = read_raw_memory_packet(current_target_address, BLOCK_SIZE)
            ep_out.write(command_packet, timeout=2000)
            
            data = ep_in.read(BLOCK_SIZE, timeout=2000)
            f.write(data)
            
            bytes_dumped += len(data)
            current_target_address += len(data)
            
            percent = (bytes_dumped / DUMP_SIZE) * 100
            print(f"\rProgress: {percent:.1f}% [{bytes_dumped}/{DUMP_SIZE} Bytes Data Captured]", end="")
            
        except usb.core.USBError as e:
            print(f"\n[!] Memory pipeline stalled at address {hex(current_target_address)}. Error: {e}")
            break

if bytes_dumped > 0:
    print(f"\n\n[SUCCESS] Raw Core Dump Complete!")
    print(f"[+] Output file saved to '{output_file}'")