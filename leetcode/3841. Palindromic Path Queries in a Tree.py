3841. Palindromic Path Queries in a Tree


You are given an undirected tree with n nodes labeled 0 to n - 1. This is represented by a 2D array edges of length n - 1, where edges[i] = [ui, vi] indicates an undirected edge between nodes ui and vi.

You are also given a string s of length n consisting of lowercase English letters, where s[i] represents the character assigned to node i.

You are also given a string array queries, where each queries[i] is either:

"update ui c": Change the character at node ui to c. Formally, update s[ui] = c.
"query ui vi": Determine whether the string formed by the characters on the unique path from ui to vi (inclusive) can be rearranged into a palindrome.
Return a boolean array answer, where answer[j] is true if the jth query of type "query ui vi"​​​​​​​ can be rearranged into a palindrome, and false otherwise.

 

Example 1:

Input: n = 3, edges = [[0,1],[1,2]], s = "aac", queries = ["query 0 2","update 1 b","query 0 2"]

Output: [true,false]

Explanation:

"query 0 2": Path 0 → 1 → 2 gives "aac", which can be rearranged to form "aca", a palindrome. Thus, answer[0] = true.
"update 1 b": Update node 1 to 'b', now s = "abc".
"query 0 2": Path characters are "abc", which cannot be rearranged to form a palindrome. Thus, answer[1] = false.
Thus, answer = [true, false].

Example 2:

Input: n = 4, edges = [[0,1],[0,2],[0,3]], s = "abca", queries = ["query 1 2","update 0 b","query 2 3","update 3 a","query 1 3"]

Output: [false,false,true]

Explanation:

"query 1 2": Path 1 → 0 → 2 gives "bac", which cannot be rearranged to form a palindrome. Thus, answer[0] = false.
"update 0 b": Update node 0 to 'b', now s = "bbca".
"query 2 3": Path 2 → 0 → 3 gives "cba", which cannot be rearranged to form a palindrome. Thus, answer[1] = false.
"update 3 a": Update node 3 to 'a', s = "bbca".
"query 1 3": Path 1 → 0 → 3 gives "bba", which can be rearranged to form "bab", a palindrome. Thus, answer[2] = true.
Thus, answer = [false, false, true].

 

Constraints:

1 <= n == s.length <= 5 * 104
edges.length == n - 1
edges[i] = [ui, vi]
0 <= ui, vi <= n - 1
s consists of lowercase English letters.
The input is generated such that edges represents a valid tree.
1 <= queries.length <= 5 * 104​​​​​​​
queries[i] = "update ui c" or
queries[i] = "query ui vi"
0 <= ui, vi <= n - 1
c is a lowercase English letter.




















class Solution:
    def palindromePath(self, n: int, edges: list[list[int]], s: str, queries: list[str]) -> list[bool]:
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)

        LOG = n.bit_length()
        parent = [[0] * n for _ in range(LOG)]
        depth = [0] * n
        tin = [0] * n
        tout = [0] * n
        timer = 0

        stack = [(0, -1, 0)]

        while stack:
            u, p, state = stack.pop()

            if state == 0:
                tin[u] = timer
                timer += 1

                parent[0][u] = u if p == -1 else p

                for k in range(1, LOG):
                    parent[k][u] = parent[k - 1][parent[k - 1][u]]

                stack.append((u, p, 1))

                for v in reversed(adj[u]):
                    if v != p:
                        depth[v] = depth[u] + 1
                        stack.append((v, u, 0))
            else:
                tout[u] = timer - 1

        bit = [0] * (n + 2)
        values = [1 << (ord(c) - ord('a')) for c in s]

        def add(i, delta):
            i += 1
            while i < len(bit):
                bit[i] ^= delta
                i += i & -i

        def prefix(i):
            result = 0
            i += 1
            while i > 0:
                result ^= bit[i]
                i -= i & -i
            return result

        for u in range(n):
            add(tin[u], values[u])
            add(tout[u] + 1, values[u])

        def is_ancestor(u, v):
            return tin[u] <= tin[v] <= tout[u]

        def lca(u, v):
            if is_ancestor(u, v):
                return u
            if is_ancestor(v, u):
                return v

            for k in range(LOG - 1, -1, -1):
                p = parent[k][u]
                if not is_ancestor(p, v):
                    u = p

            return parent[0][u]

        ans = []

        for q in queries:
            parts = q.split()

            if parts[0] == "update":
                u = int(parts[1])
                c = parts[2]
                new_value = 1 << (ord(c) - ord('a'))

                if values[u] != new_value:
                    delta = values[u] ^ new_value

                    add(tin[u], delta)
                    add(tout[u] + 1, delta)

                    values[u] = new_value

            else:
                u = int(parts[1])
                v = int(parts[2])
                w = lca(u, v)

                mask = prefix(tin[u]) ^ prefix(tin[v]) ^ values[w]

                ans.append((mask & (mask - 1)) == 0)

        return ans




















