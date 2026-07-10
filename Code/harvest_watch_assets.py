import json
import urllib.request

# The official host destination pulled straight from your Wireshark handshake map
target_url = "http://dail.cynet2open.com:10090/api/clockDial/page.html?page=1&limit=50&typeId="

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-J701F) CyFit/1.2.3'
}

print(f"[*] Querying factory backend asset vault: {target_url}")

try:
    req = urllib.request.Request(target_url, headers=headers)
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        
    raw_json = json.loads(html)
    
    # Check if the server responded with a valid data matrix block
    if "data" in raw_json or "rows" in raw_json:
        dial_list = raw_json.get("data", raw_json.get("rows", []))
        print(f"[+] Server Handshake Success! Found {len(dial_list)} available base packages.\n")
        
        print("=== FACTORY WATCH FACE ASSET DIRECTORY ===")
        print(f"{'ID':<6} | {'Face Name':<20} | {'Download Target URL'}")
        print("-" * 80)
        
        for dial in dial_list:
            dial_id = dial.get("id", "N/A")
            dial_name = dial.get("name", "Unnamed_Face").strip()
            
            # Extract common asset naming variations from the Actions semi engine
            file_link = dial.get("fileUrl", dial.get("downloadUrl", dial.get("filePath", "None")))
            
            if file_link != "None":
                print(f"{dial_id:<6} | {dial_name[:20]:<20} | {file_link}")
                
    else:
        print("[-] Unexpected server response map format. Raw data loop dumped below:")
        print(html[:500])
        
except Exception as e:
    print(f"[!] Target server link fetch failure: {e}")
    print("[*] Double check if your laptop has active internet connectivity!")