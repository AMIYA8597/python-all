# Master FAANG Interview Checklist and Cheat Sheet

## 1. Introduction & The FAANG Mindset
Interviewing at top-tier tech companies (FAANG: Facebook/Meta, Amazon, Apple, Netflix, Google) requires more than just knowing how to code. It requires a holistic understanding of computer science fundamentals, scalable systems, and effective communication. This document serves as a textbook-depth reference guide, designed to be your ultimate cheat sheet and checklist for technical and behavioral interviews.

### The Philosophy
FAANG companies optimize for hiring false negatives over false positives. This means they would rather reject a good candidate than hire a bad one. To succeed, you must demonstrate strong problem-solving skills, code fluency, architectural intuition, and cultural fit.
- **Communicate constantly:** Your thought process is more important than the final solution. The interviewer wants to know *how* you think, not just *what* you know.
- **Clarify before coding:** Never assume requirements. Always ask clarifying questions. What are the constraints? Are there negative numbers? Does the data fit in memory? What is the expected scale?
- **Optimize incrementally:** Start with a brute-force solution to get a baseline. Do not prematurely optimize. Once you have a working baseline, systematically apply data structure patterns to optimize time and space complexity.
- **Test rigorously:** Manually trace your code with edge cases (empty inputs, extremely large inputs, negative numbers, single elements) before declaring it finished.

---

## 2. Behavioral Interviews: The STAR Method & Leadership Principles
Behavioral interviews assess your past behavior as a predictor of future performance. They are heavily weighted, especially at companies like Amazon (where Leadership Principles are the core of the interview).

### The STAR Methodology
Structure every answer using the STAR format. Keep it concise (2-3 minutes per answer). Practice delivering these stories out loud.
- **Situation (10%):** Set the context. What was the project, who were the stakeholders, and what were the constraints? Provide enough detail so the interviewer understands the stakes, but do not bog them down in irrelevant technical jargon.
- **Task (10%):** What was your specific responsibility? What goal were you trying to achieve? 
- **Action (60%):** This is the most critical part. What steps did *you* take to solve the problem? Use "I", not "we". Detail your technical and non-technical contributions. Emphasize your decision-making process, trade-offs considered, and how you demonstrated leadership. 
- **Result (20%):** What was the outcome? Use quantifiable metrics (e.g., "reduced latency by 40%", "generated $1M in revenue", "saved 20 hours of manual work per week"). What did you learn from this experience?

### Common Behavioral Archetypes to Prepare
Create a "Story Matrix": write down 5-7 robust stories from your past experience. Each story should be adaptable to multiple archetypes.
1. **Navigating Ambiguity:** A time you had to design a system with vague requirements or pivot based on changing business needs.
2. **Conflict Resolution:** A time you disagreed with a coworker or manager about a technical decision. Focus on how you used data to drive the decision and maintained a positive relationship.
3. **Overcoming Failure:** A project that failed, a bug you introduced that brought down production, or a missed deadline. Focus on the post-mortem: how did you fix it, and what systemic changes did you implement to prevent it from happening again?
4. **Leadership & Influence:** A time you led a team, mentored a junior engineer, or convinced others to adopt a new technology or process without having direct authority over them.
5. **Customer Obsession:** A time you went above and beyond for a customer, or pushed back on a feature because it would degrade the user experience.

---

## 3. System Design Interviews: Core Principles & Architecture
System design interviews evaluate your ability to architect scalable, reliable, and maintainable systems. You are not expected to build a perfect system, but rather to discuss trade-offs intelligently.

### The 5-Step Framework (RADICAL)
1. **Requirements & Goals (5 mins):** 
   - *Functional:* What are the core features? (e.g., "Users can upload videos, users can view videos").
   - *Non-Functional:* Scale, availability, latency, consistency requirements. (e.g., "System must be highly available, low latency for video streaming, eventual consistency for view counts is acceptable").
