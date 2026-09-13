import json

QUEUE_FILE = r"d:\work\python-all\WORK_QUEUE.json"

def get_next(count):
    with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
        queue = json.load(f)
            
    batch = []
    for path, status in queue.items():
        if status == 'PENDING':
            batch.append(path)
            queue[path] = 'IN_PROGRESS'
            if len(batch) >= count:
                break
                
    with open(QUEUE_FILE, 'w', encoding='utf-8') as f:
        json.dump(queue, f, indent=2)
        
    print(json.dumps(batch, indent=2))

if __name__ == '__main__':
    get_next(1)
