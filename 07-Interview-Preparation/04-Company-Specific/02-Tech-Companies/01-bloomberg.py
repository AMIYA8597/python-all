"""
# ==============================================================================
# LABORATORY: INTERVIEW PREPARATION (BLOOMBERG PYTHON QUESTIONS)
# ==============================================================================
#
# 1. WHY THIS MATTERS
# -------------------
# Bloomberg interviews are notorious for mimicking real-world Financial Trading 
# Systems. They demand systems that can ingest massive streams of chaotic data, 
# sort it instantly, and return aggregate metrics (like 'Top Traded Stocks' or 
# 'Order Book matching') in strict O(1) or O(log N) time.
#
# A junior engineer uses arrays and constantly calls `list.sort()`. As the stream 
# hits millions of trades per second, the O(N log N) sorting collapses the system.
# 
# A senior engineer deploys compound Data Structures (e.g., Doubly-Linked Lists 
# bound to Hash Maps, or specialized Heaps). They design the "Underground System" 
# or "Browser History" using O(1) state-machine transitions that can handle 
# infinite throughput without breaking a sweat.
#
# 2. LEARNING OBJECTIVES
# ----------------------
# - Master Compound Data Structures (Hash Maps containing Objects/Lists).
# - Master O(1) System Design for real-time streaming data.
# - Understand the architecture of the 'Design Underground System' problem.
#
# ==============================================================================
"""

import collections

def section_header(title: str) -> None:
    print(f"\n{'='*60}\n{title.upper()}\n{'='*60}")


# ==============================================================================
# 3. DESIGN UNDERGROUND SYSTEM (BLOOMBERG FAVORITE)
# ==============================================================================
class UndergroundSystem:
    """
    Simulates a subway system. 
    Customers check in at Station A and check out at Station B.
    We must calculate the AVERAGE travel time between any two stations instantly!
    
    Time: O(1) for ALL operations.
    Space: O(P + S^2) where P is Passengers and S is Stations.
    """
    def __init__(self):
        # Maps the Passenger ID to their Check-In state.
        # Key: int (Passenger ID) -> Value: Tuple(str (Station), int (Time))
        self.check_in_data = {}
        
        # Maps a Route to its total aggregate statistics.
        # Key: Tuple(str (Start), str (End)) -> Value: [Total Time, Trip Count]
        # We MUST store the sum and count to calculate an accurate average mathematically!
        self.journey_data = collections.defaultdict(lambda: [0, 0])

    def checkIn(self, id: int, stationName: str, t: int) -> None:
        """O(1) Time"""
        # We record the exact moment the passenger entered the system!
        self.check_in_data[id] = (stationName, t)
        print(f"  [CHECK IN] Passenger {id} entered '{stationName}' at t={t}")

    def checkOut(self, id: int, stationName: str, t: int) -> None:
        """O(1) Time"""
        # Look up their origin!
        start_station, start_time = self.check_in_data.pop(id)
        
        # Mathematically calculate the duration of the trip
        travel_time = t - start_time
        route_key = (start_station, stationName)
        
        # Update the aggregate database
        self.journey_data[route_key][0] += travel_time
        self.journey_data[route_key][1] += 1
        
        print(f"  [CHECK OUT] Passenger {id} left '{stationName}' at t={t}. Route: {start_station}->{stationName} took {travel_time}s.")

    def getAverageTime(self, startStation: str, endStation: str) -> float:
        """O(1) Time"""
        route_key = (startStation, endStation)
        total_time, trip_count = self.journey_data[route_key]
        
        # Avoid division by zero!
        if trip_count == 0: return 0.0
        
        avg = total_time / trip_count
        print(f"    [QUERY] Average time for {startStation}->{endStation} = {avg:.2f}s")
        return avg

def demonstrate_underground_system():
    section_header("Bloomberg: Design Underground System (O(1))")
    
    subway = UndergroundSystem()
    
    subway.checkIn(45, "Leyton", 3)
    subway.checkIn(32, "Paradise", 8)
    subway.checkIn(27, "Leyton", 10)
    
    subway.checkOut(45, "Waterloo", 15) # Route: Leyton->Waterloo, Time: 12
    subway.checkOut(27, "Waterloo", 20) # Route: Leyton->Waterloo, Time: 10
    subway.checkOut(32, "Cambridge", 22) # Route: Paradise->Cambridge, Time: 14
    
    # Expected: (12 + 10) / 2 = 11.0
    subway.getAverageTime("Leyton", "Waterloo")


