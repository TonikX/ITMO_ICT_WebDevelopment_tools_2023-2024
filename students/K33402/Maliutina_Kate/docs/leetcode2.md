# Решения задач
## 2. Add Two Numbers
```python
class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        dummyHead = ListNode(0)
        tail = dummyHead
        carry = 0
        while l1 is not None or l2 is not None or carry != 0:
            digit1 = l1.val if l1 is not None else 0
            digit2 = l2.val if l2 is not None else 0
            sum = digit1 + digit2 + carry
            digit = sum % 10
            carry = sum // 10
            newNode = ListNode(digit)
            tail.next = newNode
            tail = tail.next
            l1 = l1.next if l1 is not None else None
            l2 = l2.next if l2 is not None else None
        result = dummyHead.next
        dummyHead.next = None
        return result
```
![leetcode2.png](src%2Fleetcode2.png)
## 38. Count and Say
```python
class Solution:
    def countAndSay(self, n: int) -> str:
        say = "1"
        for i in range(2, n + 1):
            temp = ""
            num = say[0]
            count = 1
            for i in range(1, len(say)):
                curr_num = say[i]
                if num == curr_num:
                    count += 1
                else:
                    temp += str(count) + str(num)
                    num = curr_num
                    count = 1
            temp += str(count) + str(num)
            say = temp
        return say
```
![leetcode1.png](src%2Fleetcode1.png)
## 328. Odd Even Linked List
```python
class Solution:
    def oddEvenList(self, head: Optional[ListNode]) -> Optional[ListNode]:
       if not head: 
        return None
       odd = head
       evenHead = even = head.next
       while even and even.next:
           odd.next = odd.next.next
           odd = odd.next
           even.next = even.next.next
           even = even.next
       odd.next = evenHead
       return head
```
![leetcode3.png](src%2Fleetcode3.png)