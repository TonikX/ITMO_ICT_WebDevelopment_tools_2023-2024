## Задание №15

Даны n пар скобок, напишите функцию, которая генерирует все комбинации корректно сформированных скобок.

### Решение:

Для решения задачи будем использовать метод backtracking для генерации всех возможных комбинаций корректно сформированных скобок.

```typescript
function generateParenthesis(n: number): string[] {
  const result: string[] = [];

  const backtrack = (current: string, open: number, close: number) => {
    if (current.length === 2 * n) {
      result.push(current);
      return;
    }

    if (open < n) {
      backtrack(current + "(", open + 1, close);
    }

    if (close < open) {
      backtrack(current + ")", open, close + 1);
    }
  };

  backtrack("", 0, 0);
  return result;
}
```
