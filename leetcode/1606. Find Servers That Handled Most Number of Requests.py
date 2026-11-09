1606. Find Servers That Handled Most Number of Requests



You have k servers numbered from 0 to k-1 that are being used to handle multiple requests simultaneously. Each server has infinite computational capacity but cannot handle more than one request at a time. The requests are assigned to servers according to a specific algorithm:

The ith (0-indexed) request arrives.
If all servers are busy, the request is dropped (not handled at all).
If the (i % k)th server is available, assign the request to that server.
Otherwise, assign the request to the next available server (wrapping around the list of servers and starting from 0 if necessary). For example, if the ith server is busy, try to assign the request to the (i+1)th server, then the (i+2)th server, and so on.
You are given a strictly increasing array arrival of positive integers, where arrival[i] represents the arrival time of the ith request, and another array load, where load[i] represents the load of the ith request (the time it takes to complete). Your goal is to find the busiest server(s). A server is considered busiest if it handled the most number of requests successfully among all the servers.

Return a list containing the IDs (0-indexed) of the busiest server(s). You may return the IDs in any order.

 

Example 1:


Input: k = 3, arrival = [1,2,3,4,5], load = [5,2,3,3,3] 
Output: [1] 
Explanation: 
All of the servers start out available.
The first 3 requests are handled by the first 3 servers in order.
Request 3 comes in. Server 0 is busy, so it's assigned to the next available server, which is 1.
Request 4 comes in. It cannot be handled since all servers are busy, so it is dropped.
Servers 0 and 2 handled one request each, while server 1 handled two requests. Hence server 1 is the busiest server.
Example 2:

Input: k = 3, arrival = [1,2,3,4], load = [1,2,1,2]
Output: [0]
Explanation: 
The first 3 requests are handled by first 3 servers.
Request 3 comes in. It is handled by server 0 since the server is available.
Server 0 handled two requests, while servers 1 and 2 handled one request each. Hence server 0 is the busiest server.
Example 3:

Input: k = 3, arrival = [1,2,3], load = [10,12,11]
Output: [0,1,2]
Explanation: Each server handles a single request, so they are all considered the busiest.
 

Constraints:

1 <= k <= 105
1 <= arrival.length, load.length <= 105
arrival.length == load.length
1 <= arrival[i], load[i] <= 109
arrival is strictly increasing.


























from typing import List
import heapq
from bisect import bisect_left

class Solution:
    def busiestServers(self, k: int, arrival: List[int], load: List[int]) -> List[int]:

        available = list(range(k))
        busy = []
        count = [0] * k

        for i in range(len(arrival)):

            # Release servers whose requests have completed
            while busy and busy[0][0] <= arrival[i]:
                end_time, server = heapq.heappop(busy)

                # Insert server back into sorted available list
                pos = bisect_left(available, server)
                available.insert(pos, server)

            # If all servers are busy, drop the request
            if not available:
                continue

            # Find the first available server >= i % k
            start = i % k
            pos = bisect_left(available, start)

            # Wrap around if necessary
            if pos == len(available):
                pos = 0

            server = available.pop(pos)

            # Assign request
            count[server] += 1
            heapq.heappush(busy, (arrival[i] + load[i], server))

        # Find maximum number of handled requests
        max_count = max(count)

        return [i for i in range(k) if count[i] == max_count]


















class Solution:
    def busiestServers(self, k: int, arrival: list[int], load: list[int]) -> list[int]:
        num_processed = [0] * k
        busy = [] # (time, server)
        available = [i for i in range(k)]

        for i in range(len(arrival)):
            # pop all values that end before the start time for this idx
            while busy:
                if busy[0][0] <= arrival[i]:
                    time, server = heapq.heappop(busy)
                    # add to available
                    heapq.heappush(available, (i + ((server - i) % k)))
                else:
                    break
            
            # get the next available server for this operation, figure out finished time, add to busy, and add one to num_processed
            if not available:
                continue
            virtual_server = heapq.heappop(available)
            next_server = virtual_server % k
            num_processed[next_server] += 1
            heapq.heappush(busy, (arrival[i] + load[i], next_server))
        
        # get the max value in num_processed
        max_reqs = max(num_processed)
        output = []
        for i in range(k):
            if num_processed[i] == max_reqs:
                output.append(i)
        
        return output




        


















class Solution:
    def busiestServers(self, k: int, arrival: list[int], load: list[int]) -> list[int]:
        available = list(range(k))
        heapq.heapify(available)

        busy = []
        count = [0] * k

        for i, start in enumerate(arrival):

            # Release completed servers
            while busy and busy[0][0] <= start:
                end_time, server = heapq.heappop(busy)

                virtual = i + (server - i) % k
                heapq.heappush(available, virtual)

            # Assign the next available server
            if available:
                server = heapq.heappop(available) % k

                heapq.heappush(busy, (start + load[i], server))
                count[server] += 1

        maximum = max(count)

        return [i for i in range(k) if count[i] == maximum]






















class Solution:
    def busiestServers(
        self, k: int, arrival: list[int], load: list[int]
    ) -> list[int]:
        available = list(range(k))  # Already a valid min-heap
        busy = []                  # (finish_time, server)
        counts = [0] * k

        for i, (a, l) in enumerate(zip(arrival, load)):
            # Release servers BEFORE checking availability.
            while busy and busy[0][0] <= a:
                _, server = heapq.heappop(busy)

                # Position of this server in the circular search from i.
                virtual_index = i + (server - i) % k
                heapq.heappush(available, virtual_index)

            if not available:
                continue

            server = heapq.heappop(available) % k
            counts[server] += 1
            heapq.heappush(busy, (a + l, server))

        max_val = max(counts)
        return [
            server
            for server, count in enumerate(counts)
            if count == max_val
        ]




