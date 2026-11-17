2911. Minimum Changes to Make K Semi-palindromes


Given a string s and an integer k, partition s into k substrings such that the letter changes needed to make each substring a semi-palindrome are minimized.

Return the minimum number of letter changes required.

A semi-palindrome is a special type of string that can be divided into palindromes based on a repeating pattern. To check if a string is a semi-palindrome:​

Choose a positive divisor d of the string's length. d can range from 1 up to, but not including, the string's length. For a string of length 1, it does not have a valid divisor as per this definition, since the only divisor is its length, which is not allowed.
For a given divisor d, divide the string into groups where each group contains characters from the string that follow a repeating pattern of length d. Specifically, the first group consists of characters at positions 1, 1 + d, 1 + 2d, and so on; the second group includes characters at positions 2, 2 + d, 2 + 2d, etc.
The string is considered a semi-palindrome if each of these groups forms a palindrome.
Consider the string "abcabc":

The length of "abcabc" is 6. Valid divisors are 1, 2, and 3.
For d = 1: The entire string "abcabc" forms one group. Not a palindrome.
For d = 2:
Group 1 (positions 1, 3, 5): "acb"
Group 2 (positions 2, 4, 6): "bac"
Neither group forms a palindrome.
For d = 3:
Group 1 (positions 1, 4): "aa"
Group 2 (positions 2, 5): "bb"
Group 3 (positions 3, 6): "cc"
All groups form palindromes. Therefore, "abcabc" is a semi-palindrome.
 

Example 1:

Input: s = "abcac", k = 2

Output: 1

Explanation: Divide s into "ab" and "cac". "cac" is already semi-palindrome. Change "ab" to "aa", it becomes semi-palindrome with d = 1.

Example 2:

Input: s = "abcdef", k = 2

Output: 2

Explanation: Divide s into substrings "abc" and "def". Each needs one change to become semi-palindrome.

Example 3:

Input: s = "aabbaa", k = 3

Output: 0

Explanation: Divide s into substrings "aa", "bb" and "aa". All are already semi-palindromes.

 

Constraints:

2 <= s.length <= 200
1 <= k <= s.length / 2
s contains only lowercase English letters.

























