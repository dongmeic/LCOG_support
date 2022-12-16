# LCOG_support
To document the requests on data, model, or map support for our partner agencies

# EUG
## Middle Housing Project

The task is to create a shapefile layer of taxlots that are within a walking distance of 1/4 mile to EmX bus stops.

The steps are 1) [creating EmX bus stops](https://github.com/dongmeic/LCOG_support/blob/main/EUG/Create_EmX_stops.ipynb); 2) [creating service areas from EmX bus stops](https://github.com/dongmeic/LCOG_support/blob/main/EUG/ServiceAreaAnalysis.py); 3) spatial overlay (e.g., intersect) between taxlots and service areas. The last step is done in ArcGIS Pro.

# EWEB
## [FERNS dashboard](https://lcog.maps.arcgis.com/apps/dashboards/f003689bcb7f45eca5be6f02baada6c0)

FERNS (Forest Activity Electronic Reporting and Notification System) sourced from Oregon Department of Forestry (ODF) presents the spatial and temporal patterns of the forest activity acreage by activity type. Data is [downloaded](https://github.com/dongmeic/LCOG_support/blob/main/EWEB/1_download_FERNS.ipynb) from the [ODF maps and data page](ttps://www.oregon.gov/ODF/AboutODF/Pages/MapsData.aspx). The processed data is stored [here](https://services5.arcgis.com/9s1YtFmLS0YTl10F/arcgis/rest/services/FERNS_for_McKenzie_Catchments/FeatureServer). The task is to update the [dashboard](https://lcog.maps.arcgis.com/home/item.html?id=f003689bcb7f45eca5be6f02baada6c0) using the model created by Joel Donnelly, which is exported to [python scripts](https://github.com/dongmeic/LCOG_support/tree/main/EWEB) and run in the ArcPy environment using ArcGIS Pro Notebooks (see the notebooks and "FERNS_Model.aprx" in the path set [here](https://github.com/dongmeic/LCOG_support/blob/main/EWEB/FERNS_for_AGO_step1.py)) Edit the [dashboard](https://lcog.maps.arcgis.com/home/item.html?id=f003689bcb7f45eca5be6f02baada6c0) on the "Data last updated" after the run the notebooks by step.
