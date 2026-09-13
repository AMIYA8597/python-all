"""
03 - Database Design in System Design
=====================================

What is Database Design?
Database design is the process of producing a detailed data model of a database. 
It involves organizing data according to a database model (Relational, NoSQL, etc.) 
and ensuring that the system is optimized for its primary workload (Read-heavy vs Write-heavy).

Why it exists and Industry Use Cases:
- Data must be persisted reliably across application restarts and failures.
- Databases provide structured ways to query, filter, and aggregate data efficiently.
- Use cases: E-commerce inventory (Relational/ACID), Logging systems (NoSQL/Append-only), 
  Social media feeds (Graph DB or Columnar).

Key Concepts:
1. Normalization vs. Denormalization:
   - Normalization: Dividing tables to reduce data redundancy. Good for write-heavy workloads.
   - Denormalization: Adding redundant data to speed up complex queries. Good for read-heavy workloads.
2. ACID Properties (Relational): Atomicity, Consistency, Isolation, Durability.
3. Sharding: Partitioning a database across multiple machines to scale horizontally.
4. Indexing: Creating data structures (like B-Trees or Hash Maps) to speed up data retrieval 
   at the cost of slower writes and extra storage.

Learning Objectives:
1. Understand the trade-offs between different database operations.
2. Implement a mock in-memory Key-Value store with secondary indexing.
3. Implement basic Transaction support (Commit and Rollback) demonstrating Atomicity.
"""

from typing import Dict, List, Any, Optional, Set

# ============================================================================
# Basic Concept: Simple In-Memory DB
# ============================================================================
class SimpleDatabase:
    def __init__(self):
        self.data: Dict[str, Any] = {}
        
    def write(self, key: str, value: Any) -> None:
        self.data[key] = value
        
    def read(self, key: str) -> Optional[Any]:
        return self.data.get(key)

# ============================================================================
# Professional Implementation: Key-Value Store with Indexing and Transactions
# ============================================================================
class Record:
    def __init__(self, id: str, attributes: Dict[str, Any]):
        self.id = id
        self.attributes = attributes

class TransactionDB:
    """
    An in-memory Key-Value database that supports:
    - Secondary Indexing (for fast querying by attributes)
    - Transactions (Begin, Commit, Rollback) for Atomicity.
    """
    def __init__(self):
        # Primary storage: Key -> Record
        self._store: Dict[str, Record] = {}
        
        # Secondary index: Attribute Name -> (Attribute Value -> Set of IDs)
        # E.g., 'status' -> {'active': {'id1', 'id2'}, 'inactive': {'id3'}}
        self._indexes: Dict[str, Dict[Any, Set[str]]] = {}
        
        # Transaction state
        self._in_transaction = False
        # Snapshot of the store before transaction starts
        self._store_snapshot: Dict[str, Record] = {}
        # Snapshot of indexes before transaction starts
        self._indexes_snapshot: Dict[str, Dict[Any, Set[str]]] = {}

    def _copy_indexes(self) -> Dict[str, Dict[Any, Set[str]]]:
        """Deep copy of indexes for transaction snapshot."""
        copied = {}
        for attr, val_map in self._indexes.items():
            copied[attr] = {val: ids.copy() for val, ids in val_map.items()}
        return copied

    def begin_transaction(self) -> None:
        """Start a new transaction."""
        if self._in_transaction:
            raise Exception("Transaction already in progress")
        
        self._in_transaction = True
        # Create snapshots
        self._store_snapshot = {k: Record(v.id, v.attributes.copy()) for k, v in self._store.items()}
        self._indexes_snapshot = self._copy_indexes()

    def commit(self) -> None:
        """Commit the current transaction."""
        if not self._in_transaction:
            raise Exception("No active transaction")
        
        self._in_transaction = False
        self._store_snapshot.clear()
        self._indexes_snapshot.clear()

    def rollback(self) -> None:
        """Rollback the current transaction to the snapshot state."""
        if not self._in_transaction:
            raise Exception("No active transaction")
        
        self._in_transaction = False
        self._store = self._store_snapshot
        self._indexes = self._indexes_snapshot
        self._store_snapshot = {}
        self._indexes_snapshot = {}

    def create_index(self, attribute: str) -> None:
        """Create an index on a specific attribute."""
        if attribute not in self._indexes:
            self._indexes[attribute] = {}
            # Populate index with existing data
            for record_id, record in self._store.items():
                if attribute in record.attributes:
                    val = record.attributes[attribute]
                    if val not in self._indexes[attribute]:
                        self._indexes[attribute][val] = set()
                    self._indexes[attribute][val].add(record_id)

    def insert(self, record_id: str, attributes: Dict[str, Any]) -> None:
        """Insert or update a record."""
        # Handle index updates for an existing record
        if record_id in self._store:
            old_record = self._store[record_id]
            for attr, val in old_record.attributes.items():
                if attr in self._indexes:
                    self._indexes[attr][val].discard(record_id)

        new_record = Record(record_id, attributes)
        self._store[record_id] = new_record

        # Handle index updates for the new record
        for attr, val in attributes.items():
            if attr in self._indexes:
                if val not in self._indexes[attr]:
                    self._indexes[attr][val] = set()
                self._indexes[attr][val].add(record_id)

    def find_by_id(self, record_id: str) -> Optional[Record]:
        """O(1) lookup by primary key."""
        return self._store.get(record_id)

    def find_by_attribute(self, attribute: str, value: Any) -> List[Record]:
        """Lookup records using a secondary index if available, else O(N) scan."""
        if attribute in self._indexes:
            # O(1) indexed lookup
            record_ids = self._indexes[attribute].get(value, set())
            return [self._store[r_id] for r_id in record_ids]
        else:
            # O(N) full table scan
            result = []
            for record in self._store.values():
                if record.attributes.get(attribute) == value:
                    result.append(record)
            return result


