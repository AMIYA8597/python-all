1096. Brace Expansion II
Hard
Topics
premium lock icon
Companies
Hint
Under the grammar given below, strings can represent a set of lowercase words. Let R(expr) denote the set of words the expression represents.

The grammar can best be understood through simple examples:

Single letters represent a singleton set containing that word.
R("a") = {"a"}
R("w") = {"w"}
When we take a comma-delimited list of two or more expressions, we take the union of possibilities.
R("{a,b,c}") = {"a","b","c"}
R("{{a,b},{b,c}}") = {"a","b","c"} (notice the final set only contains each word at most once)
When we concatenate two expressions, we take the set of possible concatenations between two words where the first word comes from the first expression and the second word comes from the second expression.
R("{a,b}{c,d}") = {"ac","ad","bc","bd"}
R("a{b,c}{d,e}f{g,h}") = {"abdfg", "abdfh", "abefg", "abefh", "acdfg", "acdfh", "acefg", "acefh"}
Formally, the three rules for our grammar:

For every lowercase letter x, we have R(x) = {x}.
For expressions e1, e2, ... , ek with k >= 2, we have R({e1, e2, ...}) = R(e1) ∪ R(e2) ∪ ...
For expressions e1 and e2, we have R(e1 + e2) = {a + b for (a, b) in R(e1) × R(e2)}, where + denotes concatenation, and × denotes the cartesian product.
Given an expression representing a set of words under the given grammar, return the sorted list of words that the expression represents.

 

Example 1:

Input: expression = "{a,b}{c,{d,e}}"
Output: ["ac","ad","ae","bc","bd","be"]
Example 2:

Input: expression = "{{a,z},a{b,c},{ab,z}}"
Output: ["a","ab","ac","z"]
Explanation: Each distinct word is written only once in the final answer.
 

Constraints:

1 <= expression.length <= 60
expression[i] consists of '{', '}', ','or lowercase English letters.
The given expression represents a set of words based on the grammar given in the description.




















class Solution:
    def braceExpansionII(self, expression: str) -> list[str]:

        def union(A, B):
            return A | B

        def product(A, B):
            return {a + b for a in A for b in B}

        # Parse an expression containing concatenation and commas
        def parse_expr():
            nonlocal i

            result = parse_term()

            while i < n and expression[i] == ',':
                i += 1
                result = union(result, parse_term())

            return result

        # Parse consecutive pieces (concatenation)
        def parse_term():
            nonlocal i

            result = {""}

            while i < n and expression[i] not in "},":
                if expression[i] == '{':
                    i += 1                  # skip '{'
                    part = parse_expr()
                    i += 1                  # skip '}'
                else:
                    part = {expression[i]}
                    i += 1

                result = product(result, part)

            return result

        i = 0
        n = len(expression)

        return sorted(parse_expr())


























class Solution:
    def braceExpansionII(self, expression: str) -> list[str]:
        def merge(groups: list[list[str]], group: list[str]) -> None:
            if not groups[-1]:
                groups[-1] = group
                return
            groups[-1] = [word1 + word2 for word1 in groups[-1] for word2 in group]

        def dfs(s: int, e: int) -> list[str]:
            groups = [[]]
            layer = 0
            left = 0
            for i in range(s, e + 1):
                c = expression[i]
                if c == '{':
                    layer += 1
                    if layer == 1:
                        left = i + 1
                elif c == '}':
                    layer -= 1
                    if layer == 0:
                        group = dfs(left, i - 1)
                        merge(groups, group)
                elif c == ',' and layer == 0:
                    groups.append([])
                elif layer == 0:
                    merge(groups, [c])
            return sorted(list({word for group in groups for word in group}))

        return dfs(0, len(expression) - 1)
































class Solution:
    def braceExpansionII(self, expression: str) -> List[str]:
        op = []  # Operator stack
        stk = []  # Set stack

        # Pop the operator at the top of the stack and perform the calculation
        def ope():
            l, r = len(stk) - 2, len(stk) - 1
            if op[-1] == "+":
                # Union operation
                stk[l] |= stk[r]
            else:
                # Cartesian product operation
                tmp = set()
                for left in stk[l]:
                    for right in stk[r]:
                        tmp.add(left + right)
                stk[l] = tmp
            op.pop()
            stk.pop()

        for i, ch in enumerate(expression):
            if ch == ",":
                # Keep popping operators from the top of the stack until the stack is empty or its top is not a multiplication sign
                while op and op[-1] == "*":
                    ope()
                op.append("+")
            elif ch == "{":
                # First determine whether a multiplication sign needs to be added, then push { onto the operator stack
                if i > 0 and (
                    expression[i - 1] == "}" or expression[i - 1].isalpha()
                ):
                    op.append("*")
                op.append("{")
            elif ch == "}":
                # Keep popping operators from the top of the stack until its top is {
                while op and op[-1] != "{":
                    ope()
                op.pop()
            else:
                # First determine whether a multiplication sign needs to be added, then push the newly constructed set onto the set stack
                if i > 0 and (
                    expression[i - 1] == "}" or expression[i - 1].isalpha()
                ):
                    op.append("*")
                stk.append({ch})

        while op:
            ope()

        return sorted(stk[-1])

























class Solution:
    def braceExpansionII(self, expression: str) -> list[str]:
        self._exp = expression
        _, res = self.parse_gen(0, set())
        return sorted(set(res))
    
    def parse_gen(self, idx, break_set):
        expression = self._exp
        # parse_gen
        entire = []
        building = []
        N = len(expression)
        i = idx
        while i < N:
            if expression[i].islower():
                building.append(expression[i])
                i += 1
                continue
            
            if expression[i] == '{':
                j, options = self.build_set(i)
                fixed = "".join(building)
                old_elts = entire.copy()
                entire = []
                for old in old_elts:
                    for option in options:
                        entire.append(old + fixed + option)
                    if not options:
                        entire.append(old + fixed)
                if not old_elts:
                    for option in options:
                        entire.append(fixed + option)
                    if not options:
                        entire.append(fixed)
                
                i = j + 1
                building = []
                continue
            
            if expression[i] in break_set:
                break
            
            raise ValueError(f"Failure at {i} when starting at index {idx}")
        
        if building:
            fixed = "".join(building)
            old_elts = entire.copy()
            entire = []
            for old in old_elts:
                entire.append(old + fixed)
            if not old_elts:
                entire.append(fixed)
        
        return i, entire


    def build_set(self, idx):
        '''
        Given that we're pointing to a { instance, build the option set AND return the index
        just after the matching }
        '''
        options = []
        N = len(self._exp)
        curr_i = idx + 1
        while curr_i < N:
            if self._exp[curr_i] == ',':
                # empty element
                curr_i += 1
                continue

            # collects element(s) recursively; these are suboptions
            j, built = self.parse_gen(curr_i, set(",}"))
            options += built
            if j < N and self._exp[j] == '}':
                curr_i = j
                break

            curr_i = j + 1
                    
        if curr_i == N:
            raise ValueError(f"No matching {{ for {idx}")
        
        # it's a } instance
        return (curr_i, options)
'''
Helpers:
a) parse_elt: Something that understands how to parse up to a ,
b) parse_options: Parses a {} statement
c) parse_gen: Top level parser
'''
