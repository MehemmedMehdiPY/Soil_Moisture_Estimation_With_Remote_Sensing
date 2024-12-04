import sys
sys.path.append('../')
from download import SentinelRequester

if __name__ == "__main__":
    start_date = "2023-07-15"
    end_date = "2023-07-21"
    path_geojson = "../data/Imishli/geojson/39.978022_48.076133.geojson"
    path_save = "../data/Imishli/tiff/39.978022_48.076133.tiff"
    
    requester = SentinelRequester(start_date, end_date, path_geojson, path_save, sentinel="sentinel_1")
    requester.fetch()
    