2. **API Design (5 mins):** Define the core endpoints and data contracts. (e.g., `POST /v1/videos`, `GET /v1/videos/{id}`).
3. **Capacity Estimation (5 mins):** Back-of-the-envelope math for storage, bandwidth, and QPS (Queries Per Second). Use round numbers (e.g., 100M Daily Active Users).
4. **High-Level Design (10 mins):** Draw the core components (Client -> Load Balancer -> API Gateway -> Microservices -> Database).
5. **Deep Dive & Bottlenecks (20 mins):** Discuss trade-offs, scaling strategies, caching, database sharding, and failure scenarios.

### Core Concepts

#### 1. Scalability: Vertical vs. Horizontal
- **Vertical Scaling (Scale Up):** Adding more power (CPU, RAM, Disk) to an existing machine. It is simple but has a hard hardware limit and introduces a single point of failure.
- **Horizontal Scaling (Scale Out):** Adding more machines to a pool of resources. Requires stateless applications and distributed coordination, but offers theoretically infinite scale and fault tolerance.

#### 2. The CAP Theorem & PACELC
In a distributed data store, you can only guarantee two of three:
- **Consistency (C):** Every read receives the most recent write or an error.
- **Availability (A):** Every request receives a non-error response, without the guarantee that it contains the most recent write.
- **Partition Tolerance (P):** The system continues to operate despite an arbitrary number of messages being dropped or delayed by the network.
- *In reality, partitions (P) are unavoidable, so you must choose between C and A.*
- **PACELC Theorem:** Extends CAP. In case of partition (P), choose A or C. Else (E), when the system is running normally, choose between Latency (L) and Consistency (C).

#### 3. Load Balancing
Distributes incoming network traffic across a group of backend servers to ensure no single server bears too much demand.
- **Algorithms:** Round Robin, Least Connections, IP Hash, Consistent Hashing.
- **Layer 4 vs. Layer 7:** L4 (Transport Layer) routes based on IP/Port. Extremely fast. L7 (Application Layer) routes based on HTTP headers, URLs, or cookies. Slower but allows smarter routing.

#### 4. Caching
Stores copies of frequently accessed data in memory to reduce latency and database load.
- **Strategies:** 
  - *Cache-Aside:* Application checks cache; if miss, fetches from DB and updates cache.
  - *Write-Through:* Data is written to cache and DB simultaneously.
  - *Write-Back (Write-Behind):* Data is written to cache only; asynchronously synced to DB.
- **Eviction Policies:** LRU (Least Recently Used), LFU (Least Frequently Used), FIFO.
- **Technologies:** Redis (single-threaded, supports complex data structures), Memcached (multi-threaded, simple key-value).

#### 5. Content Delivery Networks (CDNs)
Geographically distributed network of proxy servers to deliver static content (HTML, CSS, JS, images, videos) closer to the user, significantly reducing latency and offloading traffic from origin servers.

#### 6. Microservices vs. Monoliths
- **Monolith:** Single codebase, tightly coupled. Easy to develop and deploy initially, but hard to scale, slow to build, and a single bug can crash the entire system.
- **Microservices:** Independently deployable services communicating via network (REST, gRPC, Message Queues). Allows independent scaling and technology choices, but introduces complexity in deployment, networking, and distributed data consistency (requires sagas/two-phase commits).

#### 7. Database Design: Relational vs. NoSQL
- **Relational (SQL):** MySQL, PostgreSQL. Follows ACID properties (Atomicity, Consistency, Isolation, Durability). Best for structured data, complex joins, and strict consistency (e.g., financial transactions).
- **NoSQL:** Relaxes ACID for better scalability and performance.
  - *Key-Value:* DynamoDB, Redis. Fast reads/writes.
  - *Document:* MongoDB, CouchDB. Flexible schema, JSON-like data. Great for product catalogs or user profiles.
  - *Wide-Column:* Cassandra, HBase. Optimized for massive datasets, time-series data, high write throughput.
  - *Graph:* Neo4j. Optimized for navigating relationships and interconnected data (social networks, recommendation engines).

