"""numpy implementation of image filters"""
from __future__ import annotations
from PIL import Image
import numpy as np


def numpy_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    image_float = image.astype(np.float32)

    # Hint: use numpy slicing in order to have fast vectorized code

    gray_image = np.round(image_float[:,:,0] * 0.21 + image_float[:,:,1] * 0.72 + image_float[:,:,2] * 0.07).astype(np.uint8)

    gray_image = gray_image.astype(np.uint8)
    # Return image (make sure it's the right type!)
    return gray_image


def numpy_color2sepia(image: np.array, k: float = 1) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
        k (float): amount of sepia (optional)

    The amount of sepia is given as a fraction, k=0 yields no sepia while
    k=1 yields full sepia.

    Returns:
        np.array: sepia_image
    """
    if not 0 <= k <= 1:
        # validate k
        raise ValueError(f"k must be between [0-1], got {k=}")

    # Initialize sepia_image
    sepia_image = np.empty_like(image, dtype=np.uint8)

    # Define sepia matrix
    base_matrix = np.array([
    [0.393, 0.769, 0.189],
    [0.349, 0.686, 0.168],
    [0.272, 0.534, 0.131]
    ])

    # Incorporate the k factor. When k=1, sepia_matrix = base_matrix. 
    # When k=0, sepia_matrix is an identity matrix (no change to image).
    sepia_matrix = k * base_matrix + (1 - k) * np.identity(3)

    # Apply the matrix filter using Einstein summation for matrix multiplication
    sepia_image = np.einsum('...i,ij->...j', image, sepia_matrix.T) # Transponating the matrix
    
    # Clip the values between 0 and 255
    sepia_image = np.clip(sepia_image, 0, 255).astype(np.uint8)

    # Return the sepia_image
    return sepia_image
'''
if __name__ == "__main__":
    input_image_array = np.array(Image.open("test/rain.jpg"))
   
    gray_array = numpy_color2gray(input_image_array)

    image = Image.fromarray(gray_array, "L")  # "L" mode for grayscale images
    image.save("rain_gray.jpg")

import matplotlib.pyplot as plt
if __name__ == "__main__":
    input_image_array = np.array(Image.open("test/rain.jpg"))
    sepia_array = numpy_color2sepia(input_image_array)

    # Save the sepia image
    image = Image.fromarray(sepia_array.astype('uint8'), "RGB")  # "RGB" mode for color images
    image.save("rain_sepia.jpg")

    reloaded_image = Image.open("rain_sepia.jpg")
    plt.imshow(reloaded_image)
    plt.show()
'''


   
