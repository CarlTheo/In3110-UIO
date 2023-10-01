import numpy as np
from in3110_instapy.numpy_filters import numpy_color2gray, numpy_color2sepia

def test_color2gray():
    # Sample input image 3x3 RGB
    image = np.array([
        [[255, 0, 0], [0, 255, 0], [0, 0, 255]],
        [[255, 255, 0], [0, 255, 255], [255, 0, 255]],
        [[255, 255, 255], [128, 128, 128], [0, 0, 0]]
    ], dtype=np.uint8)

    # Use the function to convert the image to grayscale
    gray_image = numpy_color2gray(image)

    # Corrected grayscale reference values
    reference_gray = np.array([
        [54, 184, 18],  
        [237, 201, 71],  
        [255, 128, 0]
    ], dtype=np.uint8)

    # Assert that the converted gray_image matches the reference_gray
    np.testing.assert_array_equal(gray_image, reference_gray)

def test_color2sepia():
    # Sample input image 3x3 RGB
    image = np.array([
        [[255, 0, 0], [0, 255, 0], [0, 0, 255]],
        [[255, 255, 0], [0, 255, 255], [255, 0, 255]],
        [[255, 255, 255], [128, 128, 128], [0, 0, 0]]
    ], dtype=np.uint8)
    
    # Define sepia matrix for the transformation
    sepia_matrix = np.array([
        [0.393, 0.769, 0.189],
        [0.349, 0.686, 0.168],
        [0.272, 0.534, 0.131]
    ])
    
    # Expected sepia values, based on the sepia_matrix and the input image
    reference_sepia = np.clip(np.einsum('...i,ij->...j', image, sepia_matrix.T), 0, 255).astype(np.uint8)
    
    # Use the function to convert the image to sepia
    sepia_image = numpy_color2sepia(image, k=1)  # We set k=1 for full sepia effect

    # Assert that the converted sepia_image matches the reference_sepia
    np.testing.assert_array_equal(sepia_image, reference_sepia)