#### 8. Database Scaling (Sharding & Replication)
- **Replication:** Master-Slave (read replicas for scaling reads) or Master-Master (scaling writes, but complex conflict resolution).
- **Sharding (Data Partitioning):** Distributing data across multiple independent databases to scale writes and storage.
  - *Partitioning Criteria:* Range-based, Hash-based (uses Consistent Hashing to minimize data movement when adding/removing nodes).
  - *Challenges:* Joins across shards are slow/impossible, non-uniform data distribution (the "celebrity problem" where one shard gets all the traffic).

#### 9. Asynchronous Processing & Message Queues
Decouples heavy processing from the critical path to improve API response times and provide fault tolerance.
- **Technologies:** Kafka (high-throughput, distributed commit log, replayable), RabbitMQ (flexible routing, AMQP, volatile).
- **Use Cases:** Sending email notifications, processing uploaded videos, analytics pipelines.

---

## 4. Data Structures & Algorithms: Pattern Recognition
FAANG interviews rely heavily on algorithmic problem-solving. Memorizing solutions is ineffective; instead, master these underlying patterns to recognize how to approach unseen problems.

### Pattern 1: Sliding Window
Used for arrays or strings when finding a contiguous subarray or substring that satisfies a specific condition.
- **Indicators:** "Maximum sum subarray of size K", "Longest substring with K distinct characters", "String anagrams".
- **Mechanism:** Maintain a window defined by two pointers (`left`, `right`). Expand `right` to include elements, and shrink `left` when the condition is violated to find the optimal window.
- **Time Complexity:** O(N) because each element is processed at most twice.

### Pattern 2: Two Pointers
Used for sorted arrays or linked lists to find pairs, triplets, or subarrays.
- **Indicators:** "Target sum", "Remove duplicates in-place", "Squaring a sorted array", "Dutch national flag problem".
- **Mechanism:** Use two pointers, often starting at opposite ends (for sorted arrays) or adjacent to each other, moving towards a condition based on comparisons.

### Pattern 3: Fast & Slow Pointers (Hare & Tortoise)
Used in linked lists or arrays to detect cycles or find specific structural elements.
- **Indicators:** "Linked list cycle", "Middle of linked list", "Palindrome linked list", "Happy number".
- **Mechanism:** Two pointers moving at different speeds (e.g., slow moves 1 step, fast moves 2 steps). If there is a cycle, they will eventually meet. If the fast pointer reaches the end, there is no cycle, and the slow pointer is at the midpoint.

### Pattern 4: Merge Intervals
Used for problems involving overlapping intervals or scheduling.
- **Indicators:** "Merge overlapping intervals", "Insert interval", "Meeting rooms (minimum rooms required)", "Employee free time".
- **Mechanism:** Sort intervals based on their start time. Iterate through the intervals and merge them if the current interval's start time is less than or equal to the previous interval's end time.

### Pattern 5: Cyclic Sort
Used when dealing with an array of numbers in a given range (e.g., 1 to N).
- **Indicators:** "Find the missing number", "Find all duplicate numbers", "Find the smallest missing positive integer".
- **Mechanism:** Iterate through the array. Swap the current number to its correct index (i.e., the number `nums[i]` should be placed at index `nums[i] - 1`). Then, do a second pass to find elements out of place.

### Pattern 6: In-place Reversal of a LinkedList
- **Indicators:** "Reverse linked list", "Reverse a sub-list", "Reverse every K-element sub-list".
- **Mechanism:** Maintain `prev`, `current`, and `next` pointers. Iteratively reverse the links in place without using extra memory. Careful manipulation of pointers is critical to avoid losing the rest of the list.

