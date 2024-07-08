from typing import Callable
import inspect


def get_function_parameters(func: Callable):
    return inspect.signature(func).parameters
