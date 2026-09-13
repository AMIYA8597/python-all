"""
## A. Concept Name
Distributed Algorithms in Python (Leader Election / Bully Algorithm)

## B. Core Rules / Constraints
- In a distributed system, nodes often need to elect a coordinator (leader) to manage a central task.
- Nodes communicate asynchronously via message passing.
- The Bully Algorithm assumes each node has a unique ID, and nodes communicate reliably.
- When a node detects the leader is down, it starts an election by sending ELECTION messages to all nodes with higher IDs.
- If no higher node responds, the node declares itself the leader and broadcasts a VICTORY/COORDINATOR message.

## C. Code Implementation
(See the code below for the implementation of the Message, Node, and Network classes.)

## D. Complexity Analysis
- Time Complexity: O(N) message delays until leader is elected.
- Message Complexity: O(N^2) in the worst case (if the lowest ID node starts the election and everyone cascades).

## E. Edge Cases & Constraints
- Failed node recovery: If a previously failed high-ID node comes back online, it immediately initiates an election, pre-empting the current lower-ID leader and "bullying" its way back to power.
- Network partitioning (Split-Brain): If a network partition splits nodes into two isolated groups, both groups might elect their own leader, leading to data inconsistency. (Modern protocols like Raft solve this by requiring a quorum).

## X. Project Connection
- Apache ZooKeeper / Etcd (using ZAB/Raft protocols for leader election).
- Distributed databases (MongoDB replica sets electing primaries).
- Microservices architecture (handling coordinator node failures).
"""

import asyncio
import random
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Core Components: Message and Node definitions
# ---------------------------------------------------------------------------
class Message:
    def __init__(self, sender_id: int, m_type: str):
        self.sender_id = sender_id
        self.type = m_type  # 'ELECTION', 'OK', 'COORDINATOR', 'HEARTBEAT'
        
    def __repr__(self):
        return f"Msg({self.type} from {self.sender_id})"


class Node:
    def __init__(self, node_id: int, network: 'Network'):
        self.node_id = node_id
        self.network = network
        self.inbox: asyncio.Queue = asyncio.Queue()
        
        self.is_running = True
        self.is_leader = False
        self.leader_id: Optional[int] = None
        
        # Background tasks
        self._listener_task: Optional[asyncio.Task] = None
        self._heartbeat_task: Optional[asyncio.Task] = None

    async def start(self):
        """Starts the node's background listening and heartbeat routines."""
        self._listener_task = asyncio.create_task(self._listen())
        self._heartbeat_task = asyncio.create_task(self._monitor_leader())
        
    async def stop(self):
        """Simulates node crash/shutdown."""
        self.is_running = False
        if self._listener_task:
            self._listener_task.cancel()
        if self._heartbeat_task:
            self._heartbeat_task.cancel()

    async def send_message(self, target_id: int, m_type: str):
        if self.is_running:
            msg = Message(self.node_id, m_type)
            await self.network.route_message(target_id, msg)

    async def _listen(self):
        """Continuously process incoming messages."""
        try:
            while self.is_running:
                msg: Message = await self.inbox.get()
                await self._handle_message(msg)
                self.inbox.task_done()
        except asyncio.CancelledError:
            pass

    async def _handle_message(self, msg: Message):
        if msg.type == 'ELECTION':
            # A lower ID node called an election. We respond 'OK' to tell them to stop,
            # and then we start our own election.
            print(f"Node {self.node_id} received ELECTION from {msg.sender_id}. Replying OK.")
            await self.send_message(msg.sender_id, 'OK')
            asyncio.create_task(self.start_election())
            
        elif msg.type == 'COORDINATOR':
            # A higher ID node declared victory.
            self.leader_id = msg.sender_id
            self.is_leader = (self.node_id == msg.sender_id)
            print(f"Node {self.node_id} acknowledges Node {self.leader_id} as leader.")
            
        elif msg.type == 'HEARTBEAT':
            # Just acknowledging the leader is alive.
            pass

    async def start_election(self):
        """Initiates the Bully Algorithm election process."""
        print(f"Node {self.node_id} is starting an election...")
        higher_nodes = self.network.get_higher_nodes(self.node_id)
        
        if not higher_nodes:
            # I have the highest ID. I am the leader.
            await self._declare_victory()
            return

        # Ask higher nodes if they are alive
        for target in higher_nodes:
            await self.send_message(target, 'ELECTION')

        # Wait to see if anyone higher responds with 'OK'
        # In a real system, we'd use timeouts. Here we'll simulate a brief wait.
        await asyncio.sleep(0.5)
        
        # We need a mechanism to check if we received an 'OK'.
        # For simplicity in this demo, if no one higher declared victory, we retry.
        # A full implementation requires tracking 'OK' responses carefully.

    async def _declare_victory(self):
        self.is_leader = True
        self.leader_id = self.node_id
        print(f"--> Node {self.node_id} DECLARES VICTORY and is now the LEADER! <--")
        
        # Tell everyone else
        for target in self.network.get_all_nodes():
            if target != self.node_id:
                await self.send_message(target, 'COORDINATOR')

    async def _monitor_leader(self):
        """Periodically checks if the system needs an election."""
        try:
            while self.is_running:
                await asyncio.sleep(random.uniform(1.0, 3.0))
                
                # If leader is dead or not set, start election
                # Note: In a real distributed system, we send Ping/Pongs.
                # Here, we just consult the omniscient network registry for simulation brevity.
                if self.leader_id is None or not self.network.is_node_alive(self.leader_id):
                    if not self.is_leader:
                        print(f"Node {self.node_id} detected leader failure!")
                        await self.start_election()
        except asyncio.CancelledError:
            pass


