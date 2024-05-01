from .bench import BenchRunner
from pathlib import Path
import os

TARGET = 100_000_000
LOOPS = 10


def start():
    cpu_count = os.cpu_count() or 1
    runner = BenchRunner(
        tests=[
            {
                "target_sum": TARGET,
                "split_count": 1,
                "runner": Path("./runners/simple.py"),
            },
            {
                "target_sum": TARGET,
                "split_count": cpu_count,
                "runner": Path("./runners/threaded.py"),
            },
            {
                "target_sum": TARGET,
                "split_count": cpu_count,
                "runner": Path("./runners/threaded_pool.py"),
            },
            {
                "target_sum": TARGET,
                "split_count": cpu_count,
                "runner": Path("./runners/multiprocess.py"),
            },
            {
                "target_sum": TARGET,
                "split_count": cpu_count,
                "runner": Path("./runners/async.py"),
            },
        ],
        loops=LOOPS,
    )
    runner.run()
