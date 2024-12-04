import warnings
warnings.filterwarnings('ignore')
import os
import tempfile
from pathlib import Path

import geopandas as gpd
import numpy as np
import rasterio
import rasterio.merge
import sentinelhub
from .creds import Config
from sentinelhub import (
    CRS,
    BBox,
    BBoxSplitter,
    MimeType,
    MosaickingOrder,
    SentinelHubDownloadClient,
    SentinelHubRequest,
    SHConfig,
)

from .params import get_params

class SentinelRequester:
    def __init__(self, start_date: str, end_date: str, path_geojson: str, path_save: str, 
                 sentinel: str, crs: str = "4326"):
        
        self.IMG_EVAL, self.DATA_COLLECTION = get_params(sentinel=sentinel)

        self.config = SHConfig()

        self.config.instance_id = Config.instance_id
        self.config.sh_client_id = Config.sh_client_id
        self.config.sh_client_secret = Config.sh_client_secret
        
        # What is the date format?
        self.start_date = start_date
        self.end_date = end_date

        self.path_geojson = path_geojson
        self.path_save = path_save
        
        self.crs = crs

    def get_subarea(self, bbox: BBox) -> SentinelHubRequest:
        return SentinelHubRequest(
            evalscript=self.IMG_EVAL,
            input_data=[
                SentinelHubRequest.input_data(
                    data_collection=self.DATA_COLLECTION,
                    time_interval=(self.start_date, self.end_date),
                    mosaicking_order=MosaickingOrder.MOST_RECENT,
                )
            ],
            responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
            bbox=bbox,
            size=sentinelhub.geo_utils.bbox_to_dimensions(bbox, resolution=(10, 10)),
            data_folder=tempfile.gettempdir(),
            config=self.config,
        )
    
    def read_file(self) -> gpd.GeoDataFrame:
         filepath = os.path.join(self.path_geojson)
         return (
              gpd.read_file(filepath).\
                to_crs('epsg:4326')['geometry'][0]
                )
    
    def create_file(self, filepath) -> None:
        if not os.path.exists(filepath):
            open(filepath, 'w').close()

    def prepare_polygon(self, polygon):  
        rect = BBox(polygon.bounds, CRS('4326'))
        dims = np.array(
            sentinelhub.geo_utils.bbox_to_dimensions(rect, resolution=(10, 10))
        )
        dims = np.ceil(dims / 2300).astype(int).tolist()
        bbox_splitter = BBoxSplitter(
            [polygon], CRS('4326'), split_shape=dims
        )
        bbox_list = bbox_splitter.get_bbox_list()

        return bbox_list
    
    def download_and_save(self, bbox_list) -> None:
        sh_requests = [self.get_subarea(bbox) for bbox in bbox_list]
        dl_requests = [request.download_list[0] for request in sh_requests]

        _ = SentinelHubDownloadClient(config=self.config).download(
            dl_requests, show_progress=True, max_threads=5
        )

        data_folder = sh_requests[0].data_folder
        tiffs = [Path(data_folder) / req.get_filename_list()[0] for req in sh_requests]

        opened_tiffs = []
        for tif in tiffs:
            opened_tiffs.append(rasterio.open(tif))
        
        rasterio.merge.merge(
                    opened_tiffs,
                    dtype=np.uint16,
                    dst_path=self.path_save,
                )

    def fetch(self) -> None:
        polygon = self.read_file()
        bbox_list = self.prepare_polygon(polygon)
        self.create_file(self.path_save)
        self.download_and_save(bbox_list)
