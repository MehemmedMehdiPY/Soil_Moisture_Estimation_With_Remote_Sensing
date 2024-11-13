import os
import pandas as pd
from datetime import datetime, timedelta
from typing import Tuple, List

def get_weather(df: pd.DataFrame, start_date: str):
    """
    The function should return precipitation samples from IBM weather dataset.
    Columns you need are:
        * validTimeUtc - date time indicator
        * precip1Hour - Precipitation 
    
    $$$ Note that I am still unsure about how these precipitation columns work. We will figure that out later.

    start_date indicates the date time Sentinel - 1 data is available. 
    Your imaginary end_date is roughly 6 days ahead from start_data. 
        In other words, end_date = start_date + timedelta(days=6)
    Please, note that you should convert start_date to the data type of datetime.

    Starting from start_date, you should process the data to obtain precipitation value for each single day between revisit times. 
    Day 1, 2, 3, 4, 5, 6, 7
    Day 1 - start_date
    Day 7 - end_date

    When indexing, you might get considerably more than 7 samples since hours are also considered. 
    Use groupby method by pd.DataFrame to estimate sum of precipitation on each day.
    """
    pass
