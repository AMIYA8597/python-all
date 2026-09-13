import os
import json

root = r"d:\work\python-all\Python-DSA-AI-Master"
artifact_dir = r"C:\Users\USER\.gemini\antigravity\brain\a4879de9-bbd8-4bb9-9727-f611787dc42f"
os.makedirs(artifact_dir, exist_ok=True)

audit_results = []
status_counts = {}

def get_status(content, size):
    lower_content = content.lower()
    if size == 0:
        return "EMPTY"
    if "todo" in lower_content or "coming soon" in lower_content or "tbd" in lower_content:
        return "PLACEHOLDER"
    if size < 2000:
        return "SUPERFICIAL"
    if size < 5000:
        return "PARTIAL"
    if size < 8000:
        return "NEEDS-DEEPENING"
    return "GOOD"

for dirpath, dirnames, filenames in os.walk(root):
    for filename in filenames:
        if filename.endswith(".py") or filename.endswith(".md"):
            # skip some known non-content files
            if filename in ["MASTER_AUDIT.json", "BATCH_STATE.json", "FINAL_MANIFEST.json", "AUDIT-REPORT.md", "COMPLETION-REPORT.md", "JOB-READINESS-MATRIX.md", "KNOWLEDGE-MAP.md", "LEARNING-SYSTEM.md", "MASTER-CAPABILITY-TEST.md", "MASTER-ROADMAP.md", "PREREQUISITES-MAP.md", "QUALITY-AUDIT.md"]:
                continue
            filepath = os.path.join(dirpath, filename)
            try:
                size = os.path.getsize(filepath)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                status = get_status(content, size)
                rel_path = os.path.relpath(filepath, root)
                audit_results.append((rel_path, status, size))
                status_counts[status] = status_counts.get(status, 0) + 1
            except Exception as e:
                pass

audit_file = os.path.join(artifact_dir, "repository_audit.md")
with open(audit_file, "w", encoding="utf-8") as f:
    f.write("# Repository Audit\n\n")
    f.write("## Summary\n")
    for stat, count in sorted(status_counts.items()):
        f.write(f"- **{stat}**: {count} files\n")
    
    f.write("\n## File Details\n")
    # Group by directory
    grouped = {}
    for r, s, size in audit_results:
        d = os.path.dirname(r)
        if d not in grouped:
            grouped[d] = []
        grouped[d].append((os.path.basename(r), s, size))
    
    for d, files in sorted(grouped.items()):
        if d == "":
            d = "/"
        f.write(f"\n### {d}\n")
        f.write("| File | Status | Size (Bytes) |\n")
        f.write("|---|---|---|\n")
        for f_name, stat, size in sorted(files):
            f.write(f"| {f_name} | {stat} | {size} |\n")

print("Audit complete, written to:", audit_file)
