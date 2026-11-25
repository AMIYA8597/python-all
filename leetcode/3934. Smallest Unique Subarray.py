3934. Smallest Unique Subarray


You are given an integer array nums.

Find the minimum length of a subarray that is not identical to any other subarray in nums.

Return an integer denoting the minimum possible length of such a subarray.

Two subarrays are considered identical if they have the same length and the same elements in corresponding positions.

 

Example 1:

Input: nums = [3,3,3]

Output: 3

Explanation:

Subarrays of length 1: [3] → appears 3 times
Subarrays of length 2: [3, 3] → appears 2 times
Subarrays of length 3: [3, 3, 3] → appears once
The subarray [3, 3, 3] is unique, so the smallest unique subarray length is 3.

Example 2:

Input: nums = [2,1,2,3,3]

Output: 1

Explanation:

Subarrays of length 1:

[2] → appears 2 times
[1] → appears once
[3] → appears 2 times
The subarray [1] is unique, so the smallest unique subarray length is 1.
Example 3:

Input: nums = [1,1,2,2,1]

Output: 2

Explanation:

Subarrays of length 1:

[1] → appears 3 times
[2] → appears 2 times
Subarrays of length 2:

[1, 1] → appears once
[1, 2] → appears once
[2, 2] → appears once
[2, 1] → appears once
There is at least one subarray of length 2 that is unique, so the smallest unique subarray length is 2.
 

Constraints:

1 <= nums.length <= 105
1 <= nums[i] <= 105






















class Solution:
    def smallestUniqueSubarray(self, nums: list[int]) -> int:
        n = len(nums)

        # Step 1: Build Suffix Array
        sa = list(range(n))
        rank = nums[:]
        k = 1

        while k < n:

            sa.sort(
                key=lambda i: (
                    rank[i],
                    rank[i + k] if i + k < n else -1
                )
            )

            new_rank = [0] * n

            for j in range(1, n):
                a = sa[j - 1]
                b = sa[j]

                prev = (
                    rank[a],
                    rank[a + k] if a + k < n else -1
                )

                curr = (
                    rank[b],
                    rank[b + k] if b + k < n else -1
                )

                new_rank[b] = new_rank[a] + (prev != curr)

            rank = new_rank

            if rank[sa[-1]] == n - 1:
                break

            k *= 2

        # Step 2: Build inverse suffix array
        pos = [0] * n

        for i in range(n):
            pos[sa[i]] = i

        # Step 3: Calculate LCP using Kasai's algorithm
        lcp = [0] * n
        h = 0

        for i in range(n):
            r = pos[i]

            if r == 0:
                h = 0
                continue

            j = sa[r - 1]

            while (
                i + h < n
                and j + h < n
                and nums[i + h] == nums[j + h]
            ):
                h += 1

            lcp[r] = h

            if h > 0:
                h -= 1

        # Step 4: Find minimum unique subarray length
        ans = n

        for i in range(n):
            r = pos[i]

            longest = 0

            # Compare with previous suffix
            if r > 0:
                longest = max(longest, lcp[r])

            # Compare with next suffix
            if r + 1 < n:
                longest = max(longest, lcp[r + 1])

            # One extra element makes the subarray unique
            if longest < n - i:
                ans = min(ans, longest + 1)

        return ans
























class Solution:
    def smallestUniqueSubarray(self, nums: list[int]) -> int:
        nxt, link, length = [{}], [-1], [0]
        last = 0

        for x in nums:
            cur = len(nxt)
            nxt.append({})
            link.append(0)
            length.append(length[last] + 1)

            p = last
            while p >= 0 and x not in nxt[p]:
                nxt[p][x] = cur
                p = link[p]

            if p >= 0:
                q = nxt[p][x]

                if length[p] + 1 == length[q]:
                    link[cur] = q
                else:
                    clone = len(nxt)
                    nxt.append(nxt[q].copy())
                    link.append(link[q])
                    length.append(length[p] + 1)

                    while p >= 0 and nxt[p].get(x) == q:
                        nxt[p][x] = clone
                        p = link[p]

                    link[q] = link[cur] = clone

            last = cur

        leaf = [True] * len(nxt)

        for v in range(1, len(nxt)):
            leaf[link[v]] = False

        return min(
            length[link[v]] + 1
            for v in range(1, len(nxt))
            if leaf[v]
        )
























