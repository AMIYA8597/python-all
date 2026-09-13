"""
Bloomberg Specific Interview Preparation Module.

Learning Objectives:
- Master frequent Bloomberg interview problems like Underground System, Ordered Maps, and String manipulations.
- Understand system design concepts for single-machine caching.
- Write robust code handling edge cases typical in financial tech.

Concept Explanation:
Bloomberg interviews heavily focus on practical, system-like data structure design (e.g., Underground System, Browser History, Caching) and string/array manipulation. Problem solving often emphasizes clean, maintainable code over obscure algorithms.
"""
import collections
from typing import Dict, Tuple, List, Optional

# Basic Implementation: Two City Scheduling
def two_city_sched_cost(costs: List[List[int]]) -> int:
    """
    Basic level: Two City Scheduling (Greedy approach).
    Sort by difference in cost sending a person to city A vs city B.
    """
    costs.sort(key=lambda x: x[0] - x[1])
    total_cost = 0
    n = len(costs) // 2
    for i in range(n):
        total_cost += costs[i][0] + costs[i + n][1]
    return total_cost

# Intermediate Implementation: Design Underground System
class UndergroundSystem:
    """
    Intermediate level: Design Underground System.
    """
    def __init__(self):
        self.check_ins: Dict[int, Tuple[str, int]] = {}
        self.journey_data: Dict[Tuple[str, str], Tuple[int, int]] = {}

    def checkIn(self, id: int, stationName: str, t: int) -> None:
        self.check_ins[id] = (stationName, t)

    def checkOut(self, id: int, stationName: str, t: int) -> None:
        start_station, start_time = self.check_ins.pop(id)
        route = (start_station, stationName)
        travel_time = t - start_time
        
        if route in self.journey_data:
            total_time, count = self.journey_data[route]
            self.journey_data[route] = (total_time + travel_time, count + 1)
        else:
            self.journey_data[route] = (travel_time, 1)

    def getAverageTime(self, startStation: str, endStation: str) -> float:
        total_time, count = self.journey_data[(startStation, endStation)]
        return total_time / count

# Advanced Implementation: LFU Cache
class LFUCache:
    """
    Advanced level: LFU (Least Frequently Used) Cache.
    Performance Analysis:
    - Time Complexity: O(1) for get and put.
    - Space Complexity: O(capacity).
    """
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.min_freq = 0
        self.key_to_val_freq = {} 
        self.freq_to_keys = collections.defaultdict(collections.OrderedDict)

    def get(self, key: int) -> int:
        if key not in self.key_to_val_freq:
            return -1
        
        val, freq = self.key_to_val_freq[key]
        del self.freq_to_keys[freq][key]
        if not self.freq_to_keys[freq]:
            if self.min_freq == freq:
                self.min_freq += 1
                
        self.key_to_val_freq[key] = (val, freq + 1)
        self.freq_to_keys[freq + 1][key] = None
        return val

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return
            
        if key in self.key_to_val_freq:
            _, freq = self.key_to_val_freq[key]
            self.key_to_val_freq[key] = (value, freq)
            self.get(key) 
            return
            
        if len(self.key_to_val_freq) >= self.capacity:
            evict_key, _ = self.freq_to_keys[self.min_freq].popitem(last=False)
            del self.key_to_val_freq[evict_key]
            
        self.key_to_val_freq[key] = (value, 1)
        self.freq_to_keys[1][key] = None
        self.min_freq = 1

def run_tests():
    print("Testing Two City Scheduling...")
    costs = [[10,20],[30,200],[400,50],[30,20]]
    assert two_city_sched_cost(costs) == 110, "Basic test failed"
    
    print("Testing Underground System...")
    sys = UndergroundSystem()
    sys.checkIn(45, "Leyton", 3)
    sys.checkIn(32, "Paradise", 8)
    sys.checkOut(45, "Waterloo", 15)
    sys.checkOut(32, "Cambridge", 22)
    assert sys.getAverageTime("Leyton", "Waterloo") == 12.0
    
    print("Testing LFU Cache...")
    lfu = LFUCache(2)
    lfu.put(1, 1)
    lfu.put(2, 2)
    assert lfu.get(1) == 1
    lfu.put(3, 3) 
    assert lfu.get(2) == -1 
    
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
