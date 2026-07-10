import os

target_file = "ota_V1.03.11.bin"

print(f"[*] Scanning {target_file} directly for XML configurations...")

if not os.path.exists(target_file):
    print(f"[!] Error: {target_file} not found in this folder.")
    exit(1)

with open(target_file, "rb") as f:
    raw_data = f.read()

# Locate the beginning of the XML sheet data block
start_marker = raw_data.find(b"<ota_fw_ver=")
if start_marker == -1:
    print("[!] Could not find the XML signature block inside the binary.")
    exit(1)

# Find the ending bracket of the XML string data layout
# SDFS xml definitions usually close out with a standard firmware tag block
end_marker = raw_data.find(b"</firmware>", start_marker)
if end_marker == -1:
    # Fallback if the closing tag is named differently, read a 4KB chunk from the start
    end_marker = start_marker + 4096

extracted_xml_bytes = raw_data[start_marker : end_marker + 11]

try:
    decoded_text = extracted_xml_bytes.decode("utf-8", errors="ignore")
    # Clean up formatting by breaking lines cleanly before every XML block element tag
    formatted_output = decoded_text.replace("<", "\n<")
    
    print("\n=================== UNMASKED XML MANIFEST ===================")
    print(formatted_output)
    print("=============================================================")
    
    # Let's save a clean physical copy so you have it in your workspace
    with open("direct_manifest_dump.xml", "w", encoding="utf-8") as out:
        out.write(formatted_output)
    print("[+] Saved a copy safely to: direct_manifest_dump.xml")

except Exception as e:
    print(f"[!] Extraction parsing failed: {e}")