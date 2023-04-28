#!/usr/bin/env python

import geopandas as gpd
import pandas as pd
from data_util import *
import timeit
import sys

path = r'G:\projects\UtilityDistricts\eweb\DrinkingWater\EPA319_NPS_grant\ForestApplication\ODF_FACTS_DB\FERNS'
def main():

    #print("tested")

    inpath = path + '\\FERNS_Model'
    subfolderlist = [x[0] for x in os.walk(inpath)]

    get_data(url = 'https://gisapps.odf.oregon.gov/data/FernsNoapsPolygons.Zip',
            dest_folder = inpath + '\\FernsNoapsPolygon_downloads')

    datapath = max([i for i in subfolderlist if "Ferns_Noaps_Polygons" in i], key=os.path.getmtime)

    data = gpd.read_file(datapath, layer = 'Ferns_Noaps_Polygons')

    print("Downloaded completed and here are the last three rows:\n")

    print(data.tail(3))

    print("\n")

    data = gpd.read_file(inpath + "\\FERNS_Final_Products.gdb", layer="FERNSSummary_McKenzie_Joined")
    print(f"Last update includes {data.shape[0]} records and below shows the summarized acres by activity type:\n")
    print(data.groupby('ActType').agg(SumAcres = pd.NamedAgg(column = 'SUM_calc_acres', aggfunc = sum)))
    print("\n")

if __name__ == "__main__":
    sys.stdout = open(path+'\\FERNS_log.txt', "w")
    start = timeit.default_timer()
    main()
    # print("tested")
    stop = timeit.default_timer()
    total_time = stop - start
    print(f'Download FERNS takes {total_time}')
    sys.stdout.close()






