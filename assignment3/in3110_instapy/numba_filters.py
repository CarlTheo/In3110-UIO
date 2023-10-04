"""numba-optimized filters"""
from __future__ import annotations

from PIL import Image
import numpy as np
from numba import jit
# These are used for computing things no python can't handle::::::::::::::::::::::
def convert_to_numpy(image_input) -> np.array:
    """Convert the input to a numpy array if it's a PIL Image."""
    if isinstance(image_input, Image.Image):
        return np.array(image_input)
    return image_input

def numba_color2sepia_wrapper(image_input):
    """Wrapper function to handle the conversion and then call the Numba function."""
    image = convert_to_numpy(image_input)
    return numba_color2sepia(image)

def numba_color2gray_wrapper(image_input):
    image = convert_to_numpy(image_input)
    return numba_color2gray(image)
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

@jit(nopython = True)
def numba_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    rows, cols, _ = image.shape
    gray_image = np.empty((rows, cols), dtype = np.float64)
    # iterate through the pixels, and apply the grayscale transform
 
    for i in range(rows):
        for j in range(cols):
            r, g, b = image[i, j]
            gray = int(r * 0.21 + g * 0.72 + b * 0.07)
            gray_image[i, j] = gray
    ...

    gray_image = gray_image.astype(np.uint8)

    return gray_image

@jit(nopython = True)
def numba_color2sepia(image: np.array) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
    sepia_image = np.empty_like(image)
    height, width, _ = image.shape

    for y in range(height):
        for x in range(width):
            r, g, b = image[y, x]
            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)
            sepia_image[y, x] = [min(255, tr), min(255, tg), min(255, tb)]

    return sepia_image
