"""
# ==============================================================================
# LABORATORY: PROJECT-BASED LEARNING (RELATIONAL DATABASE ENGINE)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# A junior developer needs to store 10,000 user profiles. They save them to a 
# giant JSON file. Every time they need to find User #9842, they execute 
# `json.load()`. Python loads the entire 50MB string into RAM, parses it into 
# a massive dictionary, and extracts the user. It takes 1.5 seconds. When 
# 1,000 concurrent users log in, the server violently runs out of RAM (OOM) 
# and crashes.
#
# A senior database architect understands "Storage Engines". They build a custom 
# Relational Database using mathematical Byte Offsets and an In-Memory Index. 
# When they need User #9842, they query the ultra-fast RAM Index, which returns 
# `Byte Offset: 140452`. The script opens the physical Hard Drive file in Binary 
# Mode, executes `file.seek(140452)`, and instantly extracts the exact 100 bytes 
# belonging to the user. It takes 0.0001 seconds, consuming practically zero RAM.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Disk-Based Storage architecture (bypassing RAM exhaustion).
# - Execute algorithmic Indexing (Primary Keys to Byte Offsets).
# - Implement CRUD operations (Create, Read, Update, Delete) via OS File Pointers.
#
# ==============================================================================
"""

import os
import json
import struct
from typing import Dict, Any, Optional

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. THE STORAGE ENGINE ARCHITECTURE
# ==============================================================================
class SimpleDatabase:
    """
    An algorithmic Database Engine.
    It mathematically decouples the RAM Index from the Hard Drive Storage.
    """
    def __init__(self, db_filepath: str):
        self.db_filepath = db_filepath
        
        # THE INDEX: This lives entirely in RAM for O(1) mathematical speed.
        # It maps the Primary Key (String) to the absolute Byte Offset (Integer)
        # indicating exactly where the data lives on the silicon of the Hard Drive!
        self.index: Dict[str, int] = {}
        
        # We mathematically boot up the database!
        self._initialize_database()

    def _initialize_database(self):
        """Creates the physical file if it doesn't exist, or mathematically rebuilds the Index."""
        if not os.path.exists(self.db_filepath):
            # Create an empty file
            open(self.db_filepath, 'wb').close()
            return
            
        print("  [BOOT] Existing database detected. Mathematically rebuilding the RAM Index...")
        # We must physically scan the file ONCE at boot to find where every record lives!
        with open(self.db_filepath, 'rb') as file:
            while True:
                current_offset = file.tell() # The absolute byte position on the Hard Drive!
                
                # 1. Read the size of the upcoming record (We packed it as a 4-byte integer)
                header = file.read(4)
                if not header:
                    break # End of File!
                    
                # We use `struct` to mathematically unpack the 4 raw binary bytes into a Python Integer
                record_size = struct.unpack('<I', header)[0]
                
                # 2. Read the actual JSON payload
                raw_payload = file.read(record_size)
                
                # 3. We decode the payload just to extract the Primary Key!
                record = json.loads(raw_payload.decode('utf-8'))
                
                # THE DELETION FLAG CHECK
                if not record.get('_deleted', False):
                    primary_key = record['id']
                    # We mathematically lock the Byte Offset into RAM!
                    self.index[primary_key] = current_offset
                    
    def insert(self, record_id: str, data: Dict[str, Any]):
        """
        O(1) Insertion.
        We always mathematically APPEND to the absolute end of the file.
        This prevents catastrophic OS-level data shifting.
        """
        if record_id in self.index:
            raise ValueError(f"Primary Key Violation: Record '{record_id}' already exists.")
            
        record = {'id': record_id, **data, '_deleted': False}
        payload_bytes = json.dumps(record).encode('utf-8')
        
        # We calculate the exact mathematical size of the payload
        payload_size = len(payload_bytes)
        
        # We pack the size into a strict 4-byte Little-Endian integer
        header = struct.pack('<I', payload_size)
        
        with open(self.db_filepath, 'ab') as file:
            # We ask the OS where the physical pointer is located (the end of the file)
            byte_offset = file.tell()
            
            # We write the 4-byte Header, then the actual Data
            file.write(header)
            file.write(payload_bytes)
            
            # We mathematically update the ultra-fast RAM Index!
            self.index[record_id] = byte_offset
            
    def read(self, record_id: str) -> Optional[Dict[str, Any]]:
        """
        O(1) Retrieval.
        This is the mathematical magic. We do NOT load the whole file into RAM!
        """
        if record_id not in self.index:
            return None
            
        byte_offset = self.index[record_id]
        
        with open(self.db_filepath, 'rb') as file:
            # THE MAGIC: We command the OS to instantly teleport the reading laser 
            # to the exact byte offset on the silicon platter!
            file.seek(byte_offset)
            
            header = file.read(4)
            record_size = struct.unpack('<I', header)[0]
            
            raw_payload = file.read(record_size)
            record = json.loads(raw_payload.decode('utf-8'))
            
            # Remove the internal database flags before returning to the user
            del record['_deleted']
            return record

    def delete(self, record_id: str):
        """
        O(1) Deletion (Tombstoning).
        We do NOT physically delete the bytes from the Hard Drive. 
        That would require rewriting the entire file! We just mark it as dead.
        """
        if record_id not in self.index:
            raise KeyError(f"Primary Key '{record_id}' not found.")
            
        byte_offset = self.index[record_id]
        
        with open(self.db_filepath, 'r+b') as file:
            file.seek(byte_offset)
            
            header = file.read(4)
            record_size = struct.unpack('<I', header)[0]
            raw_payload = file.read(record_size)
            
            record = json.loads(raw_payload.decode('utf-8'))
            # We mathematically mutate the deletion flag!
            record['_deleted'] = True
            
            new_payload_bytes = json.dumps(record).encode('utf-8')
            
            # Mathematical padding to ensure we don't overwrite the next record!
            new_payload_bytes = new_payload_bytes.ljust(record_size, b' ')
            
            # We write the tombstone back to the exact same spot on the Hard Drive!
            file.seek(byte_offset + 4)
            file.write(new_payload_bytes)
            
        # We instantly nuke the pointer from the RAM Index!
        del self.index[record_id]


