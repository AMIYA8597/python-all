import json
import sys

QUEUE_FILE = r"d:\work\python-all\WORK_QUEUE.json"

def mark_verified(target):
    with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
        queue = json.load(f)
        
    path = next((p for p in queue if p.endswith(target)), None)
    if path:
        queue[path] = 'VERIFIED'
        with open(QUEUE_FILE, 'w', encoding='utf-8') as f:
            json.dump(queue, f, indent=2)
        print(f"Marked VERIFIED: {target}")
    else:
        print(f"Target not found: {target}")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        mark_verified(sys.argv[1])
    else:
        print("Please provide a file name.")