"""
Constraints:
1 <= n == s.length <= 5 * 10^4
edges.length == n - 1
edges[i] = [ui, vi]
0 <= ui, vi <= n - 1
s consists of lowercase English letters.
The input is generated such that edges represents a valid tree.
1 <= queries.length <= 5 * 10^4​​​​​​​
queries[i] = "update ui c" or
queries[i] = "query ui vi"
0 <= ui, vi <= n - 1
c is a lowercase English letter.

Hints:
Use heavy light decomposition to break each path query into O(log n) segments.
Represent characters as a 26-bit mask and maintain segment data with XOR. A path can form a palindrome if the resulting mask has at most one bit set.

Copied without trying to understand:
https://leetcode.com/problems/palindromic-path-queries-in-a-tree/solutions/7579030/brilliant-python3cpp-implementation-onq-vn85l

"""
class Solution:
    def palindromePath(self, n: int, E: list[list[int]], s: str, Q: list[str]) -> list[bool]:
        P, D = [0] * n, [0] * n
        D[0] = 2
        for u, v in E: P[u], P[v], D[u], D[v] = P[u] ^ v, P[v] ^ u, D[u] + 1, D[v] + 1

        SS, C, QQ = [1] * n, [-1] * n, [i for i in range(n) if D[i] == 1]
        for i in QQ:
            p, ss = P[i], SS[i]
            SS[p] += ss
            if (c := C[p]) == -1 or ss > SS[c]: C[p] = i

            P[p], D[p] = P[p] ^ i, D[p] - 1
            if D[p] == 1: QQ.append(p)
        QQ.append(0)

        T, D, L, t = [-1] * n, [-1] * n, [0] * n, 0
        for i in reversed(QQ):
            if ~D[i]: continue

            tt = i
            while ~i: T[i], L[t], D[i], t, i = tt, 1 << ord(s[i]) - 97, t, t + 1, C[i]
        
        B = [0] + L
        for i in range(1, n + 1):
            j = i + (i & -i)
            if j <= n: B[j] ^= B[i]
        
        A = []
        for q in Q:
            match q.split():
                case ("update", i, c):
                    x = D[int(i)]
                    v = (1 << ord(c) - 97)
                    d = v ^ L[x]
                    L[x] = v
                    x += 1
                    while x <= n: B[x], x = B[x] ^ d, x + (x & -x)
                case ("query", u, v):
                    u, v = map(int, (u, v))
                    r = 0
                    while T[u] != T[v]:
                        if D[T[u]] < D[T[v]]: u, v = v, u
                        ss, tt = D[T[u]], D[u] + 1
                        while tt > ss: r, tt = r ^ B[tt], tt & (tt - 1)
                        while ss > tt: r, ss = r ^ B[ss], ss & (ss - 1)
                        u = P[T[u]]
                    if D[u] > D[v]: u, v = v, u
                    ss, tt = D[u], D[v] + 1
                    while tt > ss: r, tt = r ^ B[tt], tt & (tt - 1)
                    while ss > tt: r, ss = r ^ B[ss], ss & (ss - 1)
                    A.append(r & (r - 1) == 0)
        return A




















        class Solution:
    def palindromePath(self, n: int, E: list[list[int]], s: str, Q: list[str]) -> list[bool]:
        P, D = [0] * n, [0] * n
        D[0] = 2
        for u, v in E: P[u], P[v], D[u], D[v] = P[u] ^ v, P[v] ^ u, D[u] + 1, D[v] + 1

        SS, C, QQ = [1] * n, [-1] * n, [i for i in range(n) if D[i] == 1]
        for i in QQ:
            p, ss = P[i], SS[i]
            SS[p] += ss
            if (c := C[p]) == -1 or ss > SS[c]: C[p] = i

            P[p], D[p] = P[p] ^ i, D[p] - 1
            if D[p] == 1: QQ.append(p)
        QQ.append(0)

        T, D, L, t = [-1] * n, [-1] * n, [0] * n, 0
        for i in reversed(QQ):
            if ~D[i]: continue

            tt = i
            while ~i: T[i], L[t], D[i], t, i = tt, 1 << ord(s[i]) - 97, t, t + 1, C[i]
        
        B = [0] + L
        for i in range(1, n + 1):
            j = i + (i & -i)
            if j <= n: B[j] ^= B[i]
        
        A = []
        for q in Q:
            match q.split():
                case ("update", i, c):
                    x = D[int(i)]
                    v = (1 << ord(c) - 97)
                    d = v ^ L[x]
                    L[x] = v
                    x += 1
                    while x <= n: B[x], x = B[x] ^ d, x + (x & -x)
                case ("query", u, v):
                    u, v = map(int, (u, v))
                    r = 0
                    while T[u] != T[v]:
                        if D[T[u]] < D[T[v]]: u, v = v, u
                        ss, tt = D[T[u]], D[u] + 1
                        while tt > ss: r, tt = r ^ B[tt], tt & (tt - 1)
                        while ss > tt: r, ss = r ^ B[ss], ss & (ss - 1)
                        u = P[T[u]]
                    if D[u] > D[v]: u, v = v, u
                    ss, tt = D[u], D[v] + 1
                    while tt > ss: r, tt = r ^ B[tt], tt & (tt - 1)
                    while ss > tt: r, ss = r ^ B[ss], ss & (ss - 1)
                    A.append(r & (r - 1) == 0)
        return A


















        class Solution:
    def palindromePath(self, n: int, E: list[list[int]], s: str, Q: list[str]) -> list[bool]:
        P, D = [0] * n, [0] * n
        D[0] = 2
        for u, v in E: P[u], P[v], D[u], D[v] = P[u] ^ v, P[v] ^ u, D[u] + 1, D[v] + 1

        SS, C, QQ = [1] * n, [-1] * n, [i for i in range(n) if D[i] == 1]
        for i in QQ:
            p, ss = P[i], SS[i]
            SS[p] += ss
            if (c := C[p]) == -1 or ss > SS[c]: C[p] = i

            P[p], D[p] = P[p] ^ i, D[p] - 1
            if D[p] == 1: QQ.append(p)
        QQ.append(0)

        T, D, L, t = [-1] * n, [-1] * n, [0] * n, 0
        for i in reversed(QQ):
            if ~D[i]: continue

            tt = i
            while ~i: T[i], L[t], D[i], t, i = tt, 1 << ord(s[i]) - 97, t, t + 1, C[i]
        
        B = [0] + L
        for i in range(1, n + 1):
            j = i + (i & -i)
            if j <= n: B[j] ^= B[i]
        
        A = []
        for q in Q:
            match q.split():
                case ("update", i, c):
                    x = D[int(i)]
                    v = (1 << ord(c) - 97)
                    d = v ^ L[x]
                    L[x] = v
                    x += 1
                    while x <= n: B[x], x = B[x] ^ d, x + (x & -x)
                case ("query", u, v):
                    u, v = map(int, (u, v))
                    r = 0
                    while T[u] != T[v]:
                        if D[T[u]] < D[T[v]]: u, v = v, u
                        ss, tt = D[T[u]], D[u] + 1
                        while tt > ss: r, tt = r ^ B[tt], tt & (tt - 1)
                        while ss > tt: r, ss = r ^ B[ss], ss & (ss - 1)
                        u = P[T[u]]
                    if D[u] > D[v]: u, v = v, u
                    ss, tt = D[u], D[v] + 1
                    while tt > ss: r, tt = r ^ B[tt], tt & (tt - 1)
                    while ss > tt: r, ss = r ^ B[ss], ss & (ss - 1)
                    A.append(r & (r - 1) == 0)
        return A





















        class BIT:
    def __init__(self, n: int):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i: int, v: int) -> None:
        n = self.n
        bit = self.bit
        while i <= n:
            bit[i] ^= v
            i += i & -i

    def pref(self, i: int) -> int:
        res = 0
        bit = self.bit
        while i > 0:
            res ^= bit[i]
            i -= i & -i
        return res

    def range_xor(self, l: int, r: int, v: int) -> None:
        self.add(l, v)
        self.add(r + 1, v)

