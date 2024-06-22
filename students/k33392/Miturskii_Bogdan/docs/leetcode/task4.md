## Задание №4

Дана строка s, верните самую длинную подстроку-палиндром в s.

### Решение:

Используем два указателя для проверки подстрок. Проверяем палиндромы для каждого символа строки, используя два возможных центра: один символ и два соседних символа.

```typescript
function longestPalindrome(s: string): string {
  if (s.length === 0) return "";
  let start = 0,
    end = 0;

  const expandAroundCenter = (
    s: string,
    left: number,
    right: number
  ): number => {
    while (left >= 0 && right < s.length && s[left] === s[right]) {
      left--;
      right++;
    }
    return right - left - 1;
  };

  for (let i = 0; i < s.length; i++) {
    const len1 = expandAroundCenter(s, i, i);
    const len2 = expandAroundCenter(s, i, i + 1);
    const len = Math.max(len1, len2);

    if (len > end - start) {
      start = i - Math.floor((len - 1) / 2);
      end = i + Math.floor(len / 2);
    }
  }

  return s.substring(start, end + 1);
}
```
