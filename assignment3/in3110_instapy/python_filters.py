"""pure Python implementation of image filters"""
from __future__ import annotations

import numpy as np


def python_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    
    # iterate through the pixels, and apply the grayscale transform

    rows, cols, _ = image.shape
    gray_image = np.empty((rows, cols), dtype=np.float64)
  
    for i in range(rows):
        for j in range(cols):
            r, g, b = image[i, j]
            gray = int(r * 0.21 + g * 0.72 + b * 0.07)
            gray_image[i, j] = gray
    ...
    gray_image = gray_image.astype(np.uint8)
    return gray_image


def python_color2sepia(image: np.array) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
    sepia_image = np.empty_like(image)
    height, width, _ = image.shape
    # Iterate through the pixels
    for y in range(height):
        for x in range(width):
            r, g, b = image[y, x]
    # applying the sepia matrix
            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)
            sepia_image[y, x] = [min(255, tr), min(255, tg), min(255, tb)]
    # Return image
    # don't forget to make sure it's the right type!
    return sepia_image