# ============================================================================
# Advanced Concepts & Interview Focus
# ============================================================================
"""
Common Interview Questions:
1. What is the CAP Theorem?
   Answer: It states a distributed database can only guarantee two out of three properties: 
   Consistency, Availability, and Partition Tolerance. In network partitions (which are inevitable), 
   we must choose between C and A.

2. Why shouldn't you index every column?
   Answer: Indexes consume extra storage space and memory. More importantly, every write 
   (Insert/Update/Delete) requires updating the indexes, which slows down write performance.

3. How does this mock database implement Atomicity?
   Answer: By keeping a snapshot of the database state (store and indexes) before a transaction begins. 
   If an error occurs or rollback is called, the state is reverted entirely to the snapshot.

Complexity Analysis:
- Indexed Lookup: O(1) time complexity (using hash map index).
- Non-Indexed Lookup (Table Scan): O(N) time complexity, where N is the number of records.
- Insert/Update: O(I) time complexity, where I is the number of active indexes.

Security/Performance Considerations:
- Isolation levels: Real DBs manage concurrency through locking or MVCC (Multi-Version Concurrency Control) 
  to prevent dirty reads or phantom reads. This mock DB lacks concurrency control (Thread Safety).
"""

# ============================================================================
# Tests / Example Usage
# ============================================================================
def test_database() -> None:
    print("Testing TransactionDB...")
    db = TransactionDB()
    
    # Create an index on 'status' before inserting
    db.create_index("status")
    
    db.insert("u1", {"name": "Alice", "status": "active", "age": 28})
    db.insert("u2", {"name": "Bob", "status": "inactive", "age": 34})
    db.insert("u3", {"name": "Charlie", "status": "active", "age": 22})
    
    # Test Index Lookup
    active_users = db.find_by_attribute("status", "active")
    assert len(active_users) == 2, "Should find 2 active users"
    
    # Test Table Scan
    old_users = db.find_by_attribute("age", 34)
    assert len(old_users) == 1, "Should find 1 user aged 34"
    assert old_users[0].attributes["name"] == "Bob"
    
    # Test Transactions
    db.begin_transaction()
    db.insert("u4", {"name": "Dave", "status": "active"})
    assert db.find_by_id("u4") is not None, "Dave should be in DB during transaction"
    
    # Whoops, mistake made, rolling back
    db.rollback()
    assert db.find_by_id("u4") is None, "Dave should NOT be in DB after rollback"
    
    # Successful transaction
    db.begin_transaction()
    db.insert("u5", {"name": "Eve", "status": "inactive"})
    db.commit()
    assert db.find_by_id("u5") is not None, "Eve should be in DB after commit"

    print("All TransactionDB tests passed!\\n")

if __name__ == "__main__":
    test_database()
