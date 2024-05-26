# Task2

| approach        | mean time +- std (sec) |
|-----------------|------------------------|
| naive           | 20.01 +- 1.25          |
| threading       | 5.11 +- 0.95           |
| multiprocessing | 	4.0 +- 0.62           |
| asyncio         | 2.06 +- 1.64           |

Здесь использование threading уже оправдано, но multiprocessing все равно круче.
Выигрвывает же asyncio, однако, он же показывает наибольшую волатильность.