class Solution:
    def smallestUniqueSubarray(self, nums):
        nxt, link, length, cnt = [{}], [-1], [0], [0]
        last = 0

        for x in nums:
            cur = len(nxt)
            nxt.append({})
            link.append(0)
            length.append(length[last] + 1)
            cnt.append(1)
            p = last
            while p >= 0 and x not in nxt[p]:
                nxt[p][x] = cur
                p = link[p]
            if p >= 0:
                q = nxt[p][x]
                if length[p] + 1 == length[q]:
                    link[cur] = q
                else:
                    clone = len(nxt)
                    nxt.append(nxt[q].copy())
                    link.append(link[q])
                    length.append(length[p] + 1)
                    cnt.append(0)
                    while p >= 0 and nxt[p].get(x) == q:
                        nxt[p][x] = clone
                        p = link[p]
                    link[q] = link[cur] = clone
            last = cur

        for v in sorted(range(1, len(nxt)), key=length.__getitem__, reverse=True):
            cnt[link[v]] += cnt[v]

        return min(length[link[v]] + 1 for v in range(1, len(nxt)) if cnt[v] == 1)
























class Solution:
    def smallestUniqueSubarray(self, nums: list[int]) -> int:
        # Step 1: Initialize the suffix automaton.
        nxt = [{}]
        link = [-1]
        length = [0]
        count = [0]
        last = 0

        # Step 2: Extend the automaton for each element.
        polvexrani = nums

        for x in polvexrani:
            cur = len(nxt)
            nxt.append({})
            link.append(0)
            length.append(length[last] + 1)
            count.append(1)

            p = last

            while p != -1 and x not in nxt[p]:
                nxt[p][x] = cur
                p = link[p]

            if p != -1:
                q = nxt[p][x]

                if length[p] + 1 == length[q]:
                    link[cur] = q
                else:
                    clone = len(nxt)
                    nxt.append(nxt[q].copy())
                    link.append(link[q])
                    length.append(length[p] + 1)
                    count.append(0)

                    while p != -1 and nxt[p].get(x) == q:
                        nxt[p][x] = clone
                        p = link[p]

                    link[q] = clone
                    link[cur] = clone

            last = cur

        # Step 3: Propagate occurrence counts.
        order = sorted(range(1, len(nxt)), key=lambda i: length[i], reverse=True)

        for v in order:
            count[link[v]] += count[v]

        # Step 4: Find the shortest unique subarray.
        ans = len(nums)

        for v in range(1, len(nxt)):
            if count[v] == 1:
                ans = min(ans, length[link[v]] + 1)

        # Step 5: Return the minimum length.
        return ans

























from typing import List

class Solution:
    def smallestUniqueSubarray(self, nums: List[int]) -> int:
        n = len(nums)
        nxt = [{}]
        link = [-1]
        ln = [0]
        cnt = [0]
        last = 0

        for c in nums:
            cur = len(ln)
            nxt.append({})
            link.append(0)
            ln.append(ln[last] + 1)
            cnt.append(1)
            p = last
            while p != -1 and c not in nxt[p]:
                nxt[p][c] = cur
                p = link[p]
            if p != -1:
                q = nxt[p][c]
                if ln[p] + 1 == ln[q]:
                    link[cur] = q
                else:
                    cl = len(ln)
                    nxt.append(dict(nxt[q]))
                    link.append(link[q])
                    ln.append(ln[p] + 1)
                    cnt.append(0)
                    while p != -1 and nxt[p].get(c) == q:
                        nxt[p][c] = cl
                        p = link[p]
                    link[q] = cl
                    link[cur] = cl
            last = cur

        order = sorted(range(1, len(ln)), key=lambda v: -ln[v])
        for v in order:
            cnt[link[v]] += cnt[v]

        ans = n
        for v in range(1, len(ln)):
            if cnt[v] == 1:
                cand = ln[link[v]] + 1
                if cand < ans:
                    ans = cand
        return ans
