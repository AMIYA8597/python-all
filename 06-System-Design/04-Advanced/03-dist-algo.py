"""
# ==============================================================================
# LABORATORY: SYSTEM DESIGN (DISTRIBUTED ALGORITHMS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# You have 5 database servers spread across the globe. You are using 
# Master-Slave Replication.
# 
# Suddenly, the Master server in New York loses power. 
# The 4 surviving Slave servers are now leaderless. Without a Master, the system 
# cannot accept any Write requests. The system is down.
#
# How do 4 independent computers, communicating over a laggy internet, mathematically 
# agree on who should become the new Master? 
# If two servers both decide they are the Master (Split-Brain), they will corrupt 
# the database irreversibly. 
#
# You must use a Distributed Consensus Algorithm (like Raft or Paxos) to safely 
# hold an "Election". 
#
# Furthermore, what happens when Server A receives a message at 10:00:01 AM, 
# and Server B receives a message at 10:00:02 AM? You cannot trust the physical 
# clocks! Server A's physical motherboard clock might be 5 seconds faster than 
# Server B's. You must use "Vector Clocks" to mathematically prove the absolute 
# chronological order of events without relying on physical time!
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Understand the Raft Leader Election process (Heartbeats & Quorum).
# - Understand the horrific Split-Brain problem.
# - Master Vector Clocks (Logical Time).
#
# ==============================================================================
"""

import time
import random

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. RAFT CONSENSUS: LEADER ELECTION (SIMULATION)
# ==============================================================================
class RaftNode:
    def __init__(self, node_id: int):
        self.node_id = node_id
        self.state = "FOLLOWER" # FOLLOWER, CANDIDATE, LEADER
        self.current_term = 0
        self.voted_for = None
        
        # A randomized timeout prevents all nodes from waking up at the exact same millisecond!
        self.election_timeout = random.uniform(0.150, 0.300) 
        self.last_heartbeat = time.time()

    def receive_heartbeat(self, term: int, leader_id: int) -> None:
        """Called when the Leader pings this node to suppress its election timer."""
        if term >= self.current_term:
            self.state = "FOLLOWER"
            self.current_term = term
            self.last_heartbeat = time.time() # Reset the bomb!
            print(f"    [Node {self.node_id}] Heartbeat received from Leader {leader_id}.")
            
    def request_vote(self, candidate_term: int, candidate_id: int) -> bool:
        """Called when another node begs this node for a vote to become Leader."""
        if candidate_term > self.current_term:
            self.current_term = candidate_term
            self.voted_for = candidate_id
            self.state = "FOLLOWER"
            print(f"    [Node {self.node_id}] Voted YES for Candidate {candidate_id}!")
            return True
        return False

