# ЛР2 — Потоки, Процессы, Асинхронность

## Цель
сравнить подходы `threading`, `multiprocessing` и `asyncio` на двух практических задачах:
- сумма чисел от 1 до 1_000_000
- параллельный парсинг страниц с сохранением результатов в бд

## Реализация
- проект: `students/k3341/Borodin_Maksim/Lr2`
- бд используется из ЛР1 через `DATABASE_URL`
- для хранения результатов парсинга добавлена таблица `parsed_pages` в ЛР1 (миграция `20260522_0002`)

## Задача 1 — сумма 1..1_000_000
файлы:
- `students/k3341/Borodin_Maksim/Lr2/src/lr2/sum_bench/threading_sum.py`
- `students/k3341/Borodin_Maksim/Lr2/src/lr2/sum_bench/multiprocessing_sum.py`
- `students/k3341/Borodin_Maksim/Lr2/src/lr2/sum_bench/async_sum.py`
- общий запуск: `students/k3341/Borodin_Maksim/Lr2/src/lr2/sum_bench/run_sum_bench.py`

результаты замеров (`Lr2/results/sum_bench.json`):

| Подход | Время, сек | Результат |
|---|---:|---:|
| threading | 0.004362 | 500000500000 |
| multiprocessing | 0.078012 | 500000500000 |
| async | 0.006613 | 500000500000 |

краткий вывод:
- для этой cpu-задачи на небольшом объеме оверхед процессов выше, чем выгода параллелизма
- threading и async в данном варианте быстрее за счет малого накладного времени
- сумма во всех трех реализациях совпадает

## Задача 2 — параллельный парсинг + сохранение в бд
файлы:
- `students/k3341/Borodin_Maksim/Lr2/src/lr2/parse_bench/threading_parse.py`
- `students/k3341/Borodin_Maksim/Lr2/src/lr2/parse_bench/multiprocessing_parse.py`
- `students/k3341/Borodin_Maksim/Lr2/src/lr2/parse_bench/async_parse.py`
- общий запуск: `students/k3341/Borodin_Maksim/Lr2/src/lr2/parse_bench/run_parse_bench.py`

используемые url:
- `students/k3341/Borodin_Maksim/Lr2/src/lr2/parse_bench/urls.py`

результаты замеров (`Lr2/results/parse_bench.json`):

| Подход | Время, сек | Успешно |
|---|---:|---:|
| threading | 5.297605 | 5/6 |
| multiprocessing | 15.476725 | 4/6 |
| async | 7.637431 | 5/6 |

сводка по записям в таблице `parsed_pages` после прогона:

| Подход | success | failed |
|---|---:|---:|
| threading | 5 | 1 |
| multiprocessing | 4 | 2 |
| async | 5 | 1 |

краткий вывод:
- на сетевой задаче лучший результат в этом прогоне у threading
- async показал сопоставимое время и стабильную обработку большинства url
- multiprocessing оказался самым медленным из-за накладных расходов и нестабильности части запросов в конкретном запуске

## Как запустить
из папки `students/k3341/Borodin_Maksim`:

```bash
make -C Lr1 up-db
make -C Lr1 migrate
make -C Lr2 install
make -C Lr2 sum-all
make -C Lr2 parse-all
```

результаты сохраняются в:
- `students/k3341/Borodin_Maksim/Lr2/results/sum_bench.json`
- `students/k3341/Borodin_Maksim/Lr2/results/parse_bench.json`