# ==============================================================================
# 4. INVALID TRANSACTIONS (STRING PARSING AND RULES)
# ==============================================================================
def invalidTransactions(transactions: list[str]) -> list[str]:
    """
    Time: O(N^2) worst case | Space: O(N)
    A transaction is invalid if:
    1. The amount exceeds $1000.
    2. OR, it occurs within (and including) 60 minutes of another transaction 
       with the SAME NAME in a DIFFERENT CITY.
       
    Format: "name,time,amount,city"
    """
    class Transaction:
        def __init__(self, raw: str):
            self.raw = raw
            parts = raw.split(',')
            self.name = parts[0]
            self.time = int(parts[1])
            self.amount = int(parts[2])
            self.city = parts[3]
            self.is_invalid = False

    print("  Parsing Transactions...")
    txs = [Transaction(raw) for raw in transactions]
    
    # Evaluate every rule
    for i in range(len(txs)):
        # Rule 1: High Amount
        if txs[i].amount > 1000:
            txs[i].is_invalid = True
            
        # Rule 2: Temporal/Geographical Conflict
        # We must check against EVERY OTHER transaction!
        for j in range(len(txs)):
            if i != j:
                if (txs[i].name == txs[j].name and 
                    txs[i].city != txs[j].city and 
                    abs(txs[i].time - txs[j].time) <= 60):
                    
                    txs[i].is_invalid = True
                    break # Already invalid, stop checking others!
                    
    # Reconstruct the raw strings
    invalid_raw = [tx.raw for tx in txs if tx.is_invalid]
    return invalid_raw

def demonstrate_invalid_tx():
    section_header("Bloomberg: Invalid Transactions")
    
    # Alice commits fraud in Beijing and Brooklyn!
    # Bob just spends too much money.
    txs = ["alice,20,800,mtv", "alice,50,100,beijing", "bob,10,1200,mtv", "bob,50,100,beijing"]
    
    print("Incoming Feed:")
    for t in txs: print(f"  {t}")
    
    invalid = invalidTransactions(txs)
    
    print("\nResult: Blocked Transactions:")
    for t in invalid: print(f"  [BLOCKED] {t}")


def run_all_labs():
    demonstrate_underground_system()
    demonstrate_invalid_tx()


# ==============================================================================
# 5. ACTIVE RECALL & INTERVIEW QUESTIONS
# ==============================================================================
"""
ACTIVE RECALL:
1. Interviewer: "In the Underground System, why do we store an array `[Total Time, Trip Count]` for the Route, instead of just continuously recalculating an average and storing a float?"
   Senior Answer: "A running mathematical average cannot be seamlessly updated just by knowing the new value and the old average, unless you also know exactly how many data points contributed to that old average! If the old average was $10$, and the new trip is $20$, you cannot just do $(10+20)/2 = 15$. If the $10$ was the average of $1,000$ trips, the new average is $(10,000 + 20) / 1001 = 10.009$. By storing the raw `Total Time` and the `Trip Count`, we can update both variables linearly in $O(1)$ time, and mathematically generate the exact average dynamically whenever `getAverageTime` is explicitly requested, completely sidestepping floating-point precision corruption."

2. Interviewer: "In the Underground System, why do we physically delete (`self.check_in_data.pop(id)`) the passenger's data upon checkout?"
   Senior Answer: "If we do not explicitly `pop()` or `del` the data from the check-in Hash Map, it becomes a permanent memory leak. Every day, millions of passengers would check in and out, bloating the `check_in_data` dictionary until the server runs out of physical RAM and crashes. By deleting the key upon checkout, we ensure the Hash Map strictly contains ONLY passengers who are *currently physically riding the trains*, capping the $O(P)$ Space Complexity to a safe mathematical bound."

3. Interviewer: "In the Invalid Transactions problem, comparing every transaction to every other transaction requires $O(N^2)$ time. Can we optimize this?"
   Senior Answer: "Yes. An $O(N^2)$ scan will choke on high-frequency trading data. We can optimize it by clustering! We can use a Hash Map where the key is the Person's Name, and the value is a List of their transactions. Furthermore, we can sort that inner list chronologically by Time. When evaluating a transaction, we ONLY look up that specific person's history, and we can use Binary Search ($O(\\log N)$) or a Sliding Window ($O(N)$) to instantly isolate the subset of transactions that fall within the strict 60-minute danger window. This mathematically crushes the time complexity from $O(N^2)$ down to nearly $O(N)$."
"""

if __name__ == "__main__":
    run_all_labs()
    print("\n[SUCCESS] Laboratory: Tech Companies Prep (Bloomberg) Completed.")
