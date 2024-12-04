import numpy as np

def create_random_mask(size: int, f: float) -> np.ndarray:
    """Mask to multiply with a channel"""
    size_1 = int(size * f)
    size_0 = size - size_1

    mask_1 = np.ones(size_1)
    mask_0 = np.zeros(size_0)

    mask = np.concatenate((mask_0, mask_1))
    np.random.shuffle(mask)
    
    return mask

def apply_red2yellow_filter(image, f=0.7) -> np.ndarray:
    """
    Apply a red filter to a random selection of pixels in the image.
    
    Parameters:
     - image: A 3D NumPy array representing the RGB image.
     - f: fraction

      Returns:
     - modified_image: A 3D NumPy array with red pixels converted to yellow."""
    
    if not isinstance(image, np.ndarray):
        raise TypeError("The image must be a NumPy array.")
    
    image = image.copy()

    cond_1 = (image[:, :, 0] == 255)
    cond_2 = (image[:, :, 1] == 0)
    cond_3 = (image[:, :, 2] == 0)
    cond = (cond_1 & cond_2 & cond_3)

    index_0, index_1 = np.where(cond)

    mask = create_random_mask(index_0.size, f=f)
    image[index_0, index_1] = np.array([255, 255, 0])
    image[index_0, index_1, 1] = image[index_0, index_1, 1] * mask

    return image;
    