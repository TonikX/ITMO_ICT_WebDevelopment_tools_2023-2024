# Leetcode
##  **3Sum**

Описание:
Given an integer array nums, return all the triplets ```[nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0```.

Notice that the solution set must not contain duplicate triplets.


```python
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        result = []
        for i in range(len(nums) - 2):
            if i > 0 and nums[i] == nums[i - 1]:
                continue
            target = -nums[i]
            j, k = i + 1, len(nums) - 1
            while j < k:
                if nums[j] + nums[k] == target:
                    result.append([nums[i], nums[j], nums[k]])
                    j += 1
                    while j < k and nums[j] == nums[j - 1]:
                        j += 1
                elif nums[j] + nums[k] < target:
                    j += 1
                else:
                    k -= 1
        return result

```

##  **Set Matrix Zeroes**

Описание:
Given an m x n integer matrix matrix, if an element is 0, set its entire row and column to 0's.

You must do it in place.


```python
class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        
        Do not return anything, modify matrix in-place instead.
        
        rows, cols = len(matrix), len(matrix[0])
        row_zeroes, col_zeroes = set(), set()

        for i in range(rows):
            for j in range(cols):
                if matrix[i][j] == 0:
                    row_zeroes.add(i)
                    col_zeroes.add(j)

        for i in range(rows):
            for j in range(cols):
                if i in row_zeroes or j in col_zeroes:
                    matrix[i][j] = 0
```

##  **Group Anagrams**

Описание:
Given an array of strings strs, group the anagrams together. You can return the answer in any order.

An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.


```python
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        anagrams = {}

        for s in strs:
            t = tuple(sorted(s))
            if t in anagrams:
                anagrams[t].append(s)
            else:
                anagrams[t] = [s]
            print(anagrams[t])
        return list(anagrams.values())
```

##  **Longest Substring Without Repeating Characters**

Описание:
Given a string s, find the length of the longest substring without repeating characters.


```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        start, max_len = 0, 0
        used_chars = {} 
        
        for i in range(len(s)):
            char = s[i]
            if char in used_chars and used_chars[char] >= start:
                start = used_chars[char] + 1
            else:
                max_len = max(max_len, i - start + 1)
            used_chars[char] = i

        return max_len
```


##  **Longest Palindromic Substring**

Описание:
Given a string s, return the longest palindromic substring in s.


```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        dp = [[False] * len(s) for _ in range(len(s))]
        max_length, start = 1, 0

        for i in range(len(s)):
            for j in range(i, -1, -1):
                if s[i] == s[j] and (i - j < 2 or dp[j + 1][i - 1]):
                    dp[j][i] = True
                    if i - j + 1 > max_length:
                        max_length = i - j + 1
                        start = j

        return s[start:start + max_length]

```

##  **Evaluate Reverse Polish Notation**

Описание:
You are given an array of strings tokens that represents an arithmetic expression in a Reverse Polish Notation.

Evaluate the expression. Return an integer that represents the value of the expression.

Note that:

The valid operators are '+', '-', '*', and '/'.
Each operand may be an integer or another expression.
The division between two integers always truncates toward zero.
There will not be any division by zero.
The input represents a valid arithmetic expression in a reverse polish notation.
The answer and all the intermediate calculations can be represented in a 32-bit integer.


```python
class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = []
        operations = {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: int(a / b)
        }
        for token in tokens:
            if token in operations:
                b = stack.pop()
                a = stack.pop()
                stack.append(operations[token](a, b))
            else:
                stack.append(int(token))
        return stack[0]

```


##  **Majority Element**

Описание:
Given an array nums of size n, return the majority element.

The majority element is the element that appears more than ⌊n / 2⌋ times. You may assume that the majority element always exists in the array.


```python
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        max_count = len(nums)//2
        max_num = 0
        nums_set = set(nums)
        for num in nums_set:
            if nums.count(num) > max_count:
                max_count = nums.count(num)
                max_num = num
        return max_num
```


##   **Sort Colors**

Описание:
Given an array nums with n objects colored red, white, or blue, sort them in-place so that objects of the same color are adjacent, with the colors in the order red, white, and blue.

We will use the integers 0, 1, and 2 to represent the color red, white, and blue, respectively.

You must solve this problem without using the library's sort function.


```python
class Solution:
    def sortColors(self, nums: List[int]) -> None:
        
        Do not return anything, modify nums in-place instead.
        
        
        left, current, right = 0, 0, len(nums) - 1

        while current <= right:
            if nums[current] == 0: nums[left], nums[current], left, current = nums[current], nums[left], left + 1, current + 1
            elif nums[current] == 2: nums[current], nums[right], right = nums[right], nums[current], right - 1
            else: current += 1
        
```


##   **Top K Frequent Elements**

Описание:
Given an integer array nums and an integer k, return the k most frequent elements. You may return the answer in any order.


```python
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        count = {}
        for num in nums:
            count[num] = count.get(num, 0) + 1

        bs = [[] for _ in range(len(nums) + 1)]
        for num, freq in count.items():
            bs[freq].append(num)

        result = []
        for b in reversed(bs):
            result.extend(b)
            if len(result) >= k:
                break

        return result[:k]
```
