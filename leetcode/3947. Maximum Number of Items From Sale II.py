3947. Maximum Number of Items From Sale II


You are given a 2D integer array items, where items[i] = [factori, pricei] represents the ith item. You are also given an integer budget.

There are unlimited copies of each item available for purchase. You may buy any number of copies of any items such that the total cost of the purchased copies is at most budget.

After buying items, you may receive free copies according to the following rules:

Each purchased copy of item i can give you at most one free copy of another item j.
The free item must satisfy i != j and factori divides factorj.
For each ordered pair (i, j), you can receive a free copy of item j from purchases of item i at most once, regardless of how many copies of item i you buy.
The same item j can be received multiple times for free if it is received from purchases of different item types.
Return the maximum total number of item copies you can obtain, including both purchased copies and free copies, while spending at most budget on purchased items.

 

Example 1:

Input: items = [[1,6],[2,4],[3,5]], budget = 19

Output: 5

Explanation:

You can buy 2 copies of item 0 and 1 copy of item 1 for a total cost of 2 * 6 + 4 = 16, which is not greater than budget = 19.
One purchased copy of item 0 gives 1 free copy of item 1, because factor0 = 1 divides factor1 = 2.
The other purchased copy of item 0 gives 1 free copy of item 2, because factor0 = 1 divides factor2 = 3.
You leave with 3 purchased copies and 2 free copies, for a total of 5 item copies.
Example 2:

Input: items = [[2,8],[1,10],[6,6],[4,12],[5,20],[5,17]], budget = 35

Output: 7

Explanation:

You can buy 2 copies of item 0, 1 copy of item 1, and 1 copy of item 2 for a total cost of 2 * 8 + 10 + 6 = 32, which is not greater than budget = 35.
One purchased copy of item 0 gives 1 free copy of item 2, because factor0 = 2 divides factor2 = 6.
The other purchased copy of item 0 gives 1 free copy of item 3, because factor0 = 2 divides factor3 = 4.
The purchased copy of item 1 gives 1 free copy of item 2, because factor1 = 1 divides factor2 = 6.
Buying item 2 gives no free copy, because factor2 = 6 does not divide the factor of any other item.
You leave with 4 purchased copies and 3 free copies, for a total of 7 item copies.
 

Constraints:

1 <= items.length <= 105
items[i] = [factori, pricei]
1 <= factori <= items.length
1 <= pricei <= 109
1 <= budget <= 109
























