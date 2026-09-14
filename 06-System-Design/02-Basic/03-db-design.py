"""
# ==============================================================================
# LABORATORY: SYSTEM DESIGN (DATABASE ARCHITECTURE)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# When designing a global system, the Web Servers (Node, Django) are easy to 
# horizontally scale. You just turn on 10,000 cheap Linux boxes.
#
# But the Database is the ultimate bottleneck. It holds the State of the universe.
# You cannot easily run 10,000 instances of a MySQL database because if User A 
# writes to Instance 1, how do the other 9,999 instances instantly know about it?
#
# To scale a Database, we must use complex architectural patterns:
# 1. Master-Slave Replication: Separates Writes (heavy locks) from Reads. 
#    All Writes go to the Master. All Reads hit the Slaves.
# 2. Database Sharding: If a table has 10 Billion rows, it mathematically 
#    surpasses the physical limits of a single hard drive's B-Tree indexing. 
#    We must violently slice the table into 10 smaller tables, spreading them 
#    across 10 independent servers.
# 3. SQL vs NoSQL (ACID vs BASE): Relational DBs guarantee perfect consistency 
#    (ACID) but struggle to scale horizontally. NoSQL DBs (Cassandra/Dynamo) 
#    sacrifice consistency (BASE) to achieve mathematically infinite horizontal scale.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the architecture of Master-Slave Replication.
# - Master Horizontal Database Sharding (Algorithmic Routing).
# - Understand ACID properties vs BASE properties.
#
# ==============================================================================
"""

import hashlib

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. MASTER-SLAVE REPLICATION (READ HEAVY WORKLOADS)
# ==============================================================================
class DatabaseInstance:
    def __init__(self, name: str):
        self.name = name
        self.data = {}
        
    def execute_write(self, key: str, value: str) -> None:
        self.data[key] = value
        
    def execute_read(self, key: str) -> str:
        return self.data.get(key, "Null")

class ReplicationCluster:
    """
    Most applications have a 95% Read to 5% Write ratio (e.g., Twitter).
    A single Master handles the 5% Writes.
    Multiple Slaves handle the 95% Reads, scaling horizontally perfectly!
    """
    def __init__(self):
        self.master = DatabaseInstance("Master-DB")
        self.slaves = [
            DatabaseInstance("Slave-1"),
            DatabaseInstance("Slave-2"),
            DatabaseInstance("Slave-3")
        ]
        self.slave_index = 0

    def write_data(self, key: str, value: str) -> str:
        """Writes ONLY go to the Master."""
        print(f"\n[CLIENT WRITE] Key: {key}")
        print(f"[{self.master.name}] Acquired Write Lock. Updating Disk...")
        self.master.execute_write(key, value)
        
        # Asynchronous Replication (Simulated)
        print(f"[REPLICATION PROCESS] Master broadcasting replication log to Slaves...")
        for slave in self.slaves:
            slave.execute_write(key, value)
            
        return "Write Successful"

    def read_data(self, key: str) -> str:
        """Reads ONLY go to the Slaves, routed via Round-Robin Load Balancing."""
        target_slave = self.slaves[self.slave_index]
        self.slave_index = (self.slave_index + 1) % len(self.slaves)
        
        print(f"\n[CLIENT READ] Key: {key}")
        print(f"[{target_slave.name}] Processing Read Query...")
        return target_slave.execute_read(key)

def demonstrate_replication():
    section_header("Master-Slave Replication")
    cluster = ReplicationCluster()
    
    cluster.write_data("user_77", "Alice Profile")
    
    # 3 massive concurrent reads hit the system. They are perfectly distributed!
    print(f"Result: {cluster.read_data('user_77')}")
    print(f"Result: {cluster.read_data('user_77')}")
    print(f"Result: {cluster.read_data('user_77')}")


