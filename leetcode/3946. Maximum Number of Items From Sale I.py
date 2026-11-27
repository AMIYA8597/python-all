3946. Maximum Number of Items From Sale I


You are given a 2D integer array items, where items[i] = [factori, pricei] represents the ith item. You are also given an integer budget.

There are unlimited copies of each item available for purchase.You may buy any number of copies of any items such that the total cost of the purchased copies is at most budget.

After buying items, you may receive free copies according to the following rules:

For each item i that you bought at least one copy of, you receive one free copy of every item j such that j != i and factori divides factorj.
Buying multiple copies of the same item i does not give additional free copies through item i.
The same item j can be received multiple times for free if it is received from purchases of different item types.
Return the maximum total number of item copies you can obtain, including both purchased copies and free copies, while spending at most budget on purchased items.

 

Example 1:

Input: items = [[6,2],[2,6],[3,4]], budget = 9

Output: 4

Explanation:

You can buy 2 copies of item 0 and 1 copy of item 2 for a total cost of 2 * 2 + 4 = 8, which is not greater than budget = 9.
Buying item 2 gives 1 free copy of item 0, because factor2 = 3 divides factor0 = 6.
You leave with 3 purchased copies and 1 free copy, for a total of 4 item copies.
Example 2:

Input: items = [[2,4],[3,2],[4,1],[6,4],[12,4]], budget = 8

Output: 10

Explanation:

You can buy 1 copy of item 0, 1 copy of item 1, and 2 copies of item 2 for a total cost of 4 + 2 + 2 * 1 = 8.
Buying item 0 gives 1 free copy of items 2, 3, and 4.
Buying item 1 gives 1 free copy of items 3 and 4.
Buying item 2 gives 1 free copy of item 4.
Thus, you receive 6 free copies. You leave with 4 purchased copies and 6 free copies, for a total of 10 item copies.
 

Constraints:

1 <= items.length <= 1000
items[i] = [factori, pricei]
1 <= factori, pricei <= 1500
1 <= budget <= 1500


























  class Solution:
    def maximumSaleItems(self, items: list[list[int]], budget: int) -> int:
        n = len(items)

        # Calculate free-copy bonus for each item
        bonus = [0] * n

        for i in range(n):
            for j in range(n):
                if i != j and items[j][0] % items[i][0] == 0:
                    bonus[i] += 1

        # dp[b] = maximum items obtainable with spending at most b
        dp = [0] * (budget + 1)

        for i in range(n):
            factor, price = items[i]

            # Activate this item type (buy the first copy)
            active = [-1] * (budget + 1)

            for b in range(price, budget + 1):
                active[b] = dp[b - price] + 1 + bonus[i]

            # Buy additional copies after activation
            for b in range(price, budget + 1):
                if active[b - price] != -1:
                    active[b] = max(active[b], active[b - price] + 1)

            # Update DP: skip this item or purchase it
            for b in range(budget + 1):
                dp[b] = max(dp[b], active[b])

        return dp[budget]




















                  # https://www.youtube.com/@0x3f
class Solution:
    def maximumSaleItems(self, items: list[list[int]], budget: int) -> int:
        max_factor = max(p[0] for p in items)
        cnt_factor = [0] * (max_factor + 1)
        for factor, _ in items:
            cnt_factor[factor] += 1

        cnt_multi = [0] * (max_factor + 1)
        f = [0] * (budget + 1)
        min_price = inf
        sum_price = 0

        for factor, price in items:
            min_price = min(min_price, price)

            if cnt_multi[factor] == 0:
                for j in range(factor, max_factor + 1, factor):
                    cnt_multi[factor] += cnt_factor[j]
            cnt = cnt_multi[factor]

            sum_price = min(sum_price + price, budget)
            for j in range(sum_price, price - 1, -1):
                v = f[j - price] + cnt
                if v > f[j]: f[j] = v

        return max(fi + (budget - i) // min_price for i, fi in enumerate(f))

























from typing import List

class Solution:
    def maximumSaleItems(self, items: List[List[int]], budget: int) -> int:
        max_f = max(f for f, _ in items)
        freq = [0] * (max_f + 1)
        for f, _ in items:
            freq[f] += 1
            
        # total_multiples[f] = count of items j where f divides factor_j (includes i itself)
        total_multiples = [0] * (max_f + 1)
        for f in range(1, max_f + 1):
            if freq[f]:
                for mult in range(f, max_f + 1, f):
                    total_multiples[f] += freq[mult]
                    
        # 0/1 Knapsack for buying at most 1 copy of each item type
        dp = [-1] * (budget + 1)
        dp[0] = 0
        min_price = float('inf')
        
        for f, price in items:
            if price < min_price:
                min_price = price
            gain = total_multiples[f]
            for c in range(budget, price - 1, -1):
                if dp[c - price] != -1 and dp[c - price] + gain > dp[c]:
                    dp[c] = dp[c - price] + gain
                    
        # Spend any leftover budget on the single cheapest item
        ans = 0
        for c in range(budget + 1):
            if dp[c] != -1:
                ans = max(ans, dp[c] + (budget - c) // min_price)
                
        return ans




















class Solution:
    def maximumSaleItems(self, items: List[List[int]], budget: int) -> int:
        n=len(items)
        maxi=0
        mini=float('inf')
        for i in items:
            maxi=maxi if maxi>i[0] else i[0]
            mini=mini if mini<i[1] else i[1]
        count=[0]*(maxi+1)
        for i in items:
            count[i[0]]+=1
        val=[0]*n
        for i in range(n):
            f=items[i][0]
            total=0
            for j in range(f,maxi+1,f):
                total+=count[j]
            val[i]=total
        dp=[-1]*(budget+1)
        dp[0]=0
        for i in range(n):
            cost=items[i][1]
            value=val[i]
            for j in range(budget,cost-1,-1):
                if dp[j-cost]!=-1:
                    dp[j]=max(dp[j],dp[j-cost]+value)
        maxtotal=0
        for i in range(budget+1):
            if dp[i]!=-1:
                extra=(budget-i)//mini
                maxtotal=max(maxtotal,dp[i]+extra)
        return maxtotal
