import time
import asyncio as aio
from parse_threading import main as threading_main
from parse_mp import main as multiprocessing_main
from parse_aio import main as asyncio_main
from functools import partial

def benchmark(function, name):
    start_time = time.perf_counter()
    function()
    end_time = time.perf_counter()
    print(f"{name} took {end_time - start_time:.4f} seconds")

def main():
    print("Benchmarking threading...")
    benchmark(threading_main, "Threading")

    print("\nBenchmarking multiprocessing...")
    benchmark(multiprocessing_main, "Multiprocessing")

    print("\nBenchmarking asyncio...")
    benchmark(partial(aio.run, asyncio_main()), "Asyncio")

if __name__ == "__main__":
    main()

