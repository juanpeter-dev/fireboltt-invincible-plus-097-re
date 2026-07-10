import os

manifest_path = os.path.join("extracted_ota", "ota.xml")

print(f"[*] Formatting XML manifest document: {manifest_path}\n")

if not os.path.exists(manifest_path):
    print(f"[!] Error: Missing {manifest_path}")
    exit(1)

with open(manifest_path, "r", encoding="utf-8", errors="ignore") as f:
    raw_xml = f.read()

# Clean up formatting by inserting a clean line break before every opening tag XML bracket
formatted_xml = raw_xml.replace("<", "\n<")

print("=================== OFFICIAL FIRMWARE STRUCTURE ===================")
print(formatted_xml)
print("====================================================================")

# Let's save the clean version as a readable text file for your notes
with open(os.path.join("extracted_ota", "readable_manifest.xml"), "w", encoding="utf-8") as out:
    out.write(formatted_xml)