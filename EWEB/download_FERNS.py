#!/usr/bin/env python

import geopandas as gpd
from data_util import *
import timeit

def main():

    #print("tested")

    inpath = r'G:\projects\UtilityDistricts\eweb\DrinkingWater\EPA319_NPS_grant\ForestApplication\ODF_FACTS_DB\FERNS\FERNS_Model'
    subfolderlist = [x[0] for x in os.walk(inpath)]

    get_data(url = 'https://gisapps.odf.oregon.gov/data/FernsNoapsPolygons.Zip',
            dest_folder = inpath + '\\FernsNoapsPolygon_downloads')

    datapath = max([i for i in subfolderlist if "Ferns_Noaps_Polygons" in i], key=os.path.getmtime)

    data = gpd.read_file(datapath, layer = 'Ferns_Noaps_Polygons')

    print("Downloaded completed and here are the last three rows:\n")

    print(data.tail(3))

    print("\n")

if __name__ == "__main__":
    start = timeit.default_timer()
    main()
    # print("tested")
    stop = timeit.default_timer()
    total_time = stop - start
    print(f'Download FERNS takes {total_time}')






