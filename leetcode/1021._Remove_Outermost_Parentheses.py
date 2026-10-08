1021. Remove Outermost Parentheses
Easy
Topics
premium lock icon
Companies
Hint
A valid parentheses string is either empty "", "(" + A + ")", or A + B, where A and B are valid parentheses strings, and + represents string concatenation.

For example, "", "()", "(())()", and "(()(()))" are all valid parentheses strings.
A valid parentheses string s is primitive if it is nonempty, and there does not exist a way to split it into s = A + B, with A and B nonempty valid parentheses strings.

Given a valid parentheses string s, consider its primitive decomposition: s = P1 + P2 + ... + Pk, where Pi are primitive valid parentheses strings.

Return s after removing the outermost parentheses of every primitive string in the primitive decomposition of s.

 

Example 1:

Input: s = "(()())(())"
Output: "()()()"
Explanation: 
The input string is "(()())(())", with primitive decomposition "(()())" + "(())".
After removing outer parentheses of each part, this is "()()" + "()" = "()()()".
Example 2:

Input: s = "(()())(())(()(()))"
Output: "()()()()(())"
Explanation: 
The input string is "(()())(())(()(()))", with primitive decomposition "(()())" + "(())" + "(()(()))".
After removing outer parentheses of each part, this is "()()" + "()" + "()(())" = "()()()()(())".
Example 3:

Input: s = "()()"
Output: ""
Explanation: 
The input string is "()()", with primitive decomposition "()" + "()".
After removing outer parentheses of each part, this is "" + "" = "".
 

Constraints:

1 <= s.length <= 105
s[i] is either '(' or ')'.
s is a valid parentheses string.





















class Solution:
    def removeOuterParentheses(self, s: str) -> str:
        result = []
        balance = 0

        for ch in s:
            if ch == '(':
                if balance > 0:
                    result.append(ch)
                balance += 1

            else:  # ch == ')'
                balance -= 1
                if balance > 0:
                    result.append(ch)

        return ''.join(result)



















        class Solution:
    def removeOuterParentheses(self, s: str) -> str:
        res=[]
        count=0
        for ch in s:
            if ch=='(':
                if count>0:
                    res.append(ch)
                count+=1
            else:
                count-=1
                if count>0:
                    res.append(ch)
        return "".join(res)

























        class Solution:
    def removeOuterParentheses(self, s: str) -> str:
        stack = []
        m = 0
        for x in s:
            if x == '(':
                if m > 0:
                     stack.append(x)
                m += 1
            else:
                if m != 1:
                    stack.append(x)
                m -= 1
        return ''.join(stack)





















        class Solution:
    def removeOuterParentheses(self, s: str) -> str:
        res=""
        count=0
        for ch in s:
            if ch == "(":
                if count>0:
                    res+=ch
                count +=1    
            else :
                count -=1
                if count>0:
                    res+=ch
        return res                    

























        class Solution:
    def removeOuterParentheses(self, s: str) -> str:
        op = ''
        depth = 0
        for i in s:
            if i == '(' and depth > 0:
                depth += 1
                op += '('
            elif i == '(':
                depth += 1
            else:
                depth -= 1
                if depth == 0:
                    continue
                else:
                    op += ')'
        return op
