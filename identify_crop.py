import os
from PIL import Image
import numpy as np
import re

def identify_crop_coordinates(screenshot_dir, white_threshold=250, white_pixel_count=50):
    """Identify conservative cropping coordinates based on white pixel thresholds."""
    left  = float('inf')
    right = 0

    image_files = sorted([f for f in os.listdir(screenshot_dir) if f.endswith('.png')])

    for filename in image_files:
        image_path = os.path.join(screenshot_dir, filename)
        image = Image.open(image_path).convert('RGB')
        image_array = np.array(image)

        height, width, _ = image_array.shape

        for y in range(height):
            row = image_array[y, :, :]

            # Count leading white pixels and trailing white pixels
            for x in range(width):
                if not np.all(row[x] >= white_threshold):
                    left = min(left, x)
                    break

            for x in range(width):
                if not np.all(row[width - 1 - x] >= white_threshold):
                    right = max(right, width - x)
                    break

        print(f"Processed image: {filename}")

    if (right - left) % 2 != 0:
        right -= 1

    return left, right
