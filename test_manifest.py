import os, json
root = 'd:/work/python-all/Python-DSA-AI-Master'
manifest_path = os.path.join(root, 'FINAL_MANIFEST.json')
if os.path.exists(manifest_path):
    with open(manifest_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f'Total in manifest: {len(data)}')
    for item in data[:5]:
        p = os.path.join(root, item['PATH'])
        if os.path.exists(p):
            print(f"Exists: {item['PATH']} - size: {os.path.getsize(p)}")
        else:
            print(f"Missing: {item['PATH']}")
