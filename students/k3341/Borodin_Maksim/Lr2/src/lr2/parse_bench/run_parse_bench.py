from lr2.common.metrics import save_metrics
from lr2.parse_bench.async_parse import run as run_async
from lr2.parse_bench.multiprocessing_parse import run as run_multiprocessing
from lr2.parse_bench.threading_parse import run as run_threading


def main() -> None:
    results = [run_threading(), run_multiprocessing(), run_async()]
    compact = []
    for item in results:
        success_count = sum(1 for row in item["results"] if row["status"] == "success")
        total_count = len(item["results"])
        compact_item = {
            "mode": item["mode"],
            "elapsed_sec": item["elapsed_sec"],
            "success_count": success_count,
            "total_count": total_count,
        }
        compact.append(compact_item)
        print(
            f"{item['mode']:>15}: elapsed={item['elapsed_sec']:.6f}s, "
            f"success={success_count}/{total_count}"
        )
    path = save_metrics("parse_bench", {"task": "parse_and_save", "results": compact})
    print(f"saved metrics: {path}")


if __name__ == "__main__":
    main()
