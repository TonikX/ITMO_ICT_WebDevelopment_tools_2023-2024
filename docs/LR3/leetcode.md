# Leetcode

## Pow(x, n)

Implement pow(x, n), which calculates x raised to the power n (i.e., x^n).

```python
class Solution:
    def myPow(self, x: float, n: int) -> float:
        def rec(x, n):
            if n == 0:
                return 1
            if n == 1:
                return x
            if n % 2 == 0:
                return rec(x * x, n // 2)
            else:
                return x * rec(x * x, n // 2)

        if n < 0:
            return 1 / rec(x, -n)
        else:
            return rec(x, n)

```

## Sqrt(x)

Given a non-negative integer x, return the square root of x rounded down to the nearest integer. The returned integer should be non-negative as well.

You must not use any built-in exponent function or operator.

For example, do not use pow(x, 0.5) in c++ or x \*\* 0.5 in python.

```python
class Solution:
    def mySqrt(self, x: int) -> int:
        left, right = 0, x
        while left <= right:
            mid = (left + right) // 2
            if mid * mid <= x < (mid + 1) * (mid + 1):
                return mid
            elif mid * mid < x:
                left = mid + 1
            else:
                right = mid - 1
        return left

```

## Happy Number

Write an algorithm to determine if a number n is happy.

A happy number is a number defined by the following process:

Starting with any positive integer, replace the number by the sum of the squares of its digits.
Repeat the process until the number equals 1 (where it will stay), or it loops endlessly in a cycle which does not include 1.
Those numbers for which this process ends in 1 are happy.
Return true if n is a happy number, and false if not.

```python
class Solution:
    def isHappy(self, n: int) -> bool:
        s = set()
        while n != 1 and n not in s:
            s.add(n)
            n = sum(int(d) ** 2 for d in str(n))
        return n == 1
```
