"""pure Python implementation of image filters"""
from __future__ import annotations
from PIL import Image
import numpy as np

def python_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
     # Convert PIL Image to numpy array
    image_np = np.asarray(image)
    
    # iterate through the pixels, and apply the grayscale transform
    rows, cols, _ = image_np.shape
    gray_image = np.empty((rows, cols), dtype=np.uint8)

    for i in range(rows):
        for j in range(cols):
            r, g, b = image_np[i, j]
            gray = int(r * 0.21 + g * 0.72 + b * 0.07)
            gray_image[i, j] = gray

    return gray_image

def python_color2sepia(image: np.array) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
    if isinstance(image, Image.Image):
        image = np.array(image)
    
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
'''
from PIL import Image
import matplotlib.pyplot as plt
if __name__ == "__main__":
    input_image_array = np.array(Image.open("test/rain.jpg"))
    sepia_array = python_color2sepia(input_image_array)

    # Save the sepia image
    image = Image.fromarray(sepia_array.astype('uint8'), "RGB")  # "RGB" mode for color images
    image.save("rain_sepia.jpg")

    reloaded_image = Image.open("rain_sepia.jpg")
    plt.imshow(reloaded_image)
    plt.show()
'''