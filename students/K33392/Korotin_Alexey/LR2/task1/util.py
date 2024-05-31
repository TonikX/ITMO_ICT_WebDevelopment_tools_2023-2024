from time import time
from typing import Tuple, Callable, Any


def get_function_execution_time_sec(func: Callable, *args) -> Tuple[float, Any]:
    start = time()
    func_return_value = func(*args)

    return time() - start, func_return_value


async def get_function_execution_time_sec_async(func: Callable, *args) -> Tuple[float, Any]:
    start = time()
    return_value = await func(*args)
    return time() - start, return_value
