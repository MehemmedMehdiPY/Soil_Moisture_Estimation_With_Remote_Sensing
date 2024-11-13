from download import SentinelRequester
import json
import os
import pandas as pd

root = './data/sentinel_data'
geojson_path = os.path.join(root, 'geojson_files', '39.978022_48.076133.geojson')

date_path = os.path.join(root, 'dates', 'dates.json')
tiff_path = os.path.join(root, 'downloaded_tiff')

dates = json.load(open(date_path))
dates = pd.DataFrame(dates, columns=['date_1', 'date_2', 'date_3'])

foldernames = os.listdir(tiff_path)
foldernames.sort()

print(foldernames)

for foldername in foldernames[20:30]:
    print('New Folder Name:', foldername)
    date_1, date_3 = foldername.split('__')
    date_1 = date_1.replace('_', '.')
    date_3 = date_3.replace('_', '.')
    
    save_path_1 = os.path.join(tiff_path, foldername, date_1 + '.tiff')
    save_path_3 = os.path.join(tiff_path, foldername, date_3 + '.tiff')
    
    requester_1 = SentinelRequester(start_date=date_1, end_date=date_1, sentinel='sentinel_1',
                                      geojson_path=geojson_path, save_path=save_path_1)
    
    requester_3 = SentinelRequester(start_date=date_3, end_date=date_3, sentinel='sentinel_1',
                                      geojson_path=geojson_path, save_path=save_path_3)
    
    requester_1.fetch()
    requester_3.fetch()
