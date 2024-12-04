import numpy as np
import random

def apply_red_filter(image, perc_range = (0.75, 0.9)):
    """
    Apply a red filter to a random selection of pixels in the image.
    
    Parameters:
     - image: A 3D NumPy array representing the RGB image.
     - perc_range: A tuple representing the range of pixels to convert to red.
      
      Returns:
     - modified_image: A 3D NumPy array with red pixels converted to yellow."""
    
    if not isinstance(image, np.ndarray):
        raise TypeError("The image must be a NumPy array.")
    
    # Get the mask for red pixels (where red channel > green and blue channels)
    red_mask = (image[:, :, 0] > 100) & (image[:, :, 1] < 100) (image[:, :, 2] < 100)
    
    # Extract the indices of red pixels
    red_pixel_indices = np.argwhere(red_mask)
    
    # Get the number of red pixels to modify based on the percentage range
    total_red_pixels = red_pixel_indices.shape[0]
    min_red_pixels = int(total_red_pixels * perc_range[0])
    max_red_pixels = int(total_red_pixels * perc_range[1])
    
    # Choose a random number of red pixels to change to yellow
    num_red_pixels_to_modify = random.randint(min_red_pixels, max_red_pixels)
    
    # Randomly select red pixels to convert to yellow
    pixels_to_modify = random.sample(range(total_red_pixels), num_red_pixels_to_modify)
    
    # Create a copy of the image to modify
    modified_image = image.copy()
    
    # Convert selected red pixels to yellow (255, 255, 0)
    for idx in pixels_to_modify:
        i, j = red_pixel_indices[idx]
        modified_image[i, j] = [255, 255, 0]
    
    return modified_image