# ==============================================================================
# 4. DATABASE SHARDING (HORIZONTAL PARTITIONING)
# ==============================================================================
class ShardedDatabase:
    """
    If a table has 1 Trillion rows, a single Master-Slave cluster will crash.
    We must Shard (physically divide) the table across N independent clusters!
    """
    def __init__(self, num_shards: int):
        self.num_shards = num_shards
        self.shards = [DatabaseInstance(f"Shard-{i}") for i in range(num_shards)]

    def _get_shard_index(self, user_id: str) -> int:
        """
        ALGORITHMIC ROUTING (Modulo Hashing)
        We convert the user_id into a cryptographic hash, turn it into an integer, 
        and modulo it by the number of shards. This guarantees that "user_123" 
        will ALWAYS mathematically route to the exact same physical Shard!
        """
        hash_val = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
        return hash_val % self.num_shards

    def insert_user(self, user_id: str, data: str) -> None:
        shard_idx = self._get_shard_index(user_id)
        target_shard = self.shards[shard_idx]
        
        print(f"[SHARD ROUTER] user: {user_id} -> Mathematically mapped to {target_shard.name}")
        target_shard.execute_write(user_id, data)

    def get_user(self, user_id: str) -> str:
        shard_idx = self._get_shard_index(user_id)
        target_shard = self.shards[shard_idx]
        return target_shard.execute_read(user_id)

def demonstrate_sharding():
    section_header("Database Sharding (Hash Routing)")
    
    sharded_db = ShardedDatabase(num_shards=4)
    print("Database shattered into 4 independent Physical Shards.")
    print("Writing 5 users. The Hash Router will mathematically distribute them!")
    
    users = ["user_101", "user_202", "user_303", "user_404", "user_505"]
    for u in users:
        sharded_db.insert_user(u, f"{u}_data")
        
    print("\nThe 1 Trillion row table is now physically divided by 4, ")
    print("restoring the $O(\\log N)$ B-Tree indexing speed on each machine!")


def run_all_labs():
    demonstrate_replication()
    demonstrate_sharding()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. In Master-Slave Replication, what happens if the Master dies? What happens to the Slaves?
   Answer: If the Master dies, the entire system loses the ability to perform Writes! (e.g., users can view their profile, but cannot post new tweets). However, the system maintains Availability for Reads because the Slaves are still running. To recover, a distributed consensus algorithm (like ZooKeeper or Raft) will automatically detect the dead Master, hold an "election" among the surviving Slaves, and promote one of the Slaves to become the new Master. The DNS/Load Balancer is then re-routed to point Write traffic to the new Master.

2. In Database Sharding using Modulo Hashing (`hash(id) % N`), what is the catastrophic flaw if you need to add a new server (change $N$ from 4 to 5)?
   Answer: "The Resharding Nightmare". If $N=4$, `hash("user_A") = 10`. $10 \pmod 4 = 2$. User A lives on Shard 2. If you add a server, $N$ becomes $5$. $10 \pmod 5 = 0$. Suddenly, the routing algorithm points to Shard 0 for User A, but User A's data is physically sitting on Shard 2! The database instantly claims User A does not exist. Every single row in the 1-Trillion-row database is mathematically misaligned. To fix it, you must physically migrate millions of terabytes of data across the network to their new modulo homes, causing massive downtime. The solution to this flaw is "Consistent Hashing".

3. Compare ACID (Relational SQL) and BASE (NoSQL). Why did massive companies invent NoSQL?
   Answer: ACID (Atomicity, Consistency, Isolation, Durability) guarantees mathematical perfection. If a bank transfer fails midway, the entire transaction violently rolls back. However, enforcing this perfection across a globally distributed network requires heavy Locks, which crush performance and prevent horizontal scaling. Massive companies (like Amazon/Dynamo or Facebook/Cassandra) realized that for non-critical data (like a shopping cart or a 'Like' button), mathematical perfection is unnecessary. They invented BASE (Basically Available, Soft state, Eventual consistency). BASE completely abandons heavy ACID Locks, allowing the database to scale infinitely across thousands of cheap servers. It accepts that data might be slightly out of sync for a few milliseconds, but it guarantees absolute Availability and infinite Scale.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: System Design (Database Architecture) Completed.")
