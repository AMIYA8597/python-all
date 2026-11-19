29. Divide Two Integers


Given two integers dividend and divisor, divide two integers without using multiplication, division, and mod operator.

The integer division should truncate toward zero, which means losing its fractional part. For example, 8.345 would be truncated to 8, and -2.7335 would be truncated to -2.

Return the quotient after dividing dividend by divisor.

Note: Assume we are dealing with an environment that could only store integers within the 32-bit signed integer range: [−231, 231 − 1]. For this problem, if the quotient is strictly greater than 231 - 1, then return 231 - 1, and if the quotient is strictly less than -231, then return -231.

 

Example 1:

Input: dividend = 10, divisor = 3
Output: 3
Explanation: 10/3 = 3.33333.. which is truncated to 3.
Example 2:

Input: dividend = 7, divisor = -3
Output: -2
Explanation: 7/-3 = -2.33333.. which is truncated to -2.
 

Constraints:

-231 <= dividend, divisor <= 231 - 1
divisor != 0


























class Solution:
    def divide(self, dividend: int, divisor: int) -> int:

        INT_MAX = 2**31 - 1
        INT_MIN = -(2**31)

        # Handle overflow case
        if dividend == INT_MIN and divisor == -1:
            return INT_MAX

        # Determine the sign of the result
        negative = (dividend < 0) != (divisor < 0)

        # Convert both numbers to positive
        dividend = abs(dividend)
        divisor = abs(divisor)

        quotient = 0

        # Subtract the largest possible shifted divisor
        while dividend >= divisor:

            temp = divisor
            multiple = 1

            while dividend >= (temp << 1):
                temp <<= 1
                multiple <<= 1

            dividend -= temp
            quotient += multiple

        # Apply the sign
        if negative:
            quotient = -quotient

        return quotient
























class Solution:
    def divide(self, dividend: int, divisor: int) -> int:

        INT_MAX = 2**31 - 1
        INT_MIN = -(2**31)

        if dividend == INT_MIN and divisor == -1:
            return INT_MAX

        negative = (dividend < 0) != (divisor < 0)

        a = abs(dividend)
        b = abs(divisor)

        result = 0

        while a >= b:
            temp = b
            multiple = 1

            while a >= (temp << 1):
                temp <<= 1
                multiple <<= 1

            a -= temp
            result += multiple

        if negative:
            result = -result

        return result






















class Solution:
    def divide(self, dividend: int, divisor: int) -> int:

        INT_MAX = 2**31 - 1
        INT_MIN = -(2**31)

        if dividend == INT_MIN and divisor == -1:
            return INT_MAX

        negative = (dividend < 0) != (divisor < 0)

        a = abs(dividend)
        b = abs(divisor)

        result = 0

        while a >= b:
            temp = b
            multiple = 1

            while a >= (temp << 1):
                temp <<= 1
                multiple <<= 1

            a -= temp
            result += multiple

        if negative:
            result = -result

        return result



















class Solution:
    def divide(self, dividend: int, divisor: int) -> int:

        dend = False
        sor = False
        if dividend < 0:
            dend = True
            dividend = abs(dividend)
        if divisor < 0:
            sor = True
            divisor = abs(divisor)
        quotient = 0
        for i in range(31,-1,-1):
            if divisor << i <= dividend:
                dividend -= divisor << i
                quotient += 1 << i

        return max(-quotient, -2**31) if dend ^ sor else min(quotient, 2**31-1)

        
        
