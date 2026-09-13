import json

QUEUE_FILE = r"d:\work\python-all\WORK_QUEUE.json"

def get_next():
    with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
        queue = json.load(f)
        
    for path, status in queue.items():
        if status == 'PENDING':
            queue[path] = 'IN_PROGRESS'
            with open(QUEUE_FILE, 'w', encoding='utf-8') as f:
                json.dump(queue, f, indent=2)
            print(path)
            return
            
    print("DONE")

if __name__ == '__main__':
    get_next()
