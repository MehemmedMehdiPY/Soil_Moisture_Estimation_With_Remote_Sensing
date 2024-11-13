import json
import os
import pandas as pd

root = './data/sentinel_data'

date_path = os.path.join(root, 'dates', 'dates.json')
tiff_path = os.path.join(root, 'downloaded_tiff')

dates = json.load(open(date_path))
dates = pd.DataFrame(dates, columns=['date_1', 'date_2', 'date_3'])

# Initializing File Hierarchy 
for i in range(dates.shape[0]):
    date_1, date_3 = dates.iloc[i, [0, 2]]
    filename = date_1 + '__' + date_3
    filename = filename.replace('-', '_')
    filepath = os.path.join(tiff_path, filename)
    if not os.path.exists(filepath):
        os.makedirs(filepath) 
