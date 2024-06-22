## Задание №3

Дана строка s, найдите длину самой длинной подстроки без повторяющихся символов.

### Решение:

Чтобы найти длину самой длинной подстроки без повторяющихся символов, будем использовать технику скользящего окна с набором (set) для отслеживания уникальных символов в текущем окне.

Для этого:
Используем два указателя для представления текущего окна символов. Расширяем окно, перемещая правый указатель. Если символ повторяется, сужаем окно, перемещая левый указатель, пока символ не перестанет повторяться. И Отслеживаем максимальную длину окна в процессе выполнения.

```typescript
function lengthOfLongestSubstring(s: string): number {
  const n = s.length;
  let maxLength = 0;
  let left = 0;
  const charSet = new Set<string>();

  for (let right = 0; right < n; right++) {
    while (charSet.has(s[right])) {
      charSet.delete(s[left]);
      left++;
    }
    charSet.add(s[right]);
    maxLength = Math.max(maxLength, right - left + 1);
  }

  return maxLength;
}
```
