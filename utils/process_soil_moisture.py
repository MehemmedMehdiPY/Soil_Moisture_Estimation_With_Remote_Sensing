import sys
sys.path.append('../')

import numpy as np
from preprocessing import free_outliers, min_max_scale, calibrate
import rasterio


ANGLE = 65 * np.pi / 180
K = 1

def get_sar(path_sar: str) -> np.ndarray:
    """Returns Synthetic Aparture Radar (SAR) view of the field with preprocessing"""
    
    with rasterio.open(path_sar) as src:
        field_sar = src.read()

    field_sar = free_outliers(field_sar, whis=1.5)
    field_sar = min_max_scale(field_sar, bit_size=16)
    field_sar_calibrated = calibrate(field_sar, angle=ANGLE, K=K)
    
    return field_sar_calibrated, src
