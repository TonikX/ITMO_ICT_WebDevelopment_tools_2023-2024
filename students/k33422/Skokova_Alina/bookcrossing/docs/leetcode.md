# Решение заданий из курса Top Interview Questions среднего уровня

## Задание 1. 3Sum

Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.

Constraints:

- 3 <= nums.length <= 3000
- -10^(5) <= nums[i] <= 10^(5)

```python
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        res = []
        nums.sort()
        for i, a in enumerate(nums):
            if i > 0 and a == nums[i - 1]:
                continue
            l, r = i + 1, len(nums) - 1
            while l < r:
                threeSum = a + nums[l] + nums[r]
                if threeSum > 0:
                    r -= 1
                elif threeSum < 0:
                    l += 1
                else:
                    res.append([a, nums[l], nums[r]])
                    l += 1
                    while nums[l] == nums[l - 1] and l < r:
                        l += 1
        return res
```

## Задание 2. Set Matrix Zeroes

Given an m x n integer matrix matrix, if an element is 0, set its entire row and column to 0's.

You must do it in place.

Constraints:

- m == matrix.length
- n == matrix[0].length
- 1 <= m, n <= 200
- -2^(31) <= matrix[i][j] <= 2^(31) - 1

```python
class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        rows, cols = len(matrix), len(matrix[0])
        rowZero = False
        for r in range(rows):
            for c in range(cols):
                if matrix[r][c] == 0:
                    matrix[0][c] = 0
                    if r > 0:
                        matrix[r][0] = 0
                    else:
                        rowZero = True
        for r in range(1, rows):
            for c in range(1, cols):
                if matrix[0][c] == 0 or matrix[r][0] == 0:
                    matrix[r][c] = 0
        if matrix[0][0] == 0:
            for r in range(rows):
                matrix[r][0] = 0
        if rowZero:
            for c in range(cols):
                matrix[0][c] = 0
```

## Задание 3. Group Anagrams

Given an array of strings strs, group the anagrams together. You can return the answer in any order.

Constraints:

- 1 <= strs.length <= 10^(4)
- 0 <= strs[i].length <= 100
- strs[i] consists of lowercase English letters.

```python
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        res = {}
        for s in strs:
            count = [0] * 26 # a...z
            for c in s:
                count[ord(c) - ord("a")] += 1
            key = tuple(count)
            if key in res:
                res[key].append(s)
            else:
                res[key] = [s]
        return list(res.values())
```

## Задание 4. Longest Substring Without Repeating Characters

Given a string s, find the length of the longest substring without repeating characters.

Constraints:

- 0 <= s.length <= 5 * 10^(4)
- s consists of English letters, digits, symbols and spaces.

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        charSet = set()
        l = 0 # указатель для метода скользящего окна
        res = 0
        for r in range(len(s)):
            while s[r] in charSet:
                charSet.remove(s[l])
                l += 1
            charSet.add(s[r])
            res = max(res, r - l + 1)
        return res
```

## Задание 5. Longest Palindromic Substring

Given a string s, return the longest palindromic substring in s.

Constraints:

- 1 <= s.length <= 1000
- s consist of only digits and English letters.

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        res = ''
        resLen = 0
        for i in range(len(s)):
            # нечетная длина
            l, r = i, i  # начинаем в середине
            while l >= 0 and r < len(s) and s[l] == s[r]: # пока это палиндром
                if (r - l + 1) > resLen:
                    res = s[l:r+1]
                    resLen = r - l + 1
                l -= 1
                r += 1
                
            # четная длина
            l, r = i, i + 1
            while l >= 0 and r < len(s) and s[l] == s[r]:
                if  (r - l + 1) > resLen:
                    res = s[l:r+1]
                    resLen = r - l + 1
                l -= 1
                r += 1
        return res
```

## Задание 6. Increasing Triplet Subsequence

Given an integer array nums, return true if there exists a triple of indices (i, j, k) such that i < j < k and nums[i] < nums[j] < nums[k]. If no such indices exists, return false.

Constraints:

- 1 <= nums.length <= 5 * 10^(5)
- -2^(31) <= nums[i] <= 2^(31) - 1

```python
class Solution:
    def increasingTriplet(self, nums: List[int]) -> bool:
        smallest = float('inf')
        middle = float('inf')
        for num in nums:
            if num > middle:
                return True
            if num <= smallest:
                smallest = num
            else:
                middle = num
        return False
```

