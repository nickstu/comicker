import screenshot
import identify_crop
import apply_crop_lr


# Take screenshots
#screenshot.take_screenshots(num_repeats=100)

# Identify crop coordinates
crop_coords = identify_crop.identify_crop_coordinates('screenshot')
print(crop_coords)

# Apply crop and split images
apply_crop_lr.apply_crop_lr('screenshot', 'cropped_images', crop_coords)