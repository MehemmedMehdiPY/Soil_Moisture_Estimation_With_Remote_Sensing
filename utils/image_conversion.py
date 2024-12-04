import numpy as np
import PIL
from PIL import Image

def convert2image(image_array: np.ndarray) -> PIL.Image.Image:
    image_array = image_array.astype(np.uint8)
    image = Image.fromarray(image_array)
    return image

if __name__ == '__main__':
    image = np.zeros((256, 256, 3))
    image = convert2image(image)
    print(type(image))