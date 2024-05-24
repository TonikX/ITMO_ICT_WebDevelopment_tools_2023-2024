# Leetcode
24.03.2024 - 07.05.2024 = 6 weeks
![leetcode.png](src%2Fleetcode.png)

## 3sum
```python
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        res = set()
        n, p, z = [], [], []
        for num in nums:
            if num > 0:
                p.append(num)
            elif num < 0: 
                n.append(num)
            else:
                z.append(num)
        N, P = set(n), set(p)
        if z:
            for num in P:
                if -1*num in N:
                    res.add((-1*num, 0, num))
        if len(z) >= 3:
            res.add((0,0,0))
        for i in range(len(n)):
            for j in range(i+1,len(n)):
                target = -1*(n[i]+n[j])
                if target in P:
                    res.add(tuple(sorted([n[i],n[j],target])))
        for i in range(len(p)):
            for j in range(i+1,len(p)):
                target = -1*(p[i]+p[j])
                if target in N:
                    res.add(tuple(sorted([p[i],p[j],target])))

        return res
```

## Group Anagrams
```python
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        result = []
        sorted_s = {}
        i = 0
        for s in strs:
            if not result:
                sorted_s[''.join(sorted(s))] = i
                i += 1
                result.append([s])
                continue
            for j in range(len(result)):
                if (''.join(sorted(s))) in sorted_s:
                    result[sorted_s[''.join(sorted(s))]].append(s)
                    break
                else:
                    sorted_s[''.join(sorted(s))] = i
                    i += 1
                    result.append([s])
                    break
        return result
```

## Longest Substring Without Repeating Characters
```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        n = len(s)
        maxLength = 0
        charIndex = [-1] * 128
        left = 0
        
        for right in range(n):
            if charIndex[ord(s[right])] >= left:
                left = charIndex[ord(s[right])] + 1
            charIndex[ord(s[right])] = right
            maxLength = max(maxLength, right - left + 1)
        
        return maxLength
```

## Longest Palindromic Substring
```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        if not s:
            return ""

        def expand_around_center(s: str, left: int, right: int):
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            return right - left - 1


        start = 0
        end = 0

        for i in range(len(s)):
            odd = expand_around_center(s, i, i)
            even = expand_around_center(s, i, i + 1)
            max_len = max(odd, even)
            
            if max_len > end - start:
                start = i - (max_len - 1) // 2
                end = i + max_len // 2
        
        return s[start:end+1]
```

## Increasing Triplet Subsequence
```python
class Solution:
    def increasingTriplet(self, nums: List[int]) -> bool:
        first = second = float('inf') 
        for n in nums: 
            if n <= first: 
                first = n
            elif n <= second:
                second = n
            else:
                return True
        return False
```

## Set Matrix Zeroes
```python
class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        m = len(matrix)
        n = len(matrix[0])
        shouldFillFirstRow = 0 in matrix[0]
        shouldFillFirstCol = 0 in list(zip(*matrix))[0]
        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][j] == 0:
                    matrix[i][0] = 0
                    matrix[0][j] = 0
        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][0] == 0 or matrix[0][j] == 0:
                    matrix[i][j] = 0
        if shouldFillFirstRow:
            matrix[0] = [0] * n
        if shouldFillFirstCol:
            for row in matrix:
                row[0] = 0
        
```