from in3110_instapy.python_filters import python_color2gray, python_color2sepia
import numpy as np
import pytest


def test_color2gray(image):
    image = np.array([[[255, 0, 0], [0, 255, 0], [0, 0, 255]],
                    [[255, 255, 0], [0, 255, 255], [255, 0, 255]],
                    [[255, 255, 255], [128, 128, 128], [0, 0, 0]]], dtype=np.uint8)
    # run color2gray
    gray_image = python_color2gray(image)

    # check that the result has the right shape, type
    assert gray_image.shape == (3, 3)
    assert gray_image.dtype == np.uint8

    # assert uniform r,g,b values
    expected_gray_values = [[53, 183, 17], 
                            [237, 201, 71], 
                            [254, 128, 0]]
    for i in range(3):
        for j in range(3):
            assert gray_image[i, j] == expected_gray_values[i][j]

def test_color2sepia():
    # Sample input image 3x3 RGB
    image = np.array([[[255, 0, 0], [0, 255, 0], [0, 0, 255]],
                      [[255, 255, 0], [0, 255, 255], [255, 0, 255]],
                      [[255, 255, 255], [128, 128, 128], [0, 0, 0]]], dtype=np.uint8)
    
    # Run color2sepia
    sepia_image = python_color2sepia(image)

    # Check that the result has the right shape, type
    assert sepia_image.shape == image.shape
    assert sepia_image.dtype == np.uint8

    # Verify individual pixel samples according to the sepia matrix
    # For each sample pixel in the input, apply the sepia matrix transformation
    # and then check against the value in the transformed image
    expected_sepia_values = [
        [[100, 88, 69], [196, 174, 136], [48, 42, 33]],
        [[255, 255, 205], [244, 217, 169], [148, 131, 102]],
        [[255, 255, 238], [172, 153, 119], [0, 0, 0]]
    ]

    for i in range(3):
        for j in range(3):
            np.testing.assert_array_equal(sepia_image[i, j], expected_sepia_values[i][j])