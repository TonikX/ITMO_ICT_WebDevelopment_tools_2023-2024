## Задание №6

Последовательность "count-and-say" — это последовательность строк цифр, определенная рекурсивной формулой:

countAndSay(1) = "1"

countAndSay(n) — это кодировка длины серий (run-length encoding) для countAndSay(n - 1).

Run-length encoding (RLE) — это метод сжатия строк, который работает путем замены последовательных одинаковых символов (повторяющихся 2 и более раз) на конкатенацию символа и числа, обозначающего количество этих символов. Например, для сжатия строки "3322251" мы заменяем "33" на "23", "222" на "32", "5" на "15" и "1" на "11". Таким образом, сжатая строка становится "23321511".

Дан положительный целочисленный n, вернуть n-й элемент последовательности "count-and-say".

### Решение:

Начнем с базового случая: countAndSay(1) = "1". Для каждого следующего элемента будем генерировать строку с использованием кодировки длины серий (RLE) предыдущего элемента. Повторяем процесс до достижения n-го элемента.

```typescript
function countAndSay(n: number): string {
  if (n === 1) return "1";

  const previousTerm = countAndSay(n - 1);
  let result = "";
  let count = 0;
  let currentChar = previousTerm[0];

  for (let char of previousTerm) {
    if (char === currentChar) {
      count++;
    } else {
      result += count.toString() + currentChar;
      currentChar = char;
      count = 1;
    }
  }

  result += count.toString() + currentChar;

  return result;
}
```
