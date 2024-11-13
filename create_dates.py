import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
import json

# Reference date
date_ref = date(year=2023, month=1, day=4)
increase_rate = 6

df = pd.read_csv('./data/weather/ibm_weather_data_imishli.csv')
print(df.columns)
print(df.shape)


df['validTimeUtc'] = pd.to_datetime(df['validTimeUtc'])

precip = df['precip24Hour']
precip = precip.groupby([df['validTimeUtc'].dt.date]).sum()



indexes = np.where(precip > 20)[0]
precip = precip[indexes]

print(indexes.shape)
print(precip.shape)

dates = []
for i in range(precip.size):
    j = 0
    while True:
        date_available = date_ref + timedelta(days = increase_rate * j)
        diff = precip.index[i] - date_available
        
        if -increase_rate <= diff.days <= increase_rate and precip.index[i] < date_available:
            
            date_available_prev = date_available - timedelta(days=increase_rate)
            if date_available_prev != precip.index[i]:
                dates.append([date_available_prev, precip.index[i], date_available])
                
            break

        j += 1

dates_str = []

for date_1, date_2, date_3 in dates:
    date_1 = date_1.strftime("%Y-%m-%d")
    date_2 = date_2.strftime("%Y-%m-%d")
    date_3 = date_3.strftime("%Y-%m-%d")
    
    dates_str.append([date_1, date_2, date_3])

print(len(dates_str))

with open('./data/sentinel_data/dates/dates.json', 'w') as f:
    json.dump(dates_str, f)