import matplotlib.pyplot as plt
import sys
sys.path.append('../')
from models import Dubois
from utils import (
    free_outliers,
    get_sar,
    transform2rgb,
    convert2image,
    ANGLE,
)
if __name__ == "__main__":
    path_sar = "../data/Imishli/tiff/39.978022_48.076133.tiff"
    data_sar, _ = get_sar(path_sar=path_sar)
    vv, vh = data_sar[0], data_sar[1]
    
    # Soil Moisture
    sm = Dubois(vv=vv, vh=vh, angle=ANGLE)
    sm = free_outliers(sm[None], whis=1.5)[0]
    sm[sm < 0.2] = 0.2

    print(sm.shape)

    sm_mapped = transform2rgb(sm)
    image = convert2image(sm_mapped)
    
    plt.imshow(image)
    plt.show()
