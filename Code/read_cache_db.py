import os
import sqlite3

db_path = "map_cache.db"

if not os.path.exists(db_path):
    print(f"[!] Error: Missing '{db_path}' in your current laptop directory.")
    print("Please copy it over from the phone's diskcache folder first!")
    exit(1)

print(f"[*] Opening and scanning watch local cache map: {db_path}")
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Extract the names of all internal data storage tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"[+] Found {len(tables)} active data storage maps inside the cache database:")
    for t in tables:
        print(f"  -> Table Name: {t[0]}")
        
    for t in tables:
        table_name = t[0]
        print(f"\n=== SHOWING DATA INSIDE TABLE: {table_name} ===")
        try:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 10;")
            rows = cursor.fetchall()
            for r in rows:
                # Convert rows to string and look for asset hooks
                row_str = str(r)
                if "http" in row_str or ".bin" in row_str or "D900" in row_str:
                    print(f"  [ASSET HOOK] -> {row_str}")
                else:
                    print(f"  -> {row_str[:120]}") # Truncate long rows to keep it clean
        except Exception as table_err:
            print(f"  [!] Could not query table rows: {table_err}")
            
    conn.close()
except Exception as e:
    print(f"[!] Database access error: {e}")