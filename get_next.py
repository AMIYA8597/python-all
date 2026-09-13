import json
import sys

QUEUE_FILE = r"d:\work\python-all\work_queue.json"

def get_next_batch(batch_size=1):
    try:
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            queue = json.load(f)
    except FileNotFoundError:
        print("QUEUE_FILE_NOT_FOUND")
        return
        
    pending = queue.get("pending", [])
    if not pending:
        print("QUEUE_EMPTY")
        return
        
    # Take the first 'batch_size' items
    items = pending[:batch_size]
    queue["pending"] = pending[batch_size:]
    
    if queue.get("in_progress") is None:
        queue["in_progress"] = []
    
    queue["in_progress"].extend(items)
    
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2)
        
    print(json.dumps(items, indent=2))

if __name__ == "__main__":
    get_next_batch(1)
