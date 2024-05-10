from typing import TypedDict, List
from pathlib import Path
import os
import statistics
import subprocess


class BecnhParams(TypedDict):
    target_sum: int
    split_count: int
    runner: Path

SEPARATOR = '-'*30

class BenchRunner:
    tests: List[BecnhParams]
    loops: int

    def __init__(self, tests: List[BecnhParams], loops: int) -> None:
        self.tests = tests
        self.loops = loops

    def run(self):
        dir_path = Path(os.path.dirname(os.path.realpath(__file__)))

        for test in self.tests:
            runner = dir_path / test["runner"]
            print(f"{test["runner"]} loops = {self.loops} target_sum = {test['target_sum']} split_count = {test['split_count']}")

            results_real = []
            results_user = []

            for _ in range(self.loops):
                process = subprocess.Popen(["time", "-p", "python", runner, f"--target_sum={test['target_sum']}", f"--split_count={test['split_count']}"],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                _, stderr = process.communicate()
                info = list(map(lambda line: float(line.split(" ")[1]), stderr.decode('utf-8').split('\n')[:-2]))
                results_real.append(info[0])
                results_user.append(info[1])
            
            print(f"real: {statistics.median(results_real)}\nuser: {statistics.median(results_user)}")

            print(f'{SEPARATOR}\n')
