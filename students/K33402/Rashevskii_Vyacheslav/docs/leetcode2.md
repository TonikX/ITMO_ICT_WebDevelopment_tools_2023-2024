# Leetcode
13.05.2024 - 24.05.2024 = 2 weeks
1 more for extra point

## Count and Say
```python
class Solution:
    def countAndSay(self, n: int) -> str:
        def count_til_diff(s: str):
            res = ''
            i = 0
            temp = ''
            while i < len(s):
                count = 1
                check = s[i]
                if (check == temp):
                    break
                temp = check
                for j in range(i + 1, len(s)):  
                    if s[j] != check:
                        i = j
                        break
                    
                    count += 1

                    if j == len(s) - 1:
                        i = j
                        break
                res += str(count) + check
            return res
    
        if n == 1:
            return '1'
        return count_til_diff(self.countAndSay(n - 1))
```

## Add Two Numbers
```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode()
        res = dummy
        total = carry = 0
        while l1 or l2 or carry:
            total = carry
            if l1:
                total += l1.val
                l1 = l1.next
            if l2:
                total += l2.val
                l2 = l2.next
            num = total % 10
            carry = total // 10
            dummy.next = ListNode(num)
            dummy = dummy.next
        return res.next
```

## Odd Even Linked List
```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def oddEvenList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head == None or head.next == None : return head 
        odd = ListNode(0) 
        odd_ptr = odd
        even = ListNode(0)
        even_ptr = even 
        idx = 1 
        while head != None :
            if idx % 2 == 0:
                even_ptr.next = head
                even_ptr = even_ptr.next
            else:
                odd_ptr.next = head
                odd_ptr = odd_ptr.next
            head = head.next
            idx+=1
        even_ptr.next = None
        odd_ptr.next = even.next
        return odd.next
```
