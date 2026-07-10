import os

target_file = "ota_V1.03.11.bin"

if not os.path.exists(target_file):
    print(f"[!] Error: Missing '{target_file}' in this directory.")
    exit(1)

# Exact parameters unmasked from your index analysis
xml_offset = 0x400
xml_size = 815

print(f"[*] Extracting true XML text block from offset {hex(xml_offset)} ({xml_size} bytes)...")

with open(target_file, "rb") as f:
    f.seek(xml_offset)
    raw_xml_bytes = f.read(xml_size)

try:
    # Decode the raw data stream into human-readable text
    decoded_xml = raw_xml_bytes.decode("utf-8", errors="ignore")
    
    # Insert clean line breaks before opening brackets to make it readable
    formatted_xml = decoded_xml.replace("<", "\n<")
    
    print("\n=================== UNMASKED FIRMWARE MAP ===================")
    print(formatted_xml)
    print("=============================================================")
    
    # Save a clean copy right in your workspace
    output_name = "true_ota_manifest.xml"
    with open(output_name, "w", encoding="utf-8") as out:
        out.write(formatted_xml)
    print(f"[SUCCESS] Clean blueprint saved to: {output_name}")

except Exception as e:
    print(f"[!] Decoding error encountered: {e}")