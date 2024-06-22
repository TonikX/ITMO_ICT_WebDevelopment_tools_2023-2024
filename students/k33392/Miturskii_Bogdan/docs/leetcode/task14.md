## Задание №14

Дана строка, содержащая цифры от 2 до 9 включительно. Необходимо вернуть все возможные комбинации букв, которые могут представлять это число. Вернуть ответ в любом порядке.

Соответствие цифр буквам (как на телефонных кнопках) приведено ниже. Обратите внимание, что цифра 1 не соответствует никаким буквам.

### Решение:

Для решения задачи будем использовать рекурсию и backtracking для генерации всех возможных комбинаций букв для данной строки цифр.

```typescript
function letterCombinations(digits: string): string[] {
  if (digits.length === 0) return [];

  const phoneMap: { [key: string]: string[] } = {
    "2": ["a", "b", "c"],
    "3": ["d", "e", "f"],
    "4": ["g", "h", "i"],
    "5": ["j", "k", "l"],
    "6": ["m", "n", "o"],
    "7": ["p", "q", "r", "s"],
    "8": ["t", "u", "v"],
    "9": ["w", "x", "y", "z"],
  };

  const result: string[] = [];

  const backtrack = (combination: string, nextDigits: string) => {
    if (nextDigits.length === 0) {
      result.push(combination);
    } else {
      let digit = nextDigits[0];
      let letters = phoneMap[digit];
      for (let i = 0; i < letters.length; i++) {
        backtrack(combination + letters[i], nextDigits.slice(1));
      }
    }
  };

  backtrack("", digits);
  return result;
}
```
