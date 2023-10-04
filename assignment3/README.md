# in3110_instapy

## Overview

`in3110_instapy` is a Python package that allows users to apply various image filters, including grayscale and sepia, using multiple implementations such as pure Python, Numba, and NumPy. This package is especially useful for those looking to quickly enhance their images through filters and measure the performance of different implementation techniques.

## Installation

To install `in3110_instapy`, follow the steps below:

1. Clone the repository to your local machine:

```bash
git clone <RepoCopy>
```

2. Navigate to the directory:

```bash
cd in3110_instapy
```

3. Install the pacage:

```bash
pip install .
```
 ## Usage

 To use the in3110_instapy package:

 1. Apply the filter to your image:
 
 ```bash
 python3 -m in3110_instapy <filename> -i <implementation> -g  # for grayscale
 ```

 or

 ```bash
 python3 -m in3110_instapy <filename> -i <implementation> -se  # for sepia
 ```

 2. Additional flags: 
 -sc can be used to scale the image, -o to specify the output filename, and -r to track the runtime. 
 For a full list of options and their descriptions, use:
```bash
python3 -m in3110_instapy --help
```
