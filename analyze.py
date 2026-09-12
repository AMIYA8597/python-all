import json
import os

root = r'd:\work\python-all'
with open('audit.json') as f:
    data = json.load(f)

# Filter for Python-DSA-AI-Master
master_files = [x for x in data if x['path'].startswith('/Python-DSA-AI-Master')]

sizes = [x['size'] for x in master_files]
print(f"Total files: {len(master_files)}")
print(f"Empty files (0 bytes): {len([x for x in master_files if x['size'] == 0])}")
print(f"Small files (< 1000 bytes): {len([x for x in master_files if x['size'] < 1000])}")
print(f"Medium files (1000-5000 bytes): {len([x for x in master_files if 1000 <= x['size'] < 5000])}")
print(f"Large files (> 5000 bytes): {len([x for x in master_files if x['size'] >= 5000])}")

# Let's check a small file and a large file to see quality
small_files = [x for x in master_files if 0 < x['size'] < 1000]
if small_files:
    print(f"\nExample small file: {small_files[0]['path']}")
    with open(root + small_files[0]['path'], 'r', encoding='utf-8') as f:
        print(f.read()[:500])