### Pattern 7: Tree Breadth-First Search (BFS)
Used for level-order traversal of trees or finding shortest paths in unweighted graphs.
- **Indicators:** "Level order traversal", "Minimum depth of a binary tree", "Connect level order siblings", "Right view of a binary tree".
- **Mechanism:** Use a Queue (e.g., `collections.deque` in Python). Track the number of nodes at the current level (using the queue size) to process the tree level by level.

### Pattern 8: Tree Depth-First Search (DFS)
Used for traversing paths from root to leaf, exploring graphs comprehensively, or topological sorting.
- **Indicators:** "Path sum", "All paths for a sum", "Lowest common ancestor", "Count paths for a sum".
- **Mechanism:** Use Recursion (implicit stack) or an explicit Stack. Keep track of the current path and path sum. Backtrack by removing the current node from the path when returning from recursion.

### Pattern 9: Two Heaps
Used for finding median or percentile values in a dynamic, streaming dataset.
- **Indicators:** "Find median of a number stream", "Sliding window median", "Maximize capital".
- **Mechanism:** Maintain a Max-Heap for the smaller half of the numbers and a Min-Heap for the larger half. Rebalance the heaps after every insertion so their sizes differ by at most 1, keeping the median readily accessible at the top of the heaps.

### Pattern 10: Subsets (Combinatorial Search)
Used for finding all combinations, permutations, or subsets of a given set of elements.
- **Indicators:** "Subsets", "Permutations", "Combinations", "Generate valid parentheses", "Letter combinations of a phone number".
- **Mechanism:** Use Backtracking (a form of DFS). Make a choice, recursively explore that choice, and then undo the choice (backtrack) to explore other options.

### Pattern 11: Modified Binary Search
Used for searching in sorted arrays, rotated sorted arrays, or matrices.
- **Indicators:** "Search in rotated sorted array", "Find peak element", "Next letter", "Number range".
- **Mechanism:** Identify which half of the array is sorted. Adjust `low` and `high` pointers based on whether the target falls into the sorted half's range.

### Pattern 12: Top 'K' Elements
Used for finding the largest, smallest, or most frequent K elements in an array or stream.
- **Indicators:** "Top K frequent elements", "Kth largest element in a stream", "K closest points to origin".
- **Mechanism:** Use a Min-Heap (to find top K largest) or Max-Heap (to find top K smallest) of size K. Iterate through the elements, pushing to the heap. If the heap size exceeds K, pop the element. This reduces time complexity from O(N log N) sorting to O(N log K).

### Pattern 13: K-way Merge
Used to merge K sorted arrays or linked lists.
- **Indicators:** "Merge K sorted lists", "Kth smallest number in M sorted lists".
- **Mechanism:** Push the first element of each array/list into a Min-Heap. Pop the smallest element, add it to the result, and push the next element from the same array/list into the heap.

### Pattern 14: Topological Sort
Used for finding a valid ordering of elements with dependencies, typically modeled as Directed Acyclic Graphs (DAGs).
- **Indicators:** "Course schedule (prerequisites)", "Task scheduling", "Alien dictionary".
- **Mechanism:** 
  1. Calculate in-degrees (number of incoming edges) for all vertices.
  2. Push all vertices with 0 in-degree to a Queue.
  3. Dequeue a vertex, add it to the sorted order, and decrement the in-degree of its neighbors.
  4. If a neighbor's in-degree becomes 0, enqueue it.
  5. If the sorted order doesn't contain all vertices, there is a cycle.

---

## 5. Dynamic Programming (DP) Mastery
Dynamic Programming solves optimization problems by breaking them down into overlapping subproblems and caching the results (memoization for top-down, tabulation for bottom-up). 

### Common DP Categories
1. **0/1 Knapsack:**
   - *Problem:* Maximize value with limited capacity. Each item is chosen 0 or 1 time.
   - *Variants:* Subset Sum (can we partition array to a target sum?), Equal Subset Sum Partition, Count of Subset Sum.