## Задание 7. Happy Number

Write an algorithm to determine if a number n is happy.

A happy number is a number defined by the following process:

- Starting with any positive integer, replace the number by the sum of the squares of its digits.
- Repeat the process until the number equals 1 (where it will stay), or it **loops endlessly in a cycle** which does not include 1.
- Those numbers for which this process ends in 1 are happy.

Return true if n is a happy number, and false if not.

Constraints:

- 1 <= n <= 2^(31) - 1

```python
class Solution:
    def isHappy(self, n: int) -> bool:
        res = []
        while n not in res: # пока нет петли
            res.append(n)
            sum_sq_dig = sum([int(i) ** 2 for i in str(n)])
            if sum_sq_dig == 1:
                return True
            n = sum_sq_dig
        return False
```

## Задание 8. Factorial Trailing Zeroes

Given an integer n, return the number of trailing zeroes in n!.

Note that n! = n * (n - 1) * (n - 2) * ... * 3 * 2 * 1.

Constraints:

- 0 <= n <= 10^(4)

```python
class Solution:
    def trailingZeroes(self, n: int) -> int:
        res = 0
        while n >= 5:
            n //= 5 
            res += n # сколько пятерок число вмещает, двойки есть всегда в пятерке, т.к. четные
        return res
```

## Задание 9. Excel Sheet Column Number

Given a string columnTitle that represents the column title as appears in an Excel sheet, return its corresponding column number.

For example:

A -> 1

B -> 2

C -> 3

...

Z -> 26

AA -> 27

AB -> 28 

...

Constraints:

- 1 <= columnTitle.length <= 7
- columnTitle consists only of uppercase English letters
- columnTitle is in the range ["A", "FXSHRXW"]

```python
class Solution:
    def titleToNumber(self, columnTitle: str) -> int:
        res = 0
        for i in range(len(columnTitle)):
            res += (ord(columnTitle[::-1][i]) - ord("A") + 1) * (26 ** i)
        return res
```

## Задание 10. Pow(x, n)

Implement pow(x, n), which calculates x raised to the power n.

Constraints:

- -100.0 < x < 100.0
- -2^(31) <= n <= 2^(31)-1
- n is an integer.
- Either x is not zero or n > 0
- -10^(4) <= x^(n) <= 10^(4)

```python
class Solution:
    def myPow(self, x: float, n: int) -> float:
        def helper(x, n):
            if n == 0:
                return 1
            elif x == 0:
                return 0
            res = helper(x, n // 2)
            return x * res * res if n % 2 else res * res
        res = helper(x, abs(n))
        return res if n >= 0 else 1 / res
```

## Задание 11. Sqrt(x)

Given a non-negative integer x, return the square root of x rounded down to the nearest integer. The returned integer should be non-negative as well.

You must not use any built-in exponent function or operator.

For example, do not use pow(x, 0.5) in c++ or x ** 0.5 in python.

Constraints:

- 0 <= x <= 2^(31) - 1

```python
class Solution:
    def mySqrt(self, x: int) -> int:
        l, r = 0, x
        res = 0
        while l <= r:
            m = l + ((r - l) // 2) # середина, чтобы не выйти за пределы
            if (m * m) > x:
                r = m - 1
            elif (m * m) < x:
                l = m + 1
                res = m # может быть результатом
            else:
                return m
        return res
```

## Задание 12. Sum of Two Integers

Given two integers a and b, return the sum of the two integers without using the operators + and -.

Constraints:

- -1000 <= a, b <= 1000

```python
class Solution:
    def getSum(self, a: int, b: int) -> int:
        if a < 0 and b < 0:
            ll1 = [1] * abs(a)
            ll2 = [1] * abs(b)
            ll1.extend(ll2)
            return -len(ll1) 
        elif a >= 0 and b >= 0:
            ll1 = [1] * a
            ll2 = [1] * b
            ll1.extend(ll2)
            return len(ll1)
        else:
            signs = {abs(min(a, b)): -1, abs(max(a, b)): 1}
            lesser = min(abs(a), abs(b))
            greater = max(abs(a), abs(b))
            ll1 = [1] * greater
            ll2 = [1] * lesser
            return len(ll1[len(ll2):]) * signs[greater]
```