class Solution:
    def minimumChanges(self, s: str, k: int) -> int:
        n = len(s)
        cost = [[0] * n for _ in range(n)]

        for l in range(n):
            for r in range(l + 1, n):
                m = r - l + 1
                cost[l][r] = float('inf')

                for d in range(1, m):
                    if m % d == 0:
                        cnt = 0
                        for i in range(d):
                            left = l + i
                            right = l + i + (m // d - 1) * d

                            while left < right:
                                if s[left] != s[right]:
                                    cnt += 1
                                left += d
                                right -= d

                        cost[l][r] = min(cost[l][r], cnt)

        dp = [[float('inf')] * (k + 1) for _ in range(n + 1)]
        dp[0][0] = 0

        for i in range(2, n + 1):
            for j in range(1, min(k, i // 2) + 1):
                for p in range(2 * (j - 1), i - 1):
                    dp[i][j] = min(
                        dp[i][j],
                        dp[p][j - 1] + cost[p][i - 1]
                    )

        return dp[n][k]


















class Solution:
  def minimumChanges(self, s: str, k: int) -> int:
    n = len(s)
    
    # Calculates the dynamic programming state.
    # `start` is the suffix start, and `k1` is the number of parts
    # to split it into.
    @functools.cache
    def DP(start, k1):
      # If there is only 1 part, there is no splitting (pivot),
      # so the answer is the number of changes to make the whole
      # suffix a semi-palindrome.
      if k1 == 1:
        return toSemiPalindrome(start, n)
      
      # Try every way to split the suffix into a part followed by
      # another suffix.
      return min(
        toSemiPalindrome(start, pivot) + DP(pivot, k1 - 1)
        # There is an implicit rule that no part must be shorter than 2.
        # We use only such pivots that won't violate the rule.
        for pivot in range(start + 2, n - (k1 - 1) * 2 + 1)
      )
    
    # Counts the minimum number of changes to make an `s` substring
    # be a semi-palindrome.
    @functools.cache
    def toSemiPalindrome(start, end):
      minChanges = math.inf
      length = end - start
      
      # Try each valid `d`. Notice that `length` itself is not a valid `d`,
      # because otherwise any string would be a semi-palindrome
      for d in range(1, length):
        if length % d != 0:
          continue

        changeCount = 0
        subLength = length // d # Length of the palindrome for each offset

        for offset in range(d):
          # `i` is the distance from the edges of the palindrome
          for i in range(subLength // 2):
            if (
              s[start + offset + d * i] !=
              s[start + offset + d * (subLength - i - 1)]
            ):
              changeCount += 1

        minChanges = min(minChanges, changeCount)

      return minChanges

    return DP(0, k)





















    class Solution:
    def minimumChanges(self, s: str, k: int) -> int:
        n = len(s)
        div = defaultdict(lambda : [1])
        for d in range(2, n):
            for v in range(d + d, n + 1, d):
                div[v].append(d)
        
        def change(i, j):
            return min(semi(i, j, d) for d in div[j - i])
        
        @cache
        def semi(i, j, d):
            if i >= j : return 0
            return semi(i + d, j - d, d) + sum(s[i + ii] != s[j - d + ii] for ii in range(d))
        
        @cache
        def dfs(i, k):
            if k == 1:
                return change(0, i)
            return min([dfs(j, k - 1) + change(j, i) for j in range((k - 1) * 2, i - 1)])
        return dfs(n, k)























        from functools import cache # Importamos cache para memorizar resultados y evitar recalcular

class Solution:
    def minimumChanges(self, s: str, k: int) -> int:
        n = len(s) # Longitud total de la cadena principal
        
        @cache # Guarda en memoria el resultado de cost() para cada subcadena que reciba
        def cost(sub):
            L = len(sub) # Longitud de la subcadena actual
            
            # min() evalúa todos los divisores 'd' y se queda con el escenario más barato
            return min(
                
                # sum() exterior: suma los cambios de los 'd' grupos independientes
                sum(
                    
                    # sum() interior: cuenta cuántos caracteres son diferentes en un solo grupo.
                    # sub[g::d] extrae el grupo empezando en 'g' y saltando de 'd' en 'd'.
                    # sub[g::d][::-1] es exactamente ese mismo grupo, pero al revés.
                    # zip() empareja cada letra original con su espejo. 
                    # Si 'a != b', suma 1. 
                    # Al final dividimos // 2 porque cada diferencia se cuenta dos veces 
                    # (una al evaluar el lado izquierdo y otra al llegar al derecho).
                    sum(a != b for a, b in zip(sub[g::d], sub[g::d][::-1])) // 2 
                    
                    # Generamos los grupos desde el índice 0 hasta d-1
                    for g in range(d)
                )
                # Filtramos para usar únicamente los 'd' que sean divisores exactos de L
                for d in range(1, L) if L % d == 0
            )

        @cache # Memoriza el estado de la DP para no recalcular el mismo índice con las mismas particiones
        def dp(i, parts_left):
            # Caso base: si nos queda solo 1 partición, agarramos desde el índice 'i' hasta el final de la cadena
            if parts_left == 1: 
                return cost(s[i:])
                
            # Probamos todos los cortes 'j' posibles y nos quedamos con la combinación que sume menos cambios
            return min(
                # Costo de volver semi-palíndromo el corte actual + el costo óptimo de los cortes restantes
                cost(s[i:j+1]) + dp(j + 1, parts_left - 1) 
                
                # Iteramos 'j' para hacer el corte. 
                # Inicia en 'i + 1' porque la longitud mínima de la partición actual debe ser 2.
                # El límite 'n - 2 * parts_left + 2' es un freno de seguridad: 
                # garantiza que dejemos suficientes letras al final de la cadena para que 
                # las particiones restantes también puedan tener al menos longitud 2.
                for j in range(i + 1, n - 2 * parts_left + 2)
            )
            
        # Disparamos la recursión desde el primer caracter (índice 0) pidiendo 'k' particiones
        return dp(0, k)






















        class Solution:
    def minimumChanges(self, s: str, k: int) -> int:
        n = len(s)
        INF = 10**9

        divisors = [[] for _ in range(n + 1)]

        for d in range(1, n):
            for length in range(2 * d, n + 1, d):
                divisors[length].append(d)

        cost = [[INF] * (n + 1) for _ in range(n)]

        for i in range(n):
            for length in range(2, n - i + 1):
                best = INF

                for d in divisors[length]:
                    groups = length // d
                    changes = 0

                    for r in range(d):
                        left = i + r
                        right = i + r + (groups - 1) * d

                        while left < right:
                            if s[left] != s[right]:
                                changes += 1
                            left += d
                            right -= d

                    if changes < best:
                        best = changes

                cost[i][i + length] = best

        dp = [INF] * (n + 1)
        dp[0] = 0

        for parts in range(1, k + 1):
            ndp = [INF] * (n + 1)

            for end in range(2 * parts, n + 1):
                for start in range(2 * (parts - 1), end - 1):
                    if dp[start] != INF:
                        value = dp[start] + cost[start][end]
                        if value < ndp[end]:
                            ndp[end] = value

            dp = ndp

        return dp[n]
