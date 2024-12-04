import numpy as np
import rasterio

ANGLE = 65 * np.pi / 180
K = 1

def free_outliers(image, whis: float = 1.5):
    q1, q3 = np.quantile(image, q=[0.25, 0.75], axis=[-2, -1])
    iqr = q3 - q1
    lower = q1 - whis * iqr
    upper = q3 + whis * iqr

    lower = lower[:, np.newaxis, np.newaxis]
    upper = upper[:, np.newaxis, np.newaxis]

    image = np.clip(image, a_min=lower, a_max=upper)
    return image

def min_max_scale(data, bit_size: int = 16):
    return (data - 0) / (2 ** bit_size - 0)

def calibrate(DN, angle: int, K: int = 1):
    """Radiometric Calibration"""
    return np.sqrt(DN ** 2 * K / np.sin(angle))

def get_sar(path_sar: str) -> np.ndarray:
    """Returns Synthetic Aparture Radar (SAR) view of the field with preprocessing"""
    
    with rasterio.open(path_sar) as src:
        field_sar = src.read()

    field_sar = free_outliers(field_sar, whis=1.5)
    field_sar = min_max_scale(field_sar, bit_size=16)
    field_sar_calibrated = calibrate(field_sar, angle=ANGLE, K=K)
    
    return field_sar_calibrated, src
