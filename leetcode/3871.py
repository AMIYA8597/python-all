3871. Count Commas in Range II
Medium
Topics
premium lock icon
Companies
Hint
You are given an integer n.

Return the total number of commas used when writing all integers from [1, n] (inclusive) in standard number formatting.

In standard formatting:

A comma is inserted after every three digits from the right.
Numbers with fewer than 4 digits contain no commas.
 

Example 1:

Input: n = 1002

Output: 3

Explanation:

The numbers "1,000", "1,001", and "1,002" each contain one comma, giving a total of 3.

Example 2:

Input: n = 998

Output: 0

Explanation:

​​​​​​​All numbers from 1 to 998 have fewer than four digits. Therefore, no commas are used.

 

Constraints:

1 <= n <= 1015


























class Solution:
    def countCommas(self, n: int) -> int:
        ans = 0
        power = 1000

        while power <= n:
            ans += n - power + 1
            power *= 1000

        return ans
    















1. First ask: when does a comma appear?

A comma is placed every 3 digits from the right.

So:

1       → no comma
99      → no comma
999     → no comma
1,000   → 1 comma
9,999   → 1 comma
10,000  → 1 comma
999,999 → 1 comma
1,000,000 → 2 commas

Therefore, the important boundaries are:

1,000
1,000,000
1,000,000,000
1,000,000,000,000
...

These are powers of 1000.

2. Don't count commas per number

Suppose:

n = 1002

We could theoretically do:

1     → 0
2     → 0
...
999   → 0
1000  → 1
1001  → 1
1002  → 1

But we obviously don't want to iterate from 1 to n, especially because:

n <= 10^15

Instead, we count how many numbers contribute a comma.

3. Counting the first comma

Every number from:

1000 → n

has at least one comma.

How many numbers are there?

For a range:

L → R

the number of elements is:

R - L + 1

Therefore:

1000 → n

contains:

n - 1000 + 1

numbers.

For n = 1002:

1002 - 1000 + 1
= 3

So we already have:

3 commas
4. But what about numbers with 2 commas?

Consider:

1,000,000
1,000,001
1,000,002
...

Every number from 1,000,000 onward has at least 2 commas.

So we need to add another comma for every number in:

1,000,000 → n

The count is:

n - 1,000,000 + 1

Notice something important:

We're not replacing the first count.

We're adding another comma because those numbers have an additional comma.

For example:

1,000,000

has 2 commas:

1st comma ← counted by the 1000 boundary
2nd comma ← counted by the 1000000 boundary
5. Same idea for 3 commas

Numbers beginning at:

1,000,000,000

have at least 3 commas.

So add:

n - 1,000,000,000 + 1

And then:

1,000,000,000,000

contributes another comma, and so on.

6. That's why we multiply by 1000

We start with:

1000

Then:

1000 × 1000 = 1,000,000

Then:

1,000,000 × 1000 = 1,000,000,000

Then:

1,000,000,000 × 1000 = 1,000,000,000,000

Each time, we're moving to the next possible comma.

So conceptually:

power = 1,000

       ↓ ×1000

power = 1,000,000

       ↓ ×1000

power = 1,000,000,000

       ↓ ×1000

power = 1,000,000,000,000
7. Let's manually trace n = 1,000,002

There are two comma positions that matter.

First comma

Numbers:

1,000 → 1,000,002

Count:

1,000,002 - 1,000 + 1
= 999,003

So there are 999,003 first commas.

Second comma

Numbers:

1,000,000 → 1,000,002

Count:

1,000,002 - 1,000,000 + 1
= 3

So there are 3 additional commas.

Total:

999,003 + 3
= 999,006

And that's the answer.

8. The key insight

The entire problem boils down to this:

Instead of asking "How many commas does each number have?", ask "How many numbers have a comma at each position?"

For every comma position:

1000              → contributes 1st comma
1000² = 1,000,000 → contributes 2nd comma
1000³             → contributes 3rd comma
1000⁴             → contributes 4th comma
...

For each boundary power, the number of additional commas is:

n - power + 1

provided:

power <= n

That's the entire reasoning behind the solution.

And importantly, 1000, not 10000, is the first boundary because 1,000 is the first number that contains a comma.



























class Solution:
    def countCommas(self, n: int) -> int:
        ans = 0
        x = 1000
        while x <= n:
            ans += n-x+1
            x *= 1000
        return ans

        



       
            
class Solution:
    def countCommas(self, n: int) -> int:
        ans = 0
        x = 999
        while x < n:
            print(x, ans)
            ans += n - x
            x *= 1000
            x += 999
        return ans

        



