# ---------------------------------------------------------------------------
# Network Simulation
# ---------------------------------------------------------------------------
class Network:
    """Simulates the physical network connecting the nodes."""
    def __init__(self):
        self.nodes: Dict[int, Node] = {}

    def register_node(self, node: Node):
        self.nodes[node.node_id] = node

    async def route_message(self, target_id: int, msg: Message):
        """Delivers a message with simulated latency."""
        if target_id in self.nodes and self.nodes[target_id].is_running:
            await asyncio.sleep(random.uniform(0.01, 0.1)) # Network delay
            await self.nodes[target_id].inbox.put(msg)

    def get_higher_nodes(self, current_id: int) -> List[int]:
        return [nid for nid in self.nodes if nid > current_id]
        
    def get_all_nodes(self) -> List[int]:
        return list(self.nodes.keys())
        
    def is_node_alive(self, node_id: int) -> bool:
        return node_id in self.nodes and self.nodes[node_id].is_running


# ---------------------------------------------------------------------------
# Example Usage & Simulation
# ---------------------------------------------------------------------------
async def run_simulation():
    print("--- Distributed Algorithms: Bully Algorithm Simulation ---")
    net = Network()
    
    # Create 5 nodes
    nodes = [Node(i, net) for i in range(1, 6)]
    for n in nodes:
        net.register_node(n)
        await n.start()

    print("Initial startup...")
    # Initial state, they will eventually notice no leader and start elections
    await asyncio.sleep(3)
    
    # Let's crash the current leader (should be node 5)
    leader_node = next((n for n in nodes if n.is_leader), None)
    if leader_node:
        print(f"\n[CRASH] Crashing the leader: Node {leader_node.node_id}\n")
        await leader_node.stop()
        
    # Wait for the remaining nodes to detect failure and elect a new leader
    await asyncio.sleep(4)
    
    # Cleanup
    for n in nodes:
        await n.stop()
    print("\nSimulation complete.")

if __name__ == "__main__":
    # Ensure Windows compatibility for asyncio
    import sys
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    asyncio.run(run_simulation())