# ==============================================================================
# 4. MATHEMATICAL PROOF (THE SIMULATION)
# ==============================================================================
def demonstrate_database():
    section_header("Project: Storage Engine Architecture")
    
    db_file = "lab_database.bin"
    if os.path.exists(db_file):
        os.remove(db_file)
        
    db = SimpleDatabase(db_file)
    
    print("  [PHASE 1: O(1) INSERTION]")
    db.insert("usr_01", {"name": "Alice", "role": "Admin", "level": 99})
    db.insert("usr_02", {"name": "Bob", "role": "User", "level": 12})
    db.insert("usr_03", {"name": "Charlie", "role": "User", "level": 5})
    
    print("    -> Database successfully populated.")
    print(f"    -> The RAM Index physically holds byte offsets: {db.index}")
    
    print("\n  [PHASE 2: O(1) DIRECT ACCESS RETRIEVAL]")
    print("    -> Requesting 'usr_02'...")
    # The database will NOT load Alice or Charlie into RAM! It teleports directly to Bob!
    record = db.read("usr_02")
    print(f"    -> [SUCCESS] Payload extracted: {record}")
    
    print("\n  [PHASE 3: O(1) TOMBSTONE DELETION]")
    print("    -> Executing DELETION on 'usr_02'...")
    db.delete("usr_02")
    
    print("    -> Attempting to read 'usr_02'...")
    deleted_record = db.read("usr_02")
    print(f"    -> Result: {deleted_record} (The RAM Index pointer was successfully annihilated!)")
    
    # Clean up the lab
    if os.path.exists(db_file):
        os.remove(db_file)
    print("\n  [TEARDOWN] Lab binary database cleanly removed.")


def run_all_labs():
    demonstrate_database()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why did we mathematically pack the Payload Size into a $4$-byte binary header using `struct.pack('<I', size)`? Why couldn't we just write the JSON string directly to the file?"
   Senior Answer: "File Pointer Navigation. A physical Hard Drive has no concept of where a JSON string begins or ends. If you just write `{data}{data}`, the reading laser has no idea when to stop reading. By writing a rigid $4$-byte binary header first, we mathematically guarantee that the first $4$ bytes of ANY record contain the exact integer length of the upcoming payload. The database reads exactly $4$ bytes, unpacks the integer (e.g., $105$), and then confidently commands the OS to read exactly $105$ bytes. This prevents the database from accidentally reading into the next record and catastrophically corrupting the JSON parser."

2. Interviewer: "When a user executes a `DELETE` command, why did we use 'Tombstoning' instead of physically erasing the bytes from the Hard Drive?"
   Senior Answer: "Mathematical $O(1)$ efficiency versus catastrophic $O(N)$ data shifting. If 'Bob' is located at byte offset $100$, and 'Charlie' is at offset $200$, physically deleting Bob would create a $100$-byte vacuum in the file. The OS would be forced to physically rewrite Charlie (and every single subsequent record in the database) $100$ bytes to the left to close the gap. In a $50$ GB database, a single deletion would trigger hours of disk thrashing. By 'Tombstoning' (flipping a boolean `_deleted = True`), we execute an instant $O(1)$ mutation. The dead bytes remain on disk, but the Database Engine mathematically ignores them. A separate 'Vacuuming' process is run during scheduled maintenance at 3:00 AM to rebuild the file and reclaim the dead space."

3. Interviewer: "Our database uses an 'Append-Only' architecture for insertions. What are the architectural benefits of always writing to the absolute end of the file?"
   Senior Answer: "Sequential Write Performance and Concurrency. Hard Drives (both HDD and SSD) are mathematically optimized for Sequential Writes. Seeking to a random middle location to insert data is violently slow (Random I/O). Appending to the end is blazing fast (Sequential I/O). Furthermore, if you are always appending, it is mathematically easier to prevent Write-Conflicts in a highly concurrent environment. A transaction simply requests an OS-level append lock, dumps its bytes at the tail end of the file, logs the offset, and releases the lock, forming the architectural foundation of a Write-Ahead Log (WAL) used by Postgres and SQLite."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Capstone Project (Database Engine) Completed.")
