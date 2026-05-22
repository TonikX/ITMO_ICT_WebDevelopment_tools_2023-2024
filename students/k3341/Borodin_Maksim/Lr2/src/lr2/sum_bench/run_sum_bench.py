from lr2.common.metrics import save_metrics
from lr2.sum_bench.async_sum import run as run_async
from lr2.sum_bench.multiprocessing_sum import run as run_multiprocessing
from lr2.sum_bench.threading_sum import run as run_threading


def main() -> None:
    results = [run_threading(), run_multiprocessing(), run_async()]
    for item in results:
        print(
            f"{item['mode']:>15}: result={item['result']}, "
            f"workers={item['workers']}, elapsed={item['elapsed_sec']:.6f}s"
        )
    path = save_metrics("sum_bench", {"task": "sum_1_to_1000000", "results": results})
    print(f"saved metrics: {path}")


if __name__ == "__main__":
    main()
