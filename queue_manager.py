import json
import os
import re

AUDIT_FILE = r"d:\work\python-all\CONTENT_DEPTH_AUDIT.json"
QUEUE_FILE = r"d:\work\python-all\WORK_QUEUE.json"

def init_queue():
    if not os.path.exists(AUDIT_FILE):
        print("Audit file not found.")
        return
        
    with open(AUDIT_FILE, 'r', encoding='utf-8') as f:
        audit_data = json.load(f)
        
    # Reset queue
    queue = {}
    
    added = 0
    pattern = re.compile(r"\\(?:[0-7][0-9]-.*)\\(?:.*\.md|.*\.py)$")
    
    for item in audit_data:
        path = item['path']
        if pattern.search(path):
            # Only include actual curriculum files, not root scripts
            if item['status'] in ['EMPTY', 'SHALLOW', 'MICRO', 'BASIC', 'INCOMPLETE', 'NORMAL']:
                queue[path] = 'PENDING'
                added += 1
                
    with open(QUEUE_FILE, 'w', encoding='utf-8') as f:
        json.dump(queue, f, indent=2)
        
    print(f"Queue re-initialized. {len(queue)} total items.")

def get_next_batch(batch_size=3):
    if not os.path.exists(QUEUE_FILE):
        print("[]")
        return
        
    with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
        queue = json.load(f)
        
    batch = []
    for path, status in queue.items():
        if status == 'PENDING':
            batch.append(path)
            if len(batch) >= batch_size:
                break
                
    for b in batch:
        queue[b] = 'IN_PROGRESS'
        
    with open(QUEUE_FILE, 'w', encoding='utf-8') as f:
        json.dump(queue, f, indent=2)
        
    print(json.dumps(batch))

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'get':
        size = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        get_next_batch(size)
    else:
        init_queue()
