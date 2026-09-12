import os
import json

def audit(root_dir):
    results = []
    for dirpath, _, filenames in os.walk(root_dir):
        if '.git' in dirpath: continue
        for f in filenames:
            if not f.endswith(('.py', '.md')): continue
            path = os.path.join(dirpath, f)
            size = os.path.getsize(path)
            with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                lines = file.readlines()
                length = len(lines)
            rel_path = os.path.relpath(path, root_dir)
            results.append({"path": rel_path, "size": size, "lines": length})
    
    with open('AUDIT_DATA.json', 'w') as f:
        json.dump(results, f, indent=4)
    print(f"Audited {len(results)} files.")

audit('.')
