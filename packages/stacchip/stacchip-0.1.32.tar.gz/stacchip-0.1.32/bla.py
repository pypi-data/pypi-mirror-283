import pystac_client
from stacchip.indexer import Sentinel2Indexer
from stacchip.chipper import Chipper
import os

catalog = pystac_client.Client.open("https://earth-search.aws.element84.com/v1")

os.environ["CPL_TMPDIR"] = "/tmp"
os.environ["GDAL_CACHEMAX"] = "75%"
os.environ["GDAL_INGESTED_BYTES_AT_OPEN"] = "32768"
os.environ["GDAL_DISABLE_READDIR_ON_OPEN"] = "EMPTY_DIR"
os.environ["GDAL_HTTP_MERGE_CONSECUTIVE_RANGES"] = "YES"
os.environ["GDAL_HTTP_MULTIPLEX"] = "YES"
os.environ["GDAL_HTTP_VERSION"] = "2"
os.environ["PYTHONWARNINGS"] = "ignore"
os.environ["VSI_CACHE"] = "TRUE"


items = catalog.search(collections=["sentinel-2-l2a"], max_items=1)
item = items.item_collection()[0]
dat = list(item.assets.keys())
for k in dat:
    if k not in ["red", "green", "blue", "nir"]:
        del item.assets[k]
indexer = Sentinel2Indexer(item)
# index = .create_index()
chip = Chipper(item_id=item.id, indexer=indexer, platform="", bucket="example").chip(
    x=10, y=10
)

from pyarrow import dataset as da

from geoarrow.pyarrow import io

import geoarrow.pyarrow as ga

table = io.read_geoparquet_table(
    "/home/tam/Desktop/clay-v1-data-combined-index.parquet"
)
geoms = table.column("geometry")
pdgeoms = ga.to_geopandas(geoms)

centroids = pdgeoms.centroid


data = da.dataset(
    "/home/tam/Desktop/clay-v1-data-combined-index.parquet", format="parquet"
)
table = data.to_table(
    columns=["chipid", "platform", "item", "date", "chip_index_x", "chip_index_y"]
)
