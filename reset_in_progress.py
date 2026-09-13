import json

QUEUE_FILE = r"d:\work\python-all\WORK_QUEUE.json"

with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
    queue = json.load(f)
    
count = 0
for path, status in queue.items():
    if status == 'IN_PROGRESS':
        queue[path] = 'PENDING'
        count += 1
        
with open(QUEUE_FILE, 'w', encoding='utf-8') as f:
    json.dump(queue, f, indent=2)
    
print(f"Reset {count} files from IN_PROGRESS back to PENDING.")
