import os

# Pointing straight to your newly structured Docs folder layout
cache_folder = os.path.join("..", "Docs", "cache")

if not os.path.exists(cache_folder):
    # Fallback to look for a local execution or direct relative layout
    cache_folder = os.path.join("Docs", "cache")

if not os.path.exists(cache_folder):
    print(f"[!] Error: Cannot find the 'cache' directory structure.")
    print("Please verify that the phone's cache folder was copied into 'WatchProject/Docs/cache/'!")
    exit(1)

print(f"[*] Scanning cached directory structures for downloaded watch faces inside: {cache_folder}")
found_files = []

for root, dirs, files in os.walk(cache_folder):
    for file in files:
        full_path = os.path.join(root, file)
        try:
            file_size = os.path.getsize(full_path)
            # A watch face asset block (SDFS cluster) is typically between 200KB and 4MB
            if file_size > 200000:  # Files larger than 200KB
                found_files.append((full_path, file_size))
        except Exception:
            continue

if found_files:
    print(f"\n[+] Discovered {len(found_files)} potential graphic asset bundles in your phone's cache!")
    print("-" * 80)
    for path, size in found_files:
        print(f"  -> File: {path} | Size: {size / 1024:.2f} KB")
    print("-" * 80)
    print("[*] Next step: We will run our deep slicer on these targets to verify if they contain SDFS structures.")
else:
    print("[-] No large asset binaries found in the cache folder yet.")
    print("    If empty, double-check if your phone's 'diskcache' directory contains files without extensions!")