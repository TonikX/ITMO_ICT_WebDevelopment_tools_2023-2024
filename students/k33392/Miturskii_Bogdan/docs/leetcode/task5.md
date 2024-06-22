## Задание №5

Дан целочисленный массив `nums`, вернуть `true`, если существует тройка индексов \( (i, j, k) \) такая, что \( i < j < k \) и \( nums[i] < nums[j] < nums[k] \). Если таких индексов не существует, вернуть `false`.

### Решение:

Используем два указателя для отслеживания первых двух минимальных чисел. Проходим по массиву и обновляем эти указатели. Если находим число больше второго указателя, возвращаем true.

```typescript
function increasingTriplet(nums: number[]): boolean {
  let first = Number.MAX_SAFE_INTEGER;
  let second = Number.MAX_SAFE_INTEGER;

  for (const num of nums) {
    if (num <= first) {
      first = num;
    } else if (num <= second) {
      second = num;
    } else {
      return true;
    }
  }

  return false;
}
```