def simulate_raft_election():
    section_header("Raft Consensus (Leader Election)")
    
    nodes = [RaftNode(1), RaftNode(2), RaftNode(3), RaftNode(4), RaftNode(5)]
    print("Cluster of 5 Nodes Initialized. All starting as FOLLOWERS.")
    
    # 1. The Master dies!
    print("\n[DISASTER] The Master Node has died! Heartbeats stop.")
    time.sleep(0.3) # Wait for timeouts to trigger
    
    # 2. Node 3's randomized timer goes off first!
    candidate = nodes[2] # Node 3
    print(f"\n[ELECTION] Node 3's election timer expired first! It becomes a CANDIDATE.")
    candidate.state = "CANDIDATE"
    candidate.current_term += 1
    candidate.voted_for = candidate.node_id
    
    votes = 1 # It votes for itself
    
    # 3. Request votes from the cluster
    for other_node in nodes:
        if other_node.node_id != candidate.node_id:
            if other_node.request_vote(candidate.current_term, candidate.node_id):
                votes += 1
                
    # 4. Quorum Check!
    # To win an election in a 5 node cluster, you need a strict majority (3).
    quorum_needed = (len(nodes) // 2) + 1
    print(f"\n[QUORUM] Node 3 received {votes} votes. Needed: {quorum_needed}.")
    
    if votes >= quorum_needed:
        candidate.state = "LEADER"
        print("[SUCCESS] Node 3 is officially the new LEADER!")
        print("Node 3 instantly begins broadcasting Heartbeats to suppress the others...")
        for other_node in nodes:
            if other_node.node_id != candidate.node_id:
                other_node.receive_heartbeat(candidate.current_term, candidate.node_id)


# ==============================================================================
# 4. VECTOR CLOCKS (LOGICAL TIME)
# ==============================================================================
class VectorClockNode:
    """
    Physical clocks drift. Server A's clock might be 5 seconds ahead of Server B.
    A Vector Clock is an array of integers `[A, B, C]`.
    It mathematically tracks the "Causality" (Cause and Effect) of events.
    """
    def __init__(self, node_id: int, total_nodes: int):
        self.id = node_id
        # The internal clock vector: [0, 0, 0]
        self.clock = [0] * total_nodes

    def perform_local_event(self) -> list[int]:
        """An event occurs on this node. It simply ticks its own physical index up by 1."""
        self.clock[self.id] += 1
        return self.clock.copy()

    def receive_message(self, incoming_clock: list[int]) -> list[int]:
        """
        When receiving a message from another node, it synchronizes causality!
        It takes the maximum of its own knowledge and the incoming knowledge, 
        and then ticks its own clock.
        """
        for i in range(len(self.clock)):
            self.clock[i] = max(self.clock[i], incoming_clock[i])
        
        # Tick for the "Receive Event" itself
        self.clock[self.id] += 1
        return self.clock.copy()

def compare_vector_clocks(clock1: list[int], clock2: list[int]) -> str:
    """
    Mathematically proves if Event 1 CAUSED Event 2.
    For Clock 1 to 'Happen Before' Clock 2, EVERY integer in Clock 1 must be <= Clock 2,
    AND at least ONE integer must be strictly <.
    """
    is_less_or_equal = all(v1 <= v2 for v1, v2 in zip(clock1, clock2))
    is_strictly_less = any(v1 < v2 for v1, v2 in zip(clock1, clock2))
    
    is_greater_or_equal = all(v1 >= v2 for v1, v2 in zip(clock1, clock2))
    is_strictly_greater = any(v1 > v2 for v1, v2 in zip(clock1, clock2))
    
    if is_less_or_equal and is_strictly_less:
        return "Event 1 HAPPENED BEFORE Event 2 (Causal Link)"
    elif is_greater_or_equal and is_strictly_greater:
        return "Event 2 HAPPENED BEFORE Event 1 (Causal Link)"
    else:
        return "CONCURRENT! (The events happened independently in different parts of the world!)"

def demonstrate_vector_clocks():
    section_header("Vector Clocks (Causality without Physical Time)")
    
    node_A = VectorClockNode(0, 3) # Node 0
    node_B = VectorClockNode(1, 3) # Node 1
    node_C = VectorClockNode(2, 3) # Node 2
    
    print("Initial State: A[0,0,0], B[0,0,0], C[0,0,0]")
    
    print("\n1. Node A creates a Post (Event A1).")
    clock_a1 = node_A.perform_local_event()
    print(f"   Node A Clock: {clock_a1}")
    
    print("\n2. Node A sends the Post to Node B.")
    clock_b1 = node_B.receive_message(clock_a1)
    print(f"   Node B receives it. Node B Clock updates to: {clock_b1}")
    
    print("\n3. Meanwhile, Node C independently creates a Post (Event C1).")
    clock_c1 = node_C.perform_local_event()
    print(f"   Node C Clock: {clock_c1}")
    
    print("\n--- CAUSALITY ANALYSIS ---")
    print("Did Event A1 cause Event B1?")
    print(f"Compare {clock_a1} vs {clock_b1}: {compare_vector_clocks(clock_a1, clock_b1)}")
    
    print("\nDid Event A1 cause Event C1?")
    print(f"Compare {clock_a1} vs {clock_c1}: {compare_vector_clocks(clock_a1, clock_c1)}")


def run_all_labs():
    simulate_raft_election()
    demonstrate_vector_clocks()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. What is "Split-Brain", and how does the concept of a "Quorum" in Raft prevent it?
   Answer: Split-Brain occurs when a network partition snaps the cluster in half. Suppose you have 5 nodes (2 in NY, 3 in LA). The network between NY and LA breaks. The 2 NY nodes think the Master is dead and elect a new Master. The 3 LA nodes think the Master is dead and elect a new Master. You now have TWO Masters accepting Writes! The database becomes fatally corrupted as data instantly diverges. Raft strictly prevents this using a "Quorum" (Strict Majority = $N/2 + 1$). In a 5-node cluster, you MUST get 3 votes to become a Master. Because the NY partition only has 2 nodes, it mathematically CANNOT achieve a Quorum of 3! NY is paralyzed and refuses to elect a Master. The LA partition has 3 nodes, achieves Quorum, and safely elects the singular Master. Split-Brain is mathematically impossible.

2. In Raft, why must the `election_timeout` be randomized?
   Answer: If the Master dies, and all 5 Followers have a hardcoded timeout of exactly 200ms, they will all wake up at the exact same physical millisecond. They will all transition to CANDIDATE, vote for themselves, and request votes from the others. Every node will get exactly 1 vote. No one will achieve the Quorum of 3. The election fails. They will all wait 200ms and try again, failing infinitely. By randomizing the timeout (e.g., between 150ms and 300ms), mathematically, one specific node will wake up at 162ms, instantly declare itself a Candidate, and snatch the votes from the sleeping nodes BEFORE they have a chance to wake up, safely resolving the election!

3. Why do Vector Clocks represent a mathematical array `[A, B, C]` instead of a single integer timestamp like `1700439221`?
   Answer: A single integer timestamp relies on the physical quartz crystal oscillating on the computer's motherboard. If Server A's physical clock drifts 5 seconds into the future, Server A will attach a "future" timestamp to an event. When you sort the database, it will look like Server A's event happened *after* Server B's response, which breaks the physical laws of Cause and Effect! A Vector Clock completely ignores physical time. The array `[1, 2, 0]` means: "I am aware of 1 event from Node A, 2 events from Node B, and 0 events from Node C". By passing this knowledge vector along with every network message, servers mathematically prove exactly what they knew, and *when* they knew it, allowing you to perfectly reconstruct the timeline of causality (who replied to whom) without ever looking at a physical clock.
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: System Design (Distributed Algorithms) Completed.")