class Solution:
    def maximumSaleItems(self, items: List[List[int]], budget: int) -> int:
        n = len(items)

        freq = [0] * (n + 1)

        for factor, price in items:
            freq[factor] += 1

        free_count = [0] * (n + 1)

        for factor in range(1, n + 1):

            total = 0

            for multiple in range(factor, n + 1, factor):
                total += freq[multiple]

            free_count[factor] = total - 1

        min_price = min(price for factor, price in items)

        candidates = []

        for factor, price in items:

            count = free_count[factor]

            if count > 0 and price <= 2 * min_price:
                candidates.append((price, count))

        candidates.sort()

        double_count = 0
        remaining = budget

        for price, count in candidates:

            take = min(count, remaining // price)

            double_count += take
            remaining -= take * price

        single_count = remaining // min_price

        return 2 * double_count + single_count























import collections

class Solution(object):
    def maximumSaleItems(self, items, budget):
        """
        :type items: List[List[int]]
        :type budget: int
        :rtype: int
        """
        # Find the max factor to establish our sieve boundaries
        max_factor = max(f for f, _ in items)
        
        # Track the frequencies of each factor
        cnt = [0] * (max_factor + 1)
        min_p = float('inf')
        for f, price in items:
            cnt[f] += 1
            if price < min_p:
                min_p = price
                
        # Sieve: Precalculate how many items have a factor that is a multiple of i
        total_multiples = [0] * len(cnt)
        for i in range(1, len(total_multiples)):
            if not cnt[i]:
                continue
            for j in range(i, len(total_multiples), i):
                total_multiples[i] += cnt[j]
        
        # Group maximum available double-yield items by price
        # Only consider items where price < 2 * min_p
        group = collections.defaultdict(int)
        for f, price in items:
            if price >= 2 * min_p:
                continue
            # The item can give a free copy of any of its multiples (excluding itself)
            group[price] += (total_multiples[f] - 1)
            
        result = 0
        
        # Greedily buy the items that give a free duplicate (2 items per purchase)
        for p in sorted(group):
            if budget < p:
                break
            # We can buy at most what's available or what our budget permits
            copies_to_buy = min(group[p], budget // p)
            result += 2 * copies_to_buy
            budget -= copies_to_buy * p
            
        # Spend any remainder budget on the absolute cheapest items (1 item per purchase)
        result += budget // min_p
        return result
























import collections


# freq table, sort, greedy
class Solution:
    def maximumSaleItems(self, items: List[List[int]], budget: int) -> int:
        NEG_INF = float("-inf")
        cnt = [0]*(max(f for f, _ in items)+1)
        for f, _ in items:
            cnt[f] += 1
        total = [0]*len(cnt)
        for i in range(1, len(total)):
            if not cnt[i]:
                continue
            for j in range(i, len(total), i):
                total[i] += cnt[j]
        min_p = min(p for _, p in items)
        group = collections.defaultdict(int)
        for f, price in items:
            if price >= 2*min_p:
                continue
            group[price] += total[f]-1
        result = 0
        for p in sorted(group):
            c = min(group[p], budget//p)
            result += 2*c
            budget -= c*p
            if not budget:
                break
        result += budget//min_p
        return result






















# https://www.youtube.com/@0x3f
class Solution:
    def maximumSaleItems(self, items: list[list[int]], budget: int) -> int:
        n = len(items)
        cnt_factor = [0] * (n + 1)
        min_price = inf
        for factor, price in items:
            cnt_factor[factor] += 1
            min_price = min(min_price, price)

        cnt_multi = [0] * (n + 1)
        sum_cnt = defaultdict(int)  # price -> 相同 price 的 cnt 之和

        for factor, price in items:
            if price >= min_price * 2:
                continue

            if cnt_multi[factor] == 0:  # 之前没有计算过
                for j in range(factor, n + 1, factor):
                    cnt_multi[factor] += cnt_factor[j]

            cnt = cnt_multi[factor] - 1  # factor 的倍数不包括该物品
            if cnt > 0:
                sum_cnt[price] += cnt

        ans = 0
        for price in sorted(sum_cnt):
            if budget < price:  # 没钱了
                break
            c = min(sum_cnt[price], budget // price)  # 该物品最多买 c 个
            budget -= price * c
            ans += c * 2
        return ans + budget // min_price  # 剩余的钱买最便宜的物品


























from collections import defaultdict

class Solution:
    def maximumSaleItems(
        self, items: list[list[int]], budget: int
    ) -> int:
        max_factor = max(f for f, _ in items)
        cheapest = min(p for _, p in items)

        freq = [0] * (max_factor + 1)
        for factor, _ in items:
            freq[factor] += 1

        multiples = [0] * (max_factor + 1)

        for factor in range(1, max_factor + 1):
            if freq[factor] == 0:
                continue

            for j in range(factor, max_factor + 1, factor):
                multiples[factor] += freq[j]

        offers = defaultdict(int)

        for factor, price in items:
            free_count = multiples[factor] - 1

            if free_count > 0 and price < 2 * cheapest:
                offers[price] += free_count

        ans = 0

        for price in sorted(offers):
            if budget < price:
                break

            count = min(offers[price], budget // price)
            ans += 2 * count
            budget -= price * count

        return ans + budget // cheapest
























class Solution:
    def maximumSaleItems(self, items, budget):
        maximum = max(factor for factor, price in items)
        frequencies = [0] * (maximum + 1)
        cheapest = min(price for factor, price in items)
        for factor, price in items:
            frequencies[factor] += 1
        capacities = {}
        for factor in range(1, maximum + 1):
            if frequencies[factor]:
                capacities[factor] = sum(frequencies[multiple]
                                         for multiple in range(factor, maximum + 1, factor)) - 1
        options = sorted((price, capacities[factor]) for factor, price in items
                         if price < 2 * cheapest and capacities[factor] > 0)
        answer = 0
        for price, capacity in options:
            taken = min(capacity, budget // price)
            answer += 2 * taken
            budget -= price * taken
            if taken < capacity:
                break
        return answer + budget // cheapest