2. **Unbounded Knapsack:**
   - *Problem:* Infinite quantities of items available.
   - *Variants:* Rod Cutting, Coin Change (minimum coins to make amount, maximum ways to make amount).
3. **Fibonacci Numbers:**
   - *Problem:* Current state depends on a few previous states.
   - *Variants:* Climbing Stairs, House Robber, Minimum jumps to reach end.
4. **Palindromic Subsequence:**
   - *Problem:* Find properties of palindromes within strings.
   - *Variants:* Longest Palindromic Subsequence, Longest Palindromic Substring, Minimum deletions to make a string a palindrome.
5. **Longest Common Substring/Subsequence:**
   - *Problem:* Compare two strings to find commonalities.
   - *Variants:* Edit Distance (Levenshtein distance), String Interleaving, Subsequence Pattern Matching.

---

## 6. Rapid Algorithms Reference

### Sorting Algorithms
- **Merge Sort:** Divide and conquer. Stable sort. `O(N log N)` time, `O(N)` space. Good for linked lists.
- **Quick Sort:** Partition around a pivot. Unstable sort. Expected `O(N log N)` time, worst `O(N^2)` (if poor pivot). `O(log N)` space for recursion stack.
- **Heap Sort:** Build max heap, extract max repeatedly. In-place, unstable. `O(N log N)` time, `O(1)` space.
- **Counting Sort/Radix Sort:** Non-comparison sorts. `O(N + K)` time, where K is the range of numbers. Only applicable for integers with a limited range.

### Graph Algorithms
- **Dijkstra's Algorithm:** Shortest path from a single source in a weighted graph (no negative weights). Uses a priority queue. Time: `O((V + E) log V)`.
- **Bellman-Ford:** Shortest path from a single source handling negative weights. Can detect negative weight cycles. Time: `O(V * E)`.
- **Floyd-Warshall:** All-pairs shortest path. Dynamic programming based. Time: `O(V^3)`.
- **Kruskal's Algorithm:** Minimum Spanning Tree (MST). Sorts edges and uses a Disjoint Set (Union-Find) to avoid cycles. Time: `O(E log E)`.
- **Prim's Algorithm:** Minimum Spanning Tree (MST). Builds the tree node by node using a priority queue. Time: `O((V + E) log V)`.
- **Tarjan's Algorithm:** Finding Strongly Connected Components (SCCs) in directed graphs, bridges, and articulation points using a single DFS pass. Time: `O(V + E)`.

### String Algorithms
- **Trie (Prefix Tree):** Extremely efficient for prefix search, autocomplete, and spell checkers. A tree where each node contains a character, a map to children nodes, and a boolean `is_end_of_word` flag. Time for insert/search: `O(L)` where L is word length.
- **KMP (Knuth-Morris-Pratt):** Substring search in `O(N + M)`. Builds an LPS (Longest Prefix Suffix) array to avoid redundant comparisons when a mismatch occurs.
- **Rabin-Karp:** Substring search using a rolling hash. Average Time: `O(N + M)`, Worst: `O(N * M)` if high hash collisions.

### Advanced Data Structures
- **Disjoint Set (Union-Find):** Manages disjoint sets. Supports `find` (with path compression) and `union` (by rank/size). Achieves near `O(1)` operations (Inverse Ackermann function). Heavily used for cycle detection in undirected graphs and Kruskal's MST.
- **Segment Tree / Fenwick Tree (Binary Indexed Tree):** Efficient for range queries (sum, min, max) and point updates in array in `O(log N)` time.
- **Bloom Filter:** Space-efficient probabilistic data structure. Answers "Is element in set?". Returns "Possibly in set" or "Definitely not in set". There are no false negatives, but possible false positives.

---

## 7. Python-Specific Interview Cheat Sheet
Python is universally accepted and highly recommended for interviews due to its concise syntax, readability, and rich standard library.

