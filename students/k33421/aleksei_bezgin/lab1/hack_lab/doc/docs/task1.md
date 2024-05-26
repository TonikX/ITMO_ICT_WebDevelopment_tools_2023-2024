# Первое задание

| approach        | mean time +- std (sec) |
|-----------------|----------------------|
| naive           | 1.33 +- 0.02         |
| threading       | 1.37 +- 0.03         |
| multiprocessing | 	0.44 +- 0.01        |
| asyncio         |     1.33 +- 0.01     |

Тут с заметным успехом всех обыгрывает multiprocessing.
Threading находится на уровне naive из-за CPU/bound операций и тратами на context switching.
Причины провала asyncio мне неизвестны.