"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (MOCK INTERVIEWS - SYSTEM DESIGN)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# System Design interviews are entirely different from algorithmic coding. You 
# are not writing code; you are architecting a distributed system on a whiteboard. 
# There is no "perfect" answer, only a series of engineering trade-offs regarding 
# Scalability, Consistency, Availability, and Latency.
#
# A junior engineer is asked to "Design Twitter". They immediately start drawing 
# database tables and SQL schemas without ever asking how much traffic the 
# system needs to handle, failing the interview instantly.
#
# A senior engineer uses the "PEDALS" methodology:
# - Requirements: Functional (What does it do?) and Non-Functional (Scale, HA).
# - Estimation: Back-of-the-envelope math (QPS, Storage capacity).
# - Data Model: Schemas (SQL vs NoSQL).
# - High-Level Architecture: Load Balancers, Web Servers, DB clusters.
# - Detailed Component Design: Caching, Sharding, Message Queues.
# - Bottlenecks: Identifying failure points and resolving them.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master the PEDALS system design framework.
# - Master Back-of-the-Envelope Capacity Estimation.
# - Understand how to mathematically justify NoSQL vs SQL.
#
# ==============================================================================
"""

import time
import sys

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")

def simulate_typing(text: str, delay: float = 0.02):
    """Simulates real-time terminal output for interview realism."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


# ==============================================================================
# 3. THE PEDALS METHODOLOGY: A LIVE SIMULATION
# ==============================================================================
def system_design_mock_simulation():
    section_header("Live Simulation: The PEDALS Framework (Design URL Shortener)")
    
    simulate_typing("INTERVIEWER: 'I want you to design a URL Shortening service like TinyURL.'")
    
    simulate_typing("\n[STAGE 1: REQUIREMENTS (Scope the System)]")
    simulate_typing("CANDIDATE: 'Let's define the scope.'")
    simulate_typing("CANDIDATE: 'Functional: 1. Generate short URL. 2. Redirect to original URL. 3. Custom short links?'")
    simulate_typing("INTERVIEWER: 'Yes to 1 and 2. No custom links to save time.'")
    simulate_typing("CANDIDATE: 'Non-Functional: Highly Available? Low Latency redirect? Read-heavy system?'")
    simulate_typing("INTERVIEWER: 'Yes, 99.99% Availability. Redirects must be under 10ms. It is extremely read-heavy.'")
    
    simulate_typing("\n[STAGE 2: ESTIMATION (Back-of-the-envelope Math)]")
    simulate_typing("CANDIDATE: 'Let's calculate the load.'")
    simulate_typing("CANDIDATE: 'Assume 100 Million new URLs generated per month.'")
    simulate_typing("CANDIDATE: 'Write QPS: 100M / (30 days * 24h * 3600s) = ~40 Writes/sec.'")
    simulate_typing("CANDIDATE: 'Read to Write ratio is 100:1. So Read QPS = 4,000 Reads/sec.'")
    simulate_typing("CANDIDATE: 'Storage: If each URL mapping is 500 bytes, 100M * 500 bytes = 50 GB per month. Over 10 years, that is 6 TB. A single modern hard drive can hold this.'")
    
    simulate_typing("\n[STAGE 3: DATA MODEL (Choosing the Database)]")
    simulate_typing("CANDIDATE: 'Since the data is just a simple mapping (ShortURL -> LongURL) with no complex relationships or joins, a NoSQL Key-Value store (like DynamoDB or Cassandra) is vastly superior to SQL. It scales horizontally flawlessly.'")
    
    simulate_typing("\n[STAGE 4: HIGH-LEVEL ARCHITECTURE]")
    simulate_typing("CANDIDATE: 'The client hits a DNS, which routes to our Load Balancer.'")
    simulate_typing("CANDIDATE: 'The LB distributes traffic across stateless Web Servers.'")
    simulate_typing("CANDIDATE: 'The Web Servers talk to a distributed NoSQL Database.'")
    
    simulate_typing("\n[STAGE 5: DETAILED COMPONENT DESIGN (The Core Algorithm)]")
    simulate_typing("CANDIDATE: 'How do we generate the short link? We can use a Base62 encoding on a globally unique integer.'")
    simulate_typing("CANDIDATE: 'To prevent DB collisions, we use a dedicated Ticket Server (or ZooKeeper) to hand out strictly increasing, unique integer IDs. We convert ID 1000 to a Base62 string, e.g., \"aB4\".'")
    simulate_typing("CANDIDATE: 'For the 10ms latency constraint, the Web Servers cannot hit the DB for every read. We must inject a Caching Layer (Redis) in front of the DB.'")
    
    simulate_typing("\n[STAGE 6: BOTTLENECKS (Trade-offs & Scaling)]")
    simulate_typing("CANDIDATE: 'What if the Redis cache fails? The DB will instantly receive 4,000 QPS and might crash (Thundering Herd). We mitigate this by distributing the cache and utilizing read-replicas for the DB.'")
    
    simulate_typing("\nINTERVIEWER: 'Excellent architectural breakdown. You passed.'")


# ==============================================================================
# 4. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "Why is 'Estimation' a mandatory step in System Design? Why can't we just design a scalable system that handles anything?"
   Senior Answer: "Architecture is entirely dictated by mathematical scale. If the total storage for 10 years is only 5 GB, deploying a massively sharded NoSQL Cassandra cluster is catastrophic over-engineering that wastes company resources; a single MySQL instance is flawless. If the read QPS is 100,000 per second, you physically MUST introduce a Redis Caching layer, otherwise the database connection pool will violently exhaust. By calculating the exact QPS and Terabyte load, you mathematically prove exactly *why* your chosen architecture is necessary, anchoring your design in engineering reality rather than buzzwords."

2. Interviewer: "In the URL Shortener design, why is a NoSQL Key-Value store structurally superior to a SQL Relational Database?"
   Senior Answer: "SQL databases enforce strict ACID compliance, rigid schemas, and support complex `JOIN` operations. A URL shortener possesses absolutely zero relational data; it is a microscopic $1:1$ mapping between a short string and a long string. Forcing this into SQL incurs overhead for relational locks and transactions that we do not need. More importantly, as the database grows to 6 TB, SQL is notoriously difficult to scale horizontally (sharding). A NoSQL Key-Value store (like DynamoDB) natively shards data across hundreds of physical nodes using consistent hashing, delivering mathematically guaranteed sub-millisecond lookup latency at infinite scale."

3. Interviewer: "Why did the candidate propose a 'Ticket Server / ZooKeeper' instead of just using a standard Random Number Generator to create the short URL?"
   Senior Answer: "If you use a Random Number Generator, you introduce the mathematical risk of Collisions. Two web servers might randomly generate the exact same string ('aB4') simultaneously. To safely insert it into the DB, you must execute a costly 'Read-Before-Write' check. If it exists, you have to generate a new string and retry, causing a catastrophic performance spiral under heavy load. By using a centralized Ticket Server that dispenses strictly increasing atomic integers ($1, 2, 3...$), we mathematically guarantee $100\\%$ global uniqueness. We run a deterministic Base62 algorithm on the integer, entirely eliminating collisions and bypassing the DB read-check entirely."
"""

if __name__ == "__main__":
    system_design_mock_simulation()
    print("\n[SUCCESS] Laboratory: Mock Interviews (System Design) Completed.")
