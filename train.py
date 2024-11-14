import warnings
warnings.filterwarnings('ignore')

import os
import pandas as pd
import numpy as np

import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from torch.optim import Adam

# from shapely import Point, Polygon
# import rasterio

from models import dubois, ANNModel
from train import Trainer
from utils import (
    ANGLE,
    get_sar,
    get_weather,
    )
from preprocessing import free_outliers

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
        df['validTimeUtc'] = pd.to_datetime(df['validTimeUtc'])
        df['validDate'] = df['validTimeUtc']
        df['validDate'] = df['validDate'].dt.date
        return df

    def get_weather(self, start_date: str):
        """Return IBM Weather samples"""
        start_date = start_date.replace('_', '-')
        samples = get_weather(self.df, start_date=start_date)
        return samples

class PrecipDataset(Dataset):
    def __init__(self):
        super().__init__()

        foldernames = os.listdir(PATH_TIFF)
        processor = Processor(path_weather=PATH_IBM_WEATHER)

        precips = np.zeros((len(foldernames), 7))
        sm = np.zeros((len(foldernames), 2))
        
        for i in range(len(foldernames)):
            foldername = foldernames[i]
            folderpath = os.path.join(PATH_TIFF, foldername)
            start_date, end_date = foldername.split('__')

            start_date = start_date.replace('_', '.')
            end_date = end_date.replace('_', '.')
            
            start_date_path = os.path.join(folderpath, start_date + '.tiff')
            end_date_path = os.path.join(folderpath, end_date + '.tiff')
            
            sample = processor.get_weather(start_date=start_date)
            sar_start, _ = processor.get_sm(start_date_path)
            sar_end, _ = processor.get_sm(end_date_path)
            
            precips[i] = sample.values
            sm[i] = [sar_start.sum(), sar_end.sum()]
        
        self.precips = torch.tensor(precips).to(torch.float32)
        self.sm = torch.tensor(sm).to(torch.float32)

        self.precip_max = self.precips.max(dim=0)[0]
        self.precip_min = self.precips.min(dim=0)[0]

        self.sm_max = self.sm.max(dim=0)[0]
        self.sm_min = self.sm.min(dim=0)[0]

    def scale(self, precip, sm):
        precip = (precip - self.precip_min) / (self.precip_max - self.precip_min)
        sm = (sm - self.sm_min) / (self.sm_max - self.sm_min)
        return precip, sm

    def __getitem__(self, idx):
        precip = self.precips[[idx]]
        sm = self.sm[[idx]]

        precip, sm = self.scale(precip, sm)
                
        X = torch.concatenate((precip, sm[:, [0]]), dim=1)
        y = sm[:, [1]]

        return X[0], y[0]

    def __len__(self):
        return len(self.precips);

ROOT = './data'
ROOT_SENTINEL = os.path.join(ROOT, 'sentinel_data')
PATH_WEATHER = os.path.join(ROOT, 'weather')
PATH_TIFF = os.path.join(ROOT_SENTINEL, 'downloaded_tiff')

PATH_IBM_WEATHER = os.path.join(PATH_WEATHER, 'ibm_weather_data_imishli.csv')

DEVICE = 'cpu'
if __name__ == '__main__':
    
    dataset = PrecipDataset()
    
    train_loader = DataLoader(dataset, batch_size=2, shuffle=True)
    val_loader = DataLoader(dataset, batch_size=len(dataset), shuffle=False)
    
    model = ANNModel().to(DEVICE)

    for X, y in val_loader:
        pass

    optimizer = Adam(model.parameters(), lr=1e-4)
    loss_fn = nn.MSELoss(reduction='sum')

    trainer = Trainer(model=model, train_loader=train_loader, val_loader=val_loader, optimizer=optimizer,
            loss_fn=loss_fn, epochs=10, filepath='./saved_models/model.pt', device=DEVICE)
    
    trainer.run()
    trainer.save_model()