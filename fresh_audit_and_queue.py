import os
import json
import re

ROOT = r"d:\work\python-all\Python-DSA-AI-Master"
QUEUE_FILE = r"d:\work\python-all\work_queue.json"
MANIFEST_FILE = r"d:\work\python-all\audit_manifest.json"

def analyze_file(filepath, rel_path):
    size = os.path.getsize(filepath)
    if size == 0:
        return {"status": "EMPTY", "action": "FILL", "reason": "Size is 0"}
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return {"status": "ERROR", "action": "FIX_ENCODING", "reason": str(e)}

    lower_content = content.lower()
    
    # Check for placeholders
    if re.search(r'\b(todo:|tbd:|coming soon|to be added|implement here)\b', lower_content):
        return {"status": "PLACEHOLDER", "action": "EXPAND", "reason": "Contains placeholder text"}
        
    # Check for shallowness
    if filepath.endswith(".md"):
        if size < 2000:
            return {"status": "SHALLOW", "action": "EXPAND", "reason": f"Markdown file is too short ({size} bytes)"}
    elif filepath.endswith(".py"):
        if size < 500:
            return {"status": "SHALLOW", "action": "EXPAND", "reason": f"Python file is too short ({size} bytes)"}
            
    # Check for completeness based on user's contract
    if "prerequisites" not in lower_content and filepath.endswith(".md") and size < 5000:
        return {"status": "INCOMPLETE_STRUCTURE", "action": "EXPAND", "reason": "Missing prerequisites section"}
        
    return {"status": "GOOD", "action": "NONE", "reason": "Appears sufficient"}

def build_queue():
    manifest = {}
    queue = []
    
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # Skip some meta directories if any
        if ".git" in dirpath:
            continue
            
        rel_dir = os.path.relpath(dirpath, ROOT)
        if rel_dir == ".":
            rel_dir = ""
            
        # Check if folder is completely empty
        if not dirnames and not filenames:
            item = {
                "type": "DIRECTORY",
                "path": rel_dir,
                "status": "EMPTY",
                "action": "BUILD_CONTENT",
                "reason": "Directory is empty"
            }
            manifest[rel_dir] = item
            queue.append(item)
            continue
            
        for filename in filenames:
            if not (filename.endswith(".py") or filename.endswith(".md")):
                continue
            
            # Skip pure metadata files
            if filename in ["AUDIT-REPORT.md", "COMPLETION-REPORT.md", "FINAL_MANIFEST.json", "AUDIT_DATA.json", "MASTER_AUDIT.json", "BATCH_STATE.json"]:
                continue
                
            filepath = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(filepath, ROOT)
            
            analysis = analyze_file(filepath, rel_path)
            
            item = {
                "type": "FILE",
                "path": rel_path,
                "status": analysis["status"],
                "action": analysis["action"],
                "reason": analysis["reason"],
                "size": os.path.getsize(filepath)
            }
            
            manifest[rel_path] = item
            
            if item["action"] != "NONE":
                queue.append(item)

    # Sort queue: files first, then directories. Smallest files first to get them out of the way, or largest to build deep?
    # Let's sort by directory to group related items, and files before dirs
    queue.sort(key=lambda x: (x["path"]))

    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        
    # Filter queue to only those needing action
    active_queue = [q for q in queue if q["action"] != "NONE"]
    
    queue_state = {
        "pending": active_queue,
        "completed": [],
        "blocked": [],
        "in_progress": None
    }
    
    with open(QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue_state, f, indent=2)
        
    print(f"Audit complete. Found {len(manifest)} items.")
    print(f"Items needing action: {len(active_queue)}")
    
if __name__ == "__main__":
    build_queue()
