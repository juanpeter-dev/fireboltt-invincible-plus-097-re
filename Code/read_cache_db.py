import os
import sqlite3

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "Docs", "map_cache.db"))

print(f"[*] Extracting resource data maps from: {db_path}\n")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Inspect column names inside the 'resources' table
    cursor.execute("PRAGMA table_info(resources);")
    columns = cursor.fetchall()
    col_names = [col[1] for col in columns]
    print(f"[+] 'resources' Table Structure Columns: {col_names}\n")
    
    # 2. Extract the actual stored rows
    cursor.execute("SELECT * FROM resources LIMIT 20;")
    rows = cursor.fetchall()
    
    if not rows:
        print("[-] The 'resources' table is currently empty.")
    else:
        print(f"=== DUMPING FIRST {len(rows)} ROWS FROM RESOURCES ===")
        for index, row in enumerate(rows):
            print(f"\n[Row #{index + 1}]")
            for col_name, value in zip(col_names, row):
                # Make the output clean and highlight URLs or asset file pathways
                val_str = str(value)
                if "http" in val_str or ".bin" in val_str or ".png" in val_str:
                    print(f"  * {col_name} -> [ASSET HOOK] {val_str}")
                else:
                    print(f"  * {col_name} -> {val_str[:120]}")
                    
    conn.close()
except Exception as e:
    print(f"[!] Database extraction failure: {e}")