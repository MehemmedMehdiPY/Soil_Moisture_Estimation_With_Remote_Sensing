import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# from shapely import Point, Polygon
# import rasterio

from models import dubois
from utils import (
    ANGLE,
    get_sar,
    get_weather
    )
from preprocessing import free_outliers

ROOT = './data'
ROOT_SENTINEL = os.path.join(ROOT, 'sentinel_data')
PATH_WEATHER = os.path.join(ROOT, 'weather')
PATH_TIFF = os.path.join(ROOT_SENTINEL, 'downloaded_tiff')

PATH_IBM_WEATHER = os.path.join(PATH_WEATHER, 'ibm_weather_data_imishli.csv')

class Processor():
    def __init__(self, path_weather: str):
        self.path_weather = path_weather
        self.df = self.read_weather()

    def get_sm(self, path_sar: str) -> np.ndarray:
        """Obtain Soil Moisture Map from Dubois model"""

        (vv, vh), src = get_sar(path_sar=path_sar)
        sm = dubois(vv=vv, vh=vh, angle=ANGLE)
        sm = free_outliers(sm[None], whis=1.5)[0]
        sm[sm < 0.2] = 0.2

        return sm, src

    def read_weather(self):
        """Read IBM Weather data"""
        df = pd.read_csv(self.path_weather)
        return df

    def get_weather(self, start_date: str):
        """Return IBM Weather samples"""
        start_date = start_date.replace('_', '-')
        samples = get_weather(self.df, start_date=start_date)
        return samples
    
if __name__ == '__main__':
    foldernames = os.listdir(PATH_TIFF)

    foldername = foldernames[0]
    folderpath = os.path.join(PATH_TIFF, foldername)
    start_date, end_date = foldername.split('__')

    start_date = start_date.replace('_', '.')
    end_date = end_date.replace('_', '.')
    
    start_date_path = os.path.join(folderpath, start_date + '.tiff')
    end_date_path = os.path.join(folderpath, end_date + '.tiff')

    # Create a processor
    processor = Processor(path_weather=PATH_IBM_WEATHER)

    sar_start, _ = processor.get_sm(start_date_path)
    sar_end, _ = processor.get_sm(end_date_path)

    print(sar_start.shape)
    print(sar_end.shape)

    plt.imshow(sar_start)
    plt.show()
    
    plt.imshow(sar_end)
    plt.show()
