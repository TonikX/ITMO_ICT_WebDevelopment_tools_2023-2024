## Задание №16

Дан целочисленный массив nums из уникальных элементов. Необходимо вернуть все возможные подмножества (множество мощностей). Набор решений не должен содержать повторяющихся подмножеств. Вернуть решение в любом порядке.

### Решение:

Для решения задачи будем использовать метод backtracking для генерации всех возможных подмножеств.

```typescript
function subsets(nums: number[]): number[][] {
  const result: number[][] = [];

  const backtrack = (start: number, currentSubset: number[]) => {
    result.push([...currentSubset]);

    for (let i = start; i < nums.length; i++) {
      currentSubset.push(nums[i]);
      backtrack(i + 1, currentSubset);
      currentSubset.pop();
    }
  };

  backtrack(0, []);
  return result;
}
```
