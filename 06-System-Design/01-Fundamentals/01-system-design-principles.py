"""
# ==============================================================================
# LABORATORY: SYSTEM DESIGN (FUNDAMENTAL PRINCIPLES)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You are building a global e-commerce platform. During Black Friday, traffic 
# spikes from 1,000 requests per second to 100,000 requests per second.
# 
# A junior engineer suggests: "Let's buy a $500,000 supercomputer to run the 
# database!" This is Vertical Scaling (Scaling Up). It has a hard mathematical 
# ceiling. When you hit the ceiling, the system crashes, and the company dies.
#
# A senior engineer suggests: "Let's deploy 10,000 cheap $50 commodity servers!" 
# This is Horizontal Scaling (Scaling Out). The ceiling is mathematically infinite. 
# But now you have a Distributed System. 
#
# Suddenly, data is fractured across oceans. If the network between New York 
# and London goes down (a Network Partition), you face a terrifying mathematical 
# dilemma known as the CAP Theorem: Do you halt the system to prevent data 
# corruption (prioritizing Consistency), or do you allow users to keep buying 
# out-of-stock items (prioritizing Availability)?
#
# System Design is the rigorous mathematical study of trade-offs at extreme scale.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Horizontal vs Vertical Scaling.
# - Understand the CAP Theorem (Consistency, Availability, Partition Tolerance).
# - Understand PACELC (Latency vs Consistency in normal operation).
#
# ==============================================================================
"""

import time
import random
import threading

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. HORIZONTAL SCALING (LOAD BALANCING SIMULATION)
# ==============================================================================
class ServerNode:
    def __init__(self, name: str):
        self.name = name
        self.active_connections = 0

    def process_request(self) -> str:
        self.active_connections += 1
        # Simulate processing time
        time.sleep(0.01)
        self.active_connections -= 1
        return f"Processed by {self.name}"

class LoadBalancer:
    """
    Simulates a Layer 7 Load Balancer distributing traffic horizontally.
    """
    def __init__(self, servers: list[ServerNode]):
        self.servers = servers
        self.round_robin_index = 0

    def route_request_round_robin(self) -> str:
        """Distributes traffic purely evenly, one by one."""
        if not self.servers: return "Error: No servers available!"
        
        target_server = self.servers[self.round_robin_index]
        self.round_robin_index = (self.round_robin_index + 1) % len(self.servers)
        
        return target_server.process_request()

    def route_request_least_connections(self) -> str:
        """Distributes traffic intelligently to the least burdened server."""
        if not self.servers: return "Error: No servers available!"
        
        # O(N) scan to find the minimum. (In reality, LBs use min-heaps/O(1) tracking)
        target_server = min(self.servers, key=lambda s: s.active_connections)
        
        return target_server.process_request()

def demonstrate_horizontal_scaling():
    section_header("Horizontal Scaling (Load Balancing)")
    
    servers = [ServerNode("Server-Alpha"), ServerNode("Server-Beta"), ServerNode("Server-Gamma")]
    lb = LoadBalancer(servers)
    
    print("Simulating a burst of 6 requests (Round Robin):")
    for i in range(6):
        print(f"  Req {i+1}: {lb.route_request_round_robin()}")
        
    print("\nThe Load Balancer mathematically spread the 6 requests evenly ")
    print("across all 3 cheap servers, preventing any single machine from melting!")


# ==============================================================================
# 4. THE CAP THEOREM SIMULATION (DISTRIBUTED CONSENSUS)
# ==============================================================================
class DistributedDatabaseNode:
    def __init__(self, name: str):
        self.name = name
        self.data = {"inventory": 100}
        self.network_partition = False  # Simulates a severed fiber-optic cable

    def read_data(self) -> int:
        return self.data["inventory"]

    def write_data(self, new_val: int) -> bool:
        self.data["inventory"] = new_val
        return True