class Solution:
    def palindromePath(self, n: int, edges: List[List[int]], s: str, queries: List[str]) -> List[bool]:
        g = [[] for _ in range(n)]
        for u, v in edges:
            g[u].append(v)
            g[v].append(u)

        LOG1 = (n).bit_length()
        up = [[0] * n for _ in range(LOG1)]
        depth = [0] * n
        tin = [0] * n
        tout = [0] * n
        pref0 = [0] * n

        a = [1 << (ord(ch) - 97) for ch in s]

        t = 0
        st = [(0, 0, 0, 0)]
        while st:
            u, p, state, px = st.pop()
            if state == 0:
                t += 1
                tin[u] = t
                up[0][u] = p
                pref0[u] = px ^ a[u]
                st.append((u, p, 1, px))
                for v in g[u]:
                    if v == p:
                        continue
                    depth[v] = depth[u] + 1
                    st.append((v, u, 0, pref0[u]))
            else:
                tout[u] = t

        for k in range(1, LOG1):
            pu = up[k - 1]
            cu = up[k]
            for i in range(n):
                cu[i] = pu[pu[i]]

        def is_anc(u,v):
            return tin[u] <= tin[v] <= tout[u]

        def lca(u,v):
            if is_anc(u, v):
                return u
            if is_anc(v, u):
                return v
            x = u
            for k in range(LOG1 - 1, -1, -1):
                y = up[k][x]
                if not is_anc(y, v):
                    x = y
            return up[0][x]

        def curpref(u):
            return pref0[u] ^ bit.pref(tin[u])

        def ok(mask):
            return mask == 0 or (mask & (mask - 1)) == 0

        bit = BIT(n)
        ans = []
        for q in queries:
            p = q.split()
            if p[0] == "query":
                u = int(p[1])
                v = int(p[2])
                w = lca(u, v)
                mask = curpref(u) ^ curpref(v) ^ a[w]
                ans.append(ok(mask))
            else:
                u = int(p[1])
                c = p[2]
                nv = 1 << (ord(c) - 97)
                delta = a[u] ^ nv
                if delta:
                    a[u] = nv
                    bit.range_xor(tin[u], tout[u], delta)
        return ans
