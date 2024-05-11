from pathlib import Path
import os
import statistics
import subprocess

LOOPS_COUNT = 10
# TEST_PATH = "./thread.py"
TEST_PATH = "./process.py"


def get_time_info(text):
    info = list(
        map(
            lambda line: float(line.split(" ")[1]),
            text.split("\n")[:-2],
        )
    )
    return (info[0], info[1])


def main():
    results_real = []
    results_user = []
    runner = Path(os.path.dirname(os.path.realpath(__file__))) / TEST_PATH

    for _ in range(LOOPS_COUNT):
        process = subprocess.Popen(
            ["time", "-p", "python", runner],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        _, stderr = process.communicate()
        info = get_time_info(stderr.decode("utf-8"))

        results_real.append(info[0])
        results_user.append(info[1])

    print(
        f"real: {round(statistics.median(results_real),2)}\nuser: {round(statistics.median(results_user), 2)}"
    )


if __name__ == "__main__":
    main()
