from time import time
from typing import Tuple, Callable, Any
from db import init_db
import logging


def bootstrap_environment(log_file: str = None) -> None:
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO, format="\x1b[38;20m%(name)s %(asctime)s %(levelname)s %(message)s\x1b[0m"
    )
    init_db()


def get_function_execution_time_sec(func: Callable, *args) -> Tuple[float, Any]:
    start = time()
    func_return_value = func(*args)

    return time() - start, func_return_value


async def get_function_execution_time_sec_async(func: Callable, *args) -> Tuple[float, Any]:
    start = time()
    return_value = await func(*args)
    return time() - start, return_value
