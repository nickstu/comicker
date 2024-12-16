import os
from PIL import Image
import numpy as np
import re
import zipfile

# Directory containing the screenshots
screenshot_dir = './'  # Set this to the correct path if needed

# Directory to save the cropped and split images
output_dir = './cropped_images'
os.makedirs(output_dir, exist_ok=True)

# Path for the final zip file
zip_filename = 'cropped_images.zip'

# Threshold for white pixels (255 for pure white)
WHITE_THRESHOLD = 250

# Number of consecutive white pixels to consider
WHITE_PIXEL_COUNT = 50

# Variables to store the most conservative crop coordinates
top = 0             # Start cropping as far down as needed
left = float('inf') # Furthest left starting point
bottom = float('inf') # End cropping as high as possible
right = 0           # Furthest right ending point

# Function to extract numeric part from filename for sorting
def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else float('inf')

# First pass: analyze all images to determine conservative coordinates
image_files = sorted([f for f in os.listdir(screenshot_dir) if f.endswith('.png')],
                     key=extract_number)

for filename in image_files:
    image_path = os.path.join(screenshot_dir, filename)
    image = Image.open(image_path).convert('RGB')
    image_array = np.array(image)

    line_A = None
    A_left = 0
    A_right = 0
    line_B = None

    height, width, _ = image_array.shape

    # Scan each line to find line A
    for y in range(height):
        row = image_array[y, :, :]
        # Check for the first 50 white pixels at the start
        if np.all(row[:WHITE_PIXEL_COUNT] >= WHITE_THRESHOLD):
            line_A = y

            # Count leading white pixels (A_left)
            A_left = 0
            for pixel in row:
                if np.all(pixel >= WHITE_THRESHOLD):
                    A_left += 1
                else:
                    break

            # Count trailing white pixels (A_right)
            A_right = 0
            for pixel in reversed(row):
                if np.all(pixel >= WHITE_THRESHOLD):
                    A_right += 1
                else:
                    break

            # Look for line B where the first 50 pixels are no longer white
            for y2 in range(y + 1, height):
                next_row = image_array[y2, :, :]
                if not np.all(next_row[:WHITE_PIXEL_COUNT] >= WHITE_THRESHOLD):
                    line_B = y2
                    break

            break  # Stop after finding line A and line B

    # Update conservative coordinates
    if line_A is not None and line_B is not None:
        top = max(top, line_A)
        left = min(left, A_left)
        bottom = min(bottom, line_B - 1)
        right = max(right, width - A_right)

# Print the conservative cropping coordinates
print(f"Conservative cropping coordinates:")
print(f"  Top: {top}")
print(f"  Bottom: {bottom}")
print(f"  Left: {left}")
print(f"  Right: {right}")

# Ensure the crop width is even
if (right - left) % 2 != 0:
    right -= 1

# Calculate the conservative crop width
crop_width = right - left

# Second pass: crop all images using the conservative coordinates and split them
for idx, filename in enumerate(image_files):
    image_path = os.path.join(screenshot_dir, filename)
    image = Image.open(image_path).convert('RGB')
    image_width, image_height = image.size

    if idx == 0:
        # For the first image, center the crop horizontally within the conservative range
        first_left = left + crop_width // 4
        first_right = first_left + crop_width // 2
        cropped_image = image.crop((first_left, top, first_right, bottom))

        output_path = os.path.join(output_dir, '000.png')
        cropped_image.save(output_path)
        print(f"Saved unsplit image: {output_path}")
    else:
        # Crop the image using the conservative coordinates
        cropped_image = image.crop((left, top, right, bottom))

        # Split the image in the middle
        cropped_width, cropped_height = cropped_image.size
        middle = cropped_width // 2

        # Right part
        image_index = (idx - 1) * 2 + 1
        right_part = cropped_image.crop((middle, 0, cropped_width, cropped_height))
        right_output_path = os.path.join(output_dir, f'{image_index:03d}.png')
        right_part.save(right_output_path)

        # Left part
        image_index = (idx - 1) * 2 + 2
        left_part = cropped_image.crop((0, 0, middle, cropped_height))
        left_output_path = os.path.join(output_dir, f'{image_index:03d}.png')
        left_part.save(left_output_path)

        print(f"Saved split images: {right_output_path}, {left_output_path}")

# Compress all files in the output directory into a zip file
with zipfile.ZipFile(zip_filename, 'w') as zipf:
    for root, _, files in os.walk(output_dir):
        for file in files:
            file_path = os.path.join(root, file)
            zipf.write(file_path, os.path.relpath(file_path, output_dir))

print(f"All files compressed into {zip_filename}")
print("Cropping, splitting, and compression process completed!")
