#!/usr/bin/env python

import geopandas as gpd
import os
import requests
import zipfile
import urllib.request
from datetime import date
from data_util import get_data

def main():

    #print("tested")

    inpath = r'G:\projects\UtilityDistricts\eweb\DrinkingWater\EPA319_NPS_grant\ForestApplication\ODF_FACTS_DB\FERNS\FERNS_Model'
    subfolderlist = [x[0] for x in os.walk(inpath)]

    get_data(url = 'https://gisapps.odf.oregon.gov/data/FernsNoapsPolygons.Zip',
            dest_folder = inpath + '\\FernsNoapsPolygon_downloads')

    datapath = [i for i in subfolderlist if "Ferns_Noaps_Polygons" in i][-1]

    data = gpd.read_file(datapath, layer = 'Ferns_Noaps_Polygons')

    print(data.head(3))

if __name__ == "__main__":
    main()






