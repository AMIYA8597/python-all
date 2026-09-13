import json

QUEUE_FILE = r"d:\work\python-all\WORK_QUEUE.json"

def mark_and_get_next(completed_files, count):
    with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
        queue = json.load(f)
        
    for cf in completed_files:
        path = next((p for p in queue if p.endswith(cf)), None)
        if path:
            queue[path] = 'VERIFIED'
            print(f"Marked VERIFIED: {cf}")
            
    batch = []
    for path, status in queue.items():
        if status == 'PENDING':
            batch.append(path)
            queue[path] = 'IN_PROGRESS'
            if len(batch) >= count:
                break
                
    with open(QUEUE_FILE, 'w', encoding='utf-8') as f:
        json.dump(queue, f, indent=2)
        
    print("NEXT BATCH:")
    print(json.dumps(batch, indent=2))

if __name__ == '__main__':
    completed = [
        r"04-Standard-Library-Reference.md",
        r"05-Modern-Python-Features.md",
        r"06-Performance-Optimization.md",
        r"01-variables-and-datatypes.py"
    ]
    mark_and_get_next(completed, 4)
