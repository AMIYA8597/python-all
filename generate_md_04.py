import os

file_path = r"d:\work\python-all\07-Interview-Preparation\01-Theory\04-Sys-Design-Int.md"
os.makedirs(os.path.dirname(file_path), exist_ok=True)

md_content = """# The FAANG System Design Interview: A Textbook Guide
## 1. Why This Matters
System design interviews (SDI) have become the most critical component of the software engineering interview loop for mid-level and senior roles at top technology companies (FAANG - Facebook, Amazon, Apple, Netflix, Google). Unlike algorithms and data structures interviews, which have definitive optimal solutions, system design interviews are open-ended, highly ambiguous, and simulate real-world architectural planning. Your performance in this interview dictates not only whether you are hired, but the level at which you are placed. A strong performance can mean the difference between a mid-level (L4) and a senior (L5) offer, which translates to a massive gap in compensation, equity, and responsibility. Understanding how to systematically break down, estimate, and design a scalable system is essential to navigating this ambiguity and proving your engineering maturity.

## 2. Prerequisites
Before attempting to conquer the system design interview, a candidate must have a robust foundational understanding of distributed systems concepts. This includes:
- **Networking Protocols**: TCP/IP, HTTP/1.1, HTTP/2, WebSockets, UDP.
- **Databases**: Relational databases (ACID properties, indexing, sharding, replication) vs. NoSQL (Key-Value, Document, Wide-Column, Graph databases, CAP Theorem, BASE properties).
- **Caching**: Eviction policies (LRU, LFU), caching strategies (Cache-Aside, Write-Through, Write-Back), Memcached, Redis.
- **Message Queues**: RabbitMQ, Kafka, asynchronous processing, decoupling.
- **Load Balancing**: Layer 4 vs. Layer 7 load balancing, reverse proxies (Nginx, HAProxy), consistent hashing.
- **System Architecture Patterns**: Microservices, monolithic architecture, serverless, event-driven architecture.

## 3. Introduction
The System Design Interview typically lasts 45 to 60 minutes. You will be given a highly vague prompt, such as "Design Twitter" or "Design a URL shortener." Your task is to lead the conversation, extract the actual requirements, make justified trade-offs, and construct an architecture that can scale to millions of users. It is less about getting the "right" answer and more about the journey—how you communicate, how you handle constraints, and your awareness of the inherent trade-offs in distributed systems.

## 4. Problem Solved
This framework solves the "blank whiteboard paralysis." When faced with a massive problem like "Design WhatsApp," it is easy to become overwhelmed or dive straight into database schema without understanding the scale. The FAANG 7-Step Framework provides a deterministic structure for an inherently non-deterministic problem. It gives the interviewer a clear signal of your methodical approach and ensures you don't miss crucial elements like estimations and bottleneck analysis.

## 5. Mental Model
Think of the System Design Interview as building a city.
- **Requirements Clarification**: Zoning laws and city planning. What are we building? A quiet suburb or a dense metropolis?
- **Estimations**: Population projections. How much water, electricity, and road capacity do we need?
- **System Interface**: The blueprints. What are the public roads entering the city?
- **Data Model**: The physical terrain and property boundaries. How is everything stored?
- **High-Level Design**: The major highways and power grids. The macro view of the city.
- **Detailed Design**: The intersections and traffic lights. How do the specific parts interact?
- **Bottlenecks**: Traffic jams and power outages. What happens when the city grows 10x?

## 6. Visual Explanation
Imagine a funnel:
1. **Top of the funnel (Wide)**: Ambiguous problem. (e.g., "Design YouTube")
2. **Filtering through Requirements**: Narrowing it down. ("Only video uploading and viewing for 10M DAU")
3. **Filtering through APIs and Data**: Defining the contracts and storage.
4. **Middle of the funnel**: The High-Level Architecture diagram (Clients -> Load Balancer -> Web Servers -> Databases/Cache).
5. **Bottom of the funnel (Deep)**: Focusing on a few core components and discussing their deep technical trade-offs.

---

# The FAANG System Design Interview Framework

## 7. Step 1: Requirements Clarification (3-5 Minutes)
Never jump straight into the design. The prompt is intentionally vague. Your first job is to scope the problem down to something achievable in 45 minutes. You must ask questions to establish the bounds of the system.

**Functional Requirements:**
What should the system do? For "Design Twitter", this might be:
- Users can post tweets (text only, up to 280 characters).
- Users can follow other users.
- Users have a home timeline consisting of tweets from people they follow.
*Out of scope*: Analytics, video uploading, trending topics, authentication.

**Non-Functional Requirements:**
What are the system qualities?
- **High Availability (HA)** vs. **Strong Consistency**: Do we prefer the system to always be up, even if users see slightly stale data? For a social media feed, High Availability is preferred. For a financial system, Strong Consistency is mandatory.
- **Latency**: The timeline should generate in under 200ms.
- **Scale**: The system must support massive read loads compared to write loads.

## 8. Step 2: Back-of-the-envelope Estimation (5 Minutes)
This step demonstrates your ability to plan for scale. You are proving that you understand the difference between 10 requests per second (RPS) and 100,000 RPS.

**Traffic Estimates:**
- Daily Active Users (DAU): e.g., 100 Million.
- Read/Write Ratio: e.g., 100 reads for every 1 write (a read-heavy system).
- Tweets per day: 100M * 2 writes/user = 200M tweets/day.
- Read requests per day: 200M * 100 = 20 Billion reads/day.
- RPS (Writes): 200M / 100,000 seconds (approx in a day) = 2,000 Writes/sec.
- RPS (Reads): 20B / 100,000 = 200,000 Reads/sec.

**Storage Estimates:**
- Size of a tweet: 280 bytes of text + 20 bytes metadata = 300 bytes.
- Storage per day: 200M tweets * 300 bytes = 60 GB / day.
- Storage for 10 years: 60 GB * 365 * 10 = ~219 TB.

**Bandwidth Estimates:**
- Ingress: 2000 writes/sec * 300 bytes = 600 KB/sec.
- Egress: 200,000 reads/sec * 300 bytes = 60 MB/sec.

*Tip:* Always memorize standard conversions (e.g., 1 million requests per day is ~12 per second, 1 byte to TB conversions).

## 9. Step 3: System Interface Definition (3-5 Minutes)
Define the API contracts. This turns abstract functional requirements into concrete endpoints. It shows you understand RESTful design, gRPC, or GraphQL.

Example for Twitter:
- `postTweet(user_id, tweet_text, media_ids)` -> Returns `tweet_id`.
- `followUser(follower_id, followee_id)` -> Returns `status`.
- `getHomeTimeline(user_id, page_token)` -> Returns `List<Tweet>`.

Discuss whether to use REST (standard), GraphQL (good for mobile fetching complex relationships), or WebSockets (for real-time chat).

## 10. Step 4: Defining the Data Model (5 Minutes)
Choose the right database based on your requirements and estimations.

**Relational vs. NoSQL:**
- If you need complex joins, ACID properties, and structured data, choose Relational (PostgreSQL, MySQL).
- If you need massive horizontal scalability, flexible schema, and high throughput, choose NoSQL (Cassandra, DynamoDB, MongoDB).

**Schema Design for Twitter:**
- `Users Table`: `user_id` (PK), `username`, `email`, `creation_date`.
- `Tweets Table`: `tweet_id` (PK), `user_id` (FK), `content`, `timestamp`.
- `Follows Table`: `follower_id` (PK), `followee_id` (PK), `timestamp`.

For Twitter, a NoSQL database (like Cassandra) is often chosen for the `Tweets` and `Follows` tables due to the massive volume and need for high write/read throughput. A relational DB could be used for `Users` as it requires strong consistency for authentication and changes less frequently.

## 11. Step 5: High-Level Design (10-15 Minutes)
Draw the boxes and arrows. This is the macro-architecture.
1. **Client** (Mobile / Web App).
2. **DNS** resolving to a **Load Balancer**.
3. **API Gateways / Web Servers**: Handle authentication, rate limiting, and route requests to internal services.
4. **Service Layer**: 
    - `Tweet Service`: Handles posting and retrieving tweets.
    - `User Service`: Handles profile info and follows.
    - `Timeline Service`: Generates the timeline feed.
5. **Caching Layer**: Redis/Memcached to store hot tweets and pre-computed timelines.
6. **Database Layer**: Main storage.

Walk the interviewer through the lifecycle of a request. "When a user posts a tweet, it hits the Load Balancer, which routes to the Tweet Service. The Tweet Service saves it to the Database, updates the Cache, and pushes a notification to a Message Queue for asynchronous timeline generation."

## 12. Step 6: Detailed Design (10-15 Minutes)
This is where you dive deep into 2 or 3 core components. The interviewer will usually guide you here based on what they want to test.

**Deep Dive Example: Timeline Generation (Fan-out problem)**
- **Pull Model (Read-heavy)**: When user A loads their timeline, the system fetches all people they follow, gets their recent tweets, merges, sorts, and returns. *Pros*: Simple writes. *Cons*: Very slow for reads, especially if following thousands of users.
- **Push Model (Write-heavy / Fan-out on Write)**: When user B posts a tweet, the system looks up all their followers and pushes the tweet into their pre-computed timeline cache (Redis). *Pros*: Reads are instant O(1). *Cons*: If Justin Bieber (100M followers) posts a tweet, you must do 100M cache writes, which causes a huge spike and delay (the "Celebrity Problem").
- **Hybrid Model (The Solution)**: Use Push Model for normal users. Use Pull Model for celebrities. When a user loads their timeline, they pull their pre-computed feed (Push from normal users) and merge it at read-time with tweets pulled from the celebrities they follow.

## 13. Step 7: Identifying and Resolving Bottlenecks (5 Minutes)
Every system has flaws. Being able to critique your own design is a hallmark of a senior engineer.
- **Single Points of Failure**: Is there only one load balancer? Introduce redundancy.
- **Database Hotspots**: Are all users trying to read the same viral tweet? Add a distributed cache with a TTL. Introduce CDN for media.
- **Data Growth**: How do we handle 219 TB of data? We implement **Sharding**. We can shard tweets by `user_id` (so all tweets for a user are on the same node), but this causes hotspots for celebrities. We can shard by `tweet_id`, but then we have to query all shards to build a timeline. A composite shard key might be needed.
- **Latency**: Add read replicas for databases. Use a global CDN.

---

# 14. Massive Mock Interview Transcript: Design WhatsApp

**Interviewer**: We'd like you to design a messaging application like WhatsApp.
**Candidate**: Great. Let's start by clarifying the requirements to ensure we build exactly what's needed. 

### Step 1: Requirements
**Candidate**: For functional requirements, I assume users need one-on-one messaging. Do we also need group chats?
**Interviewer**: Yes, 1-on-1 and group chats are required.
**Candidate**: Do we support media (images, videos)? What about read receipts (sent, delivered, read)? And does it need to support voice/video calling?
**Interviewer**: Yes to media. Yes to read receipts. Let's keep voice and video calling out of scope for now to keep things simple.
**Candidate**: Got it. What about message history? Are messages stored permanently on the server, or only until delivered?
**Interviewer**: Let's mimic WhatsApp: messages are stored temporarily on the server until delivered, then deleted. Long-term storage is on the client device.
**Candidate**: Understood. For non-functional requirements, low latency is critical for a chat app. We also need high availability, though strong consistency of message ordering is also highly important.
**Interviewer**: Agreed.

### Step 2: Estimations
**Candidate**: Let's do some back-of-the-envelope math. Let's assume 1 Billion Daily Active Users (DAU).
If each user sends 50 messages a day, that's 50 Billion messages per day.
Messages per second: 50B / 100,000 seconds = 500,000 messages per second on average. Peak traffic might be 3x, so 1.5M messages/sec.
For storage, if a text message is 100 bytes, that's 5 TB of text per day. However, we only store messages until they are delivered. Assuming 90% of users are online and messages are delivered instantly, only a small fraction is stored. If 10% are offline, we hold 500 GB a day on average.
For media, if 10% of messages have media (average 1MB), that's 5B media files * 1MB = 5 Petabytes per day! We'll definitely need a robust blob storage and CDN strategy.

### Step 3: System Interface
**Candidate**: I'll define a few core APIs. Since this is a real-time chat app, HTTP REST isn't great for receiving messages due to polling overhead. I'll use **WebSockets** for a persistent, bidirectional connection between the client and the server.
However, for sending media, the client can use a standard HTTP POST to upload the file, get a URL back, and send that URL over the WebSocket.
- `sendMessage(sender_id, receiver_id, message_type, content/url)`
- `updateMessageStatus(message_id, status)` // status: sent, delivered, read
- `createGroup(user_ids)`
- `uploadMedia(file)` -> returns `media_url`

### Step 4: Data Model
**Candidate**: Even though messages are transient on the server, we need a highly scalable, write-heavy database to act as an inbox for offline users. I'll choose a NoSQL store like **Cassandra** or **DynamoDB** because of their ability to handle massive write throughput and easy horizontal scaling.

Tables:
- `Users`: `user_id`, `name`, `last_seen`, `device_token`
- `Messages_Inbox`: `user_id` (Partition Key), `message_id` (Sort Key), `sender_id`, `content`, `status`, `timestamp`. We partition by the *receiver's* user_id so we can quickly fetch all pending messages when they come online.
- `Groups`: `group_id`, `group_name`, `created_at`
- `Group_Members`: `group_id` (PK), `user_id` (SK)

### Step 5: High-Level Design
**Candidate**: Here is the macro view.
1. The client opens a WebSocket connection to a **Chat Server** via a Load Balancer.
2. Because we have 1 Billion DAU, we need thousands of Chat Servers. We need a way to know *which* Chat Server a user is connected to.
3. I'll introduce a **Presence Service** (using Redis) that maps `user_id -> chat_server_id`.
4. When Alice wants to message Bob:
   - Alice sends the message to her connected Chat Server (Server A) via WebSocket.
   - Server A queries the Presence Service to find Bob's Chat Server.
   - If Bob is connected to Server B, Server A forwards the message to Server B.
   - Server B pushes the message to Bob via his WebSocket.
   - If Bob is offline, Server A writes the message to the `Messages_Inbox` Database and triggers a push notification.

**Interviewer**: How do Server A and Server B communicate?
**Candidate**: They could communicate directly via RPC, but that creates a tightly coupled mesh. A better approach is to use a **Message Broker** like Kafka or RabbitMQ, or a Pub/Sub system (like Redis Pub/Sub). Server A publishes the message to a channel that Server B is subscribed to.

### Step 6: Detailed Design
**Interviewer**: Let's dig into the Presence Service and connection management. Maintaining 1 Billion concurrent WebSocket connections is tough. How do you handle it?
**Candidate**: A single modern server can handle maybe 1 million concurrent WebSocket connections (the C10K problem is now C1M) if we tune the OS (epoll, increasing file descriptors). For 1 Billion users, we need at least 1,000 servers, practically more like 2,000-5,000 for redundancy.
When a user connects, the Load Balancer routes them to a Chat Server. The Chat Server registers this connection in a Redis cluster: `Key: UserID, Value: ServerID`.
To maintain presence (online/offline status), the client sends periodic heartbeats (e.g., every 5 seconds) over the WebSocket. If the Chat Server misses 3 heartbeats, it marks the user as offline in Redis and closes the connection.
**Interviewer**: What happens if a Chat Server crashes?
**Candidate**: If Server A crashes, all 500,000 users connected to it lose their WebSocket connection. Their clients will automatically attempt to reconnect. The Load Balancer will route them to healthy servers.
However, this causes a "thundering herd" problem where 500,000 users try to reconnect at the exact same millisecond, potentially taking down the new servers. To mitigate this, clients must implement **Exponential Backoff with Jitter** when reconnecting.
Also, the Presence Service still thinks those users are on Server A. We can run a background cleaner service, or let the Redis keys have a TTL (Time To Live) that is refreshed by the heartbeats. If the server dies, heartbeats stop, the TTL expires, and the users are marked offline automatically.

**Interviewer**: Good. How do you handle Group Chats?
**Candidate**: Group chats change the routing dynamic. If Alice sends a message to a group with 100 members, we have a fan-out problem.
- Alice sends 1 message to her Chat Server.
- The Chat Server queries the `Group_Members` database to get the 100 `user_ids`.
- It then queries the Presence Service to find the Chat Servers for all 100 users.
- It routes the message to all those respective servers.
For groups with thousands of members, this fan-out can be intensive. We would delegate this to a dedicated **Group Message Handler** service using a message queue like Kafka to process the fan-out asynchronously so we don't block Alice's Chat Server.

### Step 7: Bottlenecks and Optimization
**Interviewer**: Excellent. What are the potential bottlenecks in your design?
**Candidate**:
1. **The Presence Service**: Redis is incredibly fast, but querying it for every single message sent (1.5M/sec) could overwhelm it. We can mitigate this by caching the `user_id -> server_id` mapping locally on the Chat Servers for a short time, though this risks stale data. We can also shard the Redis cluster heavily based on `user_id`.
2. **Media Storage and Bandwidth**: 5 Petabytes a day is massive. Media should not go through the Chat Servers. Clients should request a pre-signed URL from an Asset Service, upload directly to S3/Cloud Storage, and only pass the URL through the Chat Servers. We must heavily utilize CDNs to cache this media globally.
3. **Message Ordering**: In distributed systems, relying on timestamps for message ordering is dangerous due to clock drift across servers. We can use a unique sequence generator (like Twitter Snowflake or a local counter per chat thread) to ensure strict ordering of messages between Alice and Bob.
4. **End-to-End Encryption**: To support true privacy, the backend shouldn't know the content. Alice fetches Bob's public key from a Key Delivery Service, encrypts the message locally, and sends the ciphertext. The server just routes the ciphertext.

**Interviewer**: Very thorough. Thank you.

---

## 15. Edge Cases & Real-World Compromises
In actual production, textbook answers hit reality. You must be prepared to discuss edge cases:
- **Network Partitions (Split Brain)**: What happens if your data centers lose connection to each other? By CAP Theorem, you must choose between Consistency and Availability. For chat, you choose Availability. Messages might be delayed, but the app still functions locally.
- **Data Deletion/GDPR**: How do you actually delete data across all caches, replicas, and backups? This is notoriously difficult. Usually, systems implement soft deletes (flagging) and run batch jobs for hard deletion.
- **Mobile Network Flakiness**: Mobile clients drop connections constantly. Using optimistic UI updates (showing the message as sent instantly) and queuing retries locally on the phone is vital for perceived performance.

## 16. Active Recall & Quizzes
To truly internalize this framework, practice these recall questions without looking:
1. What is the difference between latency and throughput?
2. When would you choose a Document Store (MongoDB) over a Wide-Column Store (Cassandra)?
3. What is the "Thundering Herd" problem and what is the standard client-side solution?
4. Explain the difference between Fan-out on Read (Pull) vs Fan-out on Write (Push).
5. What are the CAP theorem guarantees of a standard relational database configured for synchronous replication?

## 17. Practice Interview Questions
Apply the 7-Step framework to these prompts. Do not write code; draw boxes, estimate numbers, and write API definitions.
1. Design Netflix (Focus on CDN, Video streaming, and personalized recommendations).
2. Design Uber (Focus on geospatial indexing, quadtrees, and real-time location tracking).
3. Design a Rate Limiter (Focus on algorithms like Token Bucket, Leaky Bucket, Sliding Window, and Redis integration).
4. Design Web Crawler (Focus on BFS, DNS resolution bottlenecks, deduplication using Bloom Filters).
5. Design Ticketmaster (Focus on handling extreme concurrency, distributed locking, and avoiding double-booking).
"""

with open(file_path, "w", encoding="utf-8") as f:
    f.write(md_content)

print("Massive markdown string successfully written.")
