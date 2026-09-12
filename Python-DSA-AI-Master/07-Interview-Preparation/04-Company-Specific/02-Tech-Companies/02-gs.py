"""
Goldman Sachs Specific Interview Preparation Module.

Learning Objectives:
- Master string parsing and mathematical array problems frequently asked at Goldman Sachs.
- Understand run-length encoding and hashing for anagrams.
- Implement optimal solutions for Trapping Rain Water and fractional/integer problems.

Concept Explanation:
Goldman Sachs often asks array manipulation, hashing, and math-heavy programming questions. High Five, Group Anagrams, and Trapping Rain Water are classic representations. Code needs to be efficient as problem sizes can be large.
"""
from typing import List, Dict
import collections

# Basic Implementation: Group Anagrams
def group_anagrams(strs: List[str]) -> List[List[str]]:
    """
    Basic level: Group Anagrams.
    Categorize strings by their sorted version as a key.
    """
    ans: Dict[tuple, List[str]] = collections.defaultdict(list)
    for s in strs:
        count = [0] * 26
        for c in s:
            count[ord(c) - ord('a')] += 1
        ans[tuple(count)].append(s)
    return list(ans.values())

# Intermediate Implementation: High Five
def high_five(items: List[List[int]]) -> List[List[int]]:
    """
    Intermediate level: High Five.
    Given student ID and scores, calculate top 5 average for each student.
    """
    scores = collections.defaultdict(list)
    for sid, score in items:
        scores[sid].append(score)
        
    result = []
    for sid in sorted(scores.keys()):
        top_five = sorted(scores[sid], reverse=True)[:5]
        avg = sum(top_five) // len(top_five)
        result.append([sid, avg])
    return result

# Advanced Implementation: Trapping Rain Water
def trap(height: List[int]) -> int:
    """
    Advanced level: Trapping Rain Water using two pointers.
    
    Performance Analysis:
    - Time Complexity: O(N) where N is length of height array. Single pass.
    - Space Complexity: O(1) auxiliary space.
    """
    if not height:
        return 0
        
    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    water = 0
    
    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            water += left_max - height[left]
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water += right_max - height[right]
            
    return water

def run_tests():
    print("Testing Group Anagrams...")
    strs = ["eat","tea","tan","ate","nat","bat"]
    res = group_anagrams(strs)
    assert len(res) == 3
    
    print("Testing High Five...")
    items = [[1,91],[1,92],[2,93],[2,97],[1,60],[2,77],[1,65],[1,87],[1,100],[2,100],[2,76]]
    res_high = high_five(items)
    assert res_high[0][1] == 87
    
    print("Testing Trapping Rain Water...")
    heights = [0,1,0,2,1,0,1,3,2,1,2,1]
    assert trap(heights) == 6
    
    print("All tests passed!")

if __name__ == "__main__":
    run_tests()
