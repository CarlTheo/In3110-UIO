"""Command-line (script) interface to instapy"""
from __future__ import annotations

import argparse
import sys

import in3110_instapy
import numpy as np
from PIL import Image

from . import io
from in3110_instapy.timing import time_one
from in3110_instapy import python_filters
from in3110_instapy import numpy_filters
from in3110_instapy import numba_filters


def run_filter(
    file: str,
    out_file: str = None,
    implementation: str = "python",
    filter: str = "color2gray",
    scale: int = 1,
    runtime: bool = False  # <-- Add this flag
) -> None:

    """Run the selected filter"""
    # load the image from a file
    image = Image.open(file)
    if scale != 1:
        # Resize image, if needed
        new_size = (int(image.width * scale), int(image.height * scale))
        image = image.resize(new_size, Image.ANTIALIAS)

    filter_functions = {
    "color2gray": {
        "python": python_filters.python_color2gray,
        "numba": numba_filters.numba_color2gray_wrapper,    
        "numpy": numpy_filters.numpy_color2gray     
    },
    "color2sepia": {
        "python": python_filters.python_color2sepia, 
        "numba": numba_filters.numba_color2sepia_wrapper,    
        "numpy": numpy_filters.numpy_color2sepia     
    }
}

    filter_function = filter_functions[filter][implementation]
    
    # If runtime flag is raised, compute and print the average runtime
    if runtime:
        avg_runtime = time_one(filter_function, image, calls=3)
        print(f"Average time over 3 runs: {avg_runtime}s")

    filtered = filter_function(image)
    
    if out_file:
        out_image = Image.fromarray(filtered)
        out_image.save(out_file)
        
    else:
        # not asked to save, display it
        io.display(filtered)

def main(argv=None):
    """Parse the command-line and call run_filter with the arguments"""
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Apply image filters using different implementations")

    # filename is positional and required
    parser.add_argument("file", help="The filename to apply filter to")

    # Output file argument
    parser.add_argument("-o", "--out", help="The output filename", default=None)

    # Filter type arguments
    filter_group = parser.add_mutually_exclusive_group(required=True)
    filter_group.add_argument("-g", "--gray", action="store_true", help="Select gray filter")
    filter_group.add_argument("-se", "--sepia", action="store_true", help="Select sepia filter")

    # Bonus -r task
    parser.add_argument("-r", "--runtime", action="store_true", help="Track the average runtime of the chosen implementation.")
    
    # Scale argument
    parser.add_argument("-sc", "--scale", type=float, help="Scale factor to resize image", default=1)

    # Implementation type
    parser.add_argument("-i", "--implementation", choices=["python", "numba", "numpy"], 
                        help="The implementation", default="python")

    args = parser.parse_args(argv)

    # Check which filter was selected and call the respective function
    if args.gray:
        filter = "color2gray"
    else:
        filter = "color2sepia"

    run_filter(args.file, out_file=args.out, implementation=args.implementation, filter=filter, scale=args.scale, runtime=args.runtime)