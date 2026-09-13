# System Design Interviews: A Comprehensive Guide

## 1. What is a System Design Interview?

While coding interviews evaluate your ability to write correct, optimal code at the micro-level, System Design interviews evaluate your ability to architect large-scale, distributed software systems. They are open-ended conversations meant to assess how you handle ambiguity, navigate trade-offs, and design systems that are scalable, reliable, and maintainable.

System design is critical for mid-level and senior software engineering roles.

---

## 2. The 7-Step Framework for System Design

Never start drawing boxes on a whiteboard immediately. Follow a structured framework to guide the conversation.

### Step 1: Requirements Clarification (5-7 mins)
**Never assume.** Ask questions to narrow down the scope of the problem.
*   **Functional Requirements:** What should the system do? (e.g., "Users can post a 140-char tweet", "Users can view a timeline").
*   **Non-Functional Requirements:** 
    *   **Scale:** How many DAU (Daily Active Users)? How many writes/reads per second?
    *   **Latency:** Does this need to be real-time? (e.g., chat application) or is eventual consistency fine?
    *   **Availability vs. Consistency (CAP Theorem):** Does the system need to be highly available (it's okay if data is slightly stale) or highly consistent (financial transactions)?

### Step 2: Back-of-the-Envelope Estimation (Capacity Planning) (5 mins)
Perform rough calculations to understand the system's scale.
*   Traffic estimates (QPS - Queries Per Second).
*   Storage estimates (How much data added per day/year?).
*   Bandwidth estimates.
*   *Tip:* Round numbers generously to make mental math easier (e.g., $10^5 \times 10^4 = 10^9$).

### Step 3: API Design (5 mins)
Define the core APIs the client will call. This solidifies the contract.
*   Example for a Tweet: `postTweet(user_id, text, location_id, media_ids)` -> returns `tweet_id`.
*   Discuss REST vs. GraphQL vs. gRPC briefly if relevant.

### Step 4: Data Model Design (5-7 mins)
Define the core entities and how they relate. Choose the right database paradigm.
*   **Relational (SQL):** PostgreSQL, MySQL. Good for structured data, strong schemas, ACID properties (e.g., User profiles, Financial data).
*   **NoSQL (Document/Column/Key-Value):** MongoDB, Cassandra, DynamoDB. Good for massive scale, flexible schemas, rapid development (e.g., Tweets, logs, session data).
*   Define the schema: Tables, columns, primary keys, foreign keys.

### Step 5: High-Level Design (10-15 mins)
Draw the core components. Start simple and connect the dots from the client to the database.
*   Client -> Load Balancer -> Web/Application Servers -> Database.
*   Identify the read path and the write path.

### Step 6: Detailed Design & Deep Dives (10 mins)
This is where the interviewer will ask you to zoom in on specific parts.
*   "How do we handle the database becoming a bottleneck?" -> Discuss sharding, replication.
*   "How do we reduce latency for reads?" -> Discuss caching layers (Redis/Memcached) or CDNs.

### Step 7: Bottlenecks & Trade-offs (3-5 mins)
Identify single points of failure (SPOFs) and discuss what happens if traffic spikes 10x. Propose solutions (monitoring, autoscaling, message queues).

---

## 3. Core System Design Concepts

You must understand these building blocks intimately.

### 3.1 Vertical vs. Horizontal Scaling
*   **Vertical Scaling (Scale Up):** Adding more CPU/RAM to a single server. Easy, but has a hard upper limit and represents a single point of failure.
*   **Horizontal Scaling (Scale Out):** Adding more servers to a pool of resources. Harder to manage (requires load balancing, distributed state), but theoretically infinite scaling capability.

### 3.2 Load Balancing
Distributes incoming network traffic across a group of backend servers (a server farm or server pool).
*   **Types:** Layer 4 (Transport layer, TCP/UDP), Layer 7 (Application layer, HTTP).
*   **Algorithms:** Round Robin, Least Connections, IP Hash.

### 3.3 Caching
A temporary storage area that stores the result of expensive responses or frequently accessed data in memory to serve subsequent requests faster.
*   **Read-Through:** Application asks cache. If miss, cache fetches from DB, returns to app.
*   **Write-Through:** Application writes to cache. Cache writes to DB. Safe, but slow writes.
*   **Write-Behind (Write-Back):** Application writes to cache. Cache acknowledges immediately, asynchronously writes to DB. Fast, but risk of data loss if cache crashes before sync.
*   **Eviction Policies:** LRU (Least Recently Used), LFU (Least Frequently Used), TTL (Time to Live).

### 3.4 Databases: Sharding & Replication
*   **Replication:** Copying data across multiple servers. Typically Primary-Secondary. Primary handles writes, Secondaries handle reads. Improves read capacity and availability.
*   **Sharding (Data Partitioning):** Splitting a large database into smaller, faster, more easily managed parts called data shards horizontally.
    *   *Challenge:* Choosing a good shard key to prevent hotspots (e.g., sharding by user_id vs. sharding by timestamp).

### 3.5 Message Queues (Asynchronous Processing)
A communication component that buffers messages between a producer and a consumer. (e.g., Kafka, RabbitMQ, SQS).
*   **Use Cases:** Decoupling heavy background tasks (e.g., video processing, sending emails) from the critical path of the user request. Enhances system reliability (consumers can be down, messages wait in the queue).

### 3.6 The CAP Theorem
In a distributed system, you can only guarantee two of the following three properties:
1.  **Consistency (C):** Every read receives the most recent write or an error.
2.  **Availability (A):** Every request receives a (non-error) response, without the guarantee that it contains the most recent write.
3.  **Partition Tolerance (P):** The system continues to operate despite an arbitrary number of messages being dropped (or delayed) by the network between nodes.

*Note: Since network partitions (P) are unavoidable in distributed systems, you usually have to choose between CP (Consistency over Availability) or AP (Availability over Consistency).*

---

## 4. Example: Design a URL Shortener (e.g., TinyURL)

*(Brief walkthrough applying the framework)*

**1. Requirements:**
*   Given a long URL, return a short one.
*   Given a short URL, redirect to the long one.
*   Highly available, fast redirection. Over 100M URLs generated per month.

**2. Estimation:**
*   100M writes/month $\approx$ 40 writes/second.
*   Assuming 100:1 read/write ratio $\approx$ 4,000 reads/second.
*   Storage: 100M * 5 years * 500 bytes = ~300 TB.

**3. API:**
*   `createURL(api_dev_key, original_url, custom_alias=None)`
*   `getURL(api_dev_key, short_url)`

**4. Data Model:**
*   Relational or NoSQL? We have billions of simple rows, with no complex relationships. NoSQL (like DynamoDB or Cassandra) is a great fit for scaling this easily.
*   Table `URL_Mapping`: `hash` (PK), `original_url`, `creation_date`, `expiration_date`, `user_id`.

**5. High-Level Design:**
*   Client -> Load Balancer -> App Servers.
*   App Servers generate a unique ID, convert to Base62 (a-z, A-Z, 0-9).
*   App Servers store mapping in DB.
*   For reads: App server looks up Base62 string in DB, returns 301 Redirect.

**6. Deep Dive (Bottlenecks):**
*   **ID Generation:** How to ensure unique IDs across distributed app servers? Use a central ID generator (like Twitter Snowflake) or pre-allocate ranges to app servers via ZooKeeper.
*   **Read Latency:** 4K reads/second. Introduce a caching layer (Redis) in front of the database. Cache 20% of the most accessed URLs (Pareto principle).

**7. Summary:**
By focusing on scalability for reads via caching and ensuring distributed, collision-free ID generation, we design a robust URL shortener capable of handling massive traffic.
