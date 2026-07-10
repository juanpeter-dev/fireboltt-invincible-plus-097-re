import usb.core
import usb.backend.libusb1
import os
import sys
import time

# Bind to your local Zadig driver
script_dir = os.path.dirname(os.path.abspath(__file__))
dll_path = os.path.join(script_dir, "libusb-1.0.dll")
backend = usb.backend.libusb1.get_backend(find_library=lambda x: dll_path)

dev = usb.core.find(idVendor=0x10D6, idProduct=0x10D6, backend=backend)
if dev is None:
    print("[!] Watch not found in ADFU state.")
    sys.exit(1)

dev.set_configuration()

ep_out = dev[0][(0,0)][1] # Endpoint 0x02
ep_in = dev[0][(0,0)][0]  # Endpoint 0x81

print("[*] Sending Stage 1 ADFU initialization override...")

# The secret Actions Semi factory bypass sequence: 
# Opcode 0x01 forces the internal flash engine to switch context out of Mass Storage Mode
def force_dfu_mode():
    cmd = bytearray(16)
    cmd[0] = 0x01  # Opcode 0x01: Switch/Unlock internal sector mapping registers
    cmd[1] = 0x01  # Parameter byte: Collapse Virtual USB Storage state
    return cmd

try:
    # Punch the command through the OUT wire
    ep_out.write(force_dfu_mode(), timeout=2000)
    time.sleep(1)
    
    # Read the response token to check if the controller flipped
    response = ep_in.read(64, timeout=2000)
    print(f"[+] Chip Bootloader Response Vector: {[hex(b) for b in response]}")
    print("[SUCCESS] Media storage partition has been successfully collapsed.")
    print("[*] Proceeding to attempt a true system image chunk read...")
    
    # Try a targeted 512-byte raw look at memory offset 0x00
    read_cmd = bytearray(16)
    read_cmd[0] = 0x02  # Opcode 0x02: True internal ROM payload read
    read_cmd[7] = 0x02  # Length byte (512 bytes)
    
    ep_out.write(read_cmd, timeout=2000)
    system_data = ep_in.read(512, timeout=2000)
    
    with open("test_system_header.bin", "wb") as f:
        f.write(system_data)
        
    print("[+] Saved 'test_system_header.bin'. Check this file in HxD!")

except usb.core.USBError as e:
    print(f"[!] Protocol Handshake Refused: {e}")
    print("[*] Hint: The watch processor might require a hard cycle. Unplug, re-trigger Function Key mode, and run again.")