class CAPDistributedSystem:
    def __init__(self):
        # Two database nodes running in different geographic regions
        self.us_east = DistributedDatabaseNode("US-East")
        self.eu_west = DistributedDatabaseNode("EU-West")

    def simulate_network_partition(self) -> None:
        """A submarine cuts the trans-atlantic internet cable."""
        self.us_east.network_partition = True
        self.eu_west.network_partition = True
        print("\n[ALERT] MASSIVE NETWORK PARTITION DETECTED! Trans-Atlantic Cable Severed!")

    def client_purchase_CP_System(self, node: DistributedDatabaseNode, new_inventory: int) -> str:
        """
        CP (Consistency + Partition Tolerance):
        In a CP system (like MongoDB or HBase), Consistency is God. 
        If a network partition occurs, the system violently HALTS operations 
        rather than risk corrupting the data.
        """
        if node.network_partition:
            return f"[{node.name}] CP ERROR: Network is partitioned! I cannot verify data with the other node. To guarantee Consistency, I am shutting down (Loss of Availability)!"
            
        # Network is healthy, we can sync!
        node.write_data(new_inventory)
        return f"[{node.name}] CP SUCCESS: Inventory updated to {new_inventory}."

    def client_purchase_AP_System(self, node: DistributedDatabaseNode, new_inventory: int) -> str:
        """
        AP (Availability + Partition Tolerance):
        In an AP system (like Cassandra or DynamoDB), Availability is God.
        If a network partition occurs, the node happily accepts the write anyway!
        This guarantees the user is happy, but causes severe Data Inconsistency.
        """
        if node.network_partition:
            # We blindly accept the write!
            node.write_data(new_inventory)
            return f"[{node.name}] AP WARNING: Network is down, but I accepted the write anyway to stay Available! (Eventual Consistency required later)."
            
        node.write_data(new_inventory)
        return f"[{node.name}] AP SUCCESS: Inventory updated to {new_inventory}."

def demonstrate_cap_theorem():
    section_header("The CAP Theorem (Distributed Dilemmas)")
    
    system = CAPDistributedSystem()
    print("System State: Healthy. US and EU databases are perfectly synced.")
    
    system.simulate_network_partition()
    
    print("\n--- Scenario A: We configured the DB as a CP System (e.g., Banking) ---")
    print("A user in Europe tries to buy an item:")
    print(system.client_purchase_CP_System(system.eu_west, 99))
    print("Result: The user gets an ugly 500 Server Error. But the bank's ledger is 100% mathematically safe.")
    
    print("\n--- Scenario B: We configured the DB as an AP System (e.g., Twitter Likes) ---")
    print("A user in Europe clicks 'Like' on a post:")
    print(system.client_purchase_AP_System(system.eu_west, 101))
    print("Result: The user sees their 'Like' instantly! They are happy. BUT...")
    print(f"US-East thinks the likes are: {system.us_east.read_data()}")
    print(f"EU-West thinks the likes are: {system.eu_west.read_data()}")
    print("The databases are physically inconsistent! They must be reconciled later (Eventual Consistency).")


def run_all_labs():
    demonstrate_horizontal_scaling()
    demonstrate_cap_theorem()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Why is Vertical Scaling mathematically doomed to fail for global-scale applications?
   Answer: Vertical Scaling (buying a stronger CPU, more RAM, bigger hard drive) is bound by the laws of physics. Currently, the most powerful commercial servers top out at around 256 CPU cores and 8TB of RAM. Once your traffic exceeds what that single physical machine can handle, you cannot buy a "bigger" machine; they physically do not exist. Furthermore, vertical scaling introduces a massive Single Point of Failure (SPOF). If the motherboard of your $2 Million supercomputer fries, the entire company instantly goes offline. Horizontal Scaling uses an infinite number of cheap machines, providing mathematically unbounded scaling and absolute fault tolerance.

2. Explain the CAP Theorem. Why can you only choose 2 out of the 3?
   Answer: CAP stands for Consistency, Availability, and Partition Tolerance. A "Partition" means the network has physically snapped, and two servers can no longer communicate. You CANNOT choose to avoid Partitions; hardware fails, networks drop. Therefore, Partition Tolerance (P) is mandatory for distributed systems. When a partition strikes, a user sends a Write request to Server A. Server A cannot talk to Server B. You are forced into a mathematical binary choice:
   Choice 1 (CP): Server A refuses the Write. The system loses Availability, but guarantees the data on A and B remains perfectly Consistent.
   Choice 2 (AP): Server A accepts the Write. The system remains highly Available, but Server A now has different data than Server B, destroying Consistency!
   You physically cannot accept the Write AND keep the separated servers synced.

3. What is the PACELC Theorem, and how does it extend CAP?
   Answer: PACELC was created in 2010 to fix a major flaw in CAP. The CAP theorem ONLY applies during a catastrophic network failure (a Partition). But networks don't fail every second! What happens during the 99.99% of the time when the system is running perfectly normally? PACELC states: "If there is a Partition (P), how does the system trade off Availability (A) and Consistency (C)? ELse (E), when the system is running normally, how does it trade off Latency (L) and Consistency (C)?" 
   During normal operation, if you demand strict Consistency, you must wait for Server A to ping Server B and receive a mathematical confirmation before replying to the user. This mandatory waiting period destroys Latency (Speed)! PACELC acknowledges that even without a catastrophe, Consistency and Speed are fundamentally mathematically opposed.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: System Design (Fundamentals) Completed.")
