import os
import sys
sys.path.append('../')
from download import SentinelRequester

if __name__ == "__main__":
    ROOT = "../data"
    city_names = os.listdir(ROOT)
    start_date = "2023-07-15"
    end_date = "2023-07-21"
    
    for city_name in city_names:
        path_geojson_folder = os.path.join(ROOT, city_name, "geojson")
    
        filename_geojson = os.listdir(path_geojson_folder)[0]
        filename_tiff = filename_geojson[:-8] + ".tiff"
    
        path_tiff = os.path.join(ROOT, city_name, "tiff", filename_tiff)
        path_geojson = os.path.join(path_geojson_folder, filename_geojson)
        
        requester = SentinelRequester(start_date=start_date, end_date=end_date, 
                                    path_geojson=path_geojson, path_save=path_tiff, 
                                    sentinel="sentinel_1")
        requester.fetch()
    
