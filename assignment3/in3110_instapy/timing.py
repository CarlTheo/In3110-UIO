from __future__ import annotations

import time
from typing import Callable

from . import get_filter, io

from in3110_instapy import python_filters
from in3110_instapy import numpy_filters
from in3110_instapy import numba_filters

def time_one(filter_function: Callable, *arguments, calls: int = 3) -> float:
    """Return the time for one call

    When measuring, repeat the call `calls` times,
    and return the average.

    Args:
        filter_function (callable):
            The filter function to time
        *arguments:
            Arguments to pass to filter_function
        calls (int):
            The number of times to call the function,
            for measurement
    Returns:
        time (float):
            The average time (in seconds) to run filter_function(*arguments)
    """
    start_time = time.time()
    for _ in range(calls):
        filter_function(*arguments)
    end_time = time.time()
    average_time = (end_time - start_time) / calls
    return average_time

    # run the filter function `calls` times
    # return the _average_ time of one call
    ...

def make_reports(filename: str = "test/rain.jpg", calls: int = 3):
    """
    Make timing reports for all implementations and filters,
    run for a given image.

    Args:
        filename (str): the image file to use
    """

    # load the image
    image = io.read_image(filename)

    # iterate through the filters
    filter_names = ["color2gray", "color2sepia"]
    for filter_name in filter_names:
        # get the reference filter function
        reference_filter = get_filter(filter_name, "python")
        # time the reference implementation
        reference_time = time_one(reference_filter, image, calls=calls)
        print(
            f"Reference (pure Python) filter time {filter_name}: {reference_time:.3}s ({calls=})"
        )
        # iterate through the implementations
        implementations = ["numpy", "numba"]
        for implementation in implementations:
            filter_func = get_filter(filter_name, implementation)
            # time the filter
            filter_time = time_one(filter_func, image, calls=calls)
            # compare the reference time to the optimized time
            speedup = reference_time / filter_time if filter_time != 0 else float('inf')
            print(
                f"Timing: {implementation} {filter_name}: {filter_time:.7}s ({speedup=:.2f}x)"
            )

if __name__ == "__main__":
    # run as `python -m in3110_instapy.timing`
    make_reports()


