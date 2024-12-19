import os
from PIL import Image
import zipfile

def apply_crop_lr(screenshot_dir, output_dir, crop_coords, zip_filename='cropped_images.zip'):
    """Crop images left and right based on provided coordinates, keeping full height. Special handling for the first image."""
    os.makedirs(output_dir, exist_ok=True)

    left, right = crop_coords
    crop_width = right - left

    image_files = sorted([f for f in os.listdir(screenshot_dir) if f.endswith('.png')])

    for idx, filename in enumerate(image_files):
        image_path = os.path.join(screenshot_dir, filename)
        image = Image.open(image_path).convert('RGB')
        image_width, image_height = image.size

        if idx == 0:
            # For the first image, crop centered horizontally within the conservative range
            first_left = left + crop_width // 4
            first_right = first_left + crop_width // 2
            cropped_image = image.crop((first_left, 0, first_right, image_height))
            output_path = os.path.join(output_dir, '000.png')
            cropped_image.save(output_path)
            print(f"Saved unsplit image: {output_path}")
        else:
            # Crop the image using the conservative left and right coordinates
            cropped_image = image.crop((left, 0, right, image_height))

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