### Core Libraries to Know
- `collections.deque`: Double-ended queue, perfect for BFS and Sliding Window. `append()`, `appendleft()`, `pop()`, `popleft()` are all `O(1)`. Standard lists take `O(N)` for `pop(0)`.
- `collections.defaultdict`: Dictionary that initializes missing keys automatically. Avoids `KeyError`. Examples: `defaultdict(int)`, `defaultdict(list)`.
- `collections.Counter`: Automatically counts element frequencies. `Counter(arr)` returns a dict-like object mapping elements to counts. Supports `.most_common(k)`.
- `heapq`: Min-heap implementation built-in. `heapq.heapify(arr)` (runs in `O(N)`), `heapq.heappush(heap, val)`, `heapq.heappop(heap)`. *Note: For a max-heap, multiply values by -1 before pushing, and multiply by -1 again after popping.*
- `bisect`: Binary search built-in. `bisect_left(arr, val)` (finds first insertion point), `bisect_right(arr, val)` (finds last insertion point).
- `math`: `math.inf`, `-math.inf` (for initializing max/min values), `math.gcd(a, b)`, `math.ceil()`, `math.floor()`.
- `itertools`: `itertools.permutations(arr, r)`, `itertools.combinations(arr, r)`. Great for brute-forcing combinations if required.
- `functools.lru_cache` (or `@cache` in Python 3.9+): Decorator for automatic DP memoization. Just add `@cache` above your recursive function.

### Essential Python Syntax & Tricks
- **Reversing an array/string:** `arr[::-1]`
- **Sorting with a custom key:** `arr.sort(key=lambda x: (x[1], -x[0]))` (Sorts primarily by index 1 ascending, secondarily by index 0 descending).
- **String formatting:** f-strings are cleanest: `f"The value is {val}"`
- **Iteration with index:** `for i, val in enumerate(arr):`
- **Parallel iteration:** `for a, b in zip(list1, list2):`
- **List Comprehensions:** `[x*2 for x in arr if x % 2 == 0]`
- **Matrix Initialization:** `matrix = [[0] * cols for _ in range(rows)]` *(Never use `[[0]*cols]*rows` as it creates shallow copies of the rows!)*
- **Checking empty structures:** `if not my_list:` (Pythonic way to check if list/dict/string is empty).

---

## 8. Pre-Interview Master Checklist

### The Week Before
- [ ] Complete a review of the "Blind 75" or "Grind 169" core patterns.
- [ ] Practice 2-3 mock system design interviews using a whiteboard tool (e.g., Excalidraw, draw.io). Speak out loud.
- [ ] Finalize 5-7 robust STAR behavioral stories. Cross-reference them with the company's core values (e.g., Amazon Leadership Principles, Google's "Googliness").
- [ ] Test your coding environment. Ensure your camera, microphone, and internet connection are stable. Check if the company uses a specific platform (HackerRank, CoderPad) and familiarize yourself with its UI and shortcuts.

### The Day Before
- [ ] Do a light review of this cheat sheet. **Do not cram** new complex algorithms. If you don't know it by now, it's better to rest.
- [ ] Prepare 3-5 thoughtful questions for your interviewers. Good questions show genuine interest (e.g., "What is the most challenging technical problem your team is facing right now?", "How does the engineering team handle technical debt?").
- [ ] Layout your clothes. Get 8 hours of sleep. Hydrate properly.

### 1 Hour Before
- [ ] Do a "warm-up" easy coding problem (e.g., Two Sum or Reverse Linked List). The goal is not to learn, but to get your fingers typing and your brain into "code mode."
- [ ] Review your STAR stories and leadership principles one last time.
- [ ] Set up your physical space: have a glass of water, a blank notepad, and a pen ready. Close all unnecessary tabs on your computer to avoid distractions and free up memory.
- [ ] Take deep breaths. The interviewers want you to succeed. Trust your training, communicate clearly, and you will do great.

---
*End of Master FAANG Interview Checklist and Cheat Sheet.*
