## Задание №2 Найти все уникальные тройки, сумма которых равна нулю

Дан массив строк strs, сгруппируйте анаграммы вместе. Ответ можно вернуть в любом порядке.

Анаграмма — это слово или фраза, образованные путем перестановки букв другого слова или фразы, обычно с использованием всех исходных букв ровно один раз.

### Решение:

Создадим словарь для хранения сгруппированных анаграм. Отсортируем каждую строку, чтобы получить ключ. Используем этот ключ для группировки в изначальном словаре

```typescript
function groupAnagrams(strs: string[]): string[][] {
  const anagramMap: { [key: string]: string[] } = {};

  for (const str of strs) {
    const sortedStr = str.split("").sort().join("");

    if (!anagramMap[sortedStr]) {
      anagramMap[sortedStr] = [];
    }

    anagramMap[sortedStr].push(str);
  }

  return Object.values(anagramMap);
}
```
