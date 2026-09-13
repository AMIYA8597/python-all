import json
import sys

QUEUE_FILE = r"d:\work\python-all\work_queue.json"

def mark_completed(path):
    try:
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            queue = json.load(f)
    except FileNotFoundError:
        return
        
    in_progress = queue.get("in_progress") or []
    
    # Find item
    item = next((x for x in in_progress if x["path"] == path), None)
    if item:
        in_progress.remove(item)
        queue["completed"].append(item)
        
    queue["in_progress"] = in_progress
    
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2)
        
    print(f"Marked {path} as completed.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        mark_completed(sys.argv[1])
