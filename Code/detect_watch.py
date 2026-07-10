import usb.core
import usb.backend.libusb1
import time
import os
import ctypes

# Get absolute path to the local DLL file
script_dir = os.path.dirname(os.path.abspath(__file__))
dll_path = os.path.join(script_dir, "libusb-1.0.dll")

print(f"[INFO] Targeted path: {dll_path}")

# Force Windows to load the DLL into memory at the OS level first
try:
    windows_dll_handle = ctypes.CDLL(dll_path)
    print("[SUCCESS] Windows core has successfully loaded the DLL into memory!")
except Exception as e:
    print(f"[CRITICAL ERROR] Windows rejected the DLL file: {e}")
    print("Double check that you copied the file from the 'VS2015-x64' folder!")

# Explicitly create the PyUSB backend pointer using that specific file
backend = usb.backend.libusb1.get_backend(find_library=lambda x: dll_path)

print("\nSearching for Actions Semi Watch in ADFU mode (10D6:10D6)...")

while True:
    # Pass the backend directly into the find function
    dev = usb.core.find(idVendor=0x10D6, idProduct=0x10D6, backend=backend)
    if dev is not None:
        print("\n[SUCCESS] Watch Intercepted!")
        print("-" * 50)
        print(dev)
        print("-" * 50)
        break
    time.sleep(0.5)