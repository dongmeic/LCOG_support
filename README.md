# LCOG_support
To document the requests on data, model, or map support for our partner agencies

# EUG
## Middle Housing Project

The task is to create a shapefile layer of taxlots that are within a walking distance of 1/4 mile to EmX bus stops.

The steps are 1) [creating EmX bus stops](https://github.com/dongmeic/LCOG_support/blob/main/EUG/Create_EmX_stops.ipynb); 2) [creating service areas from EmX bus stops](https://github.com/dongmeic/LCOG_support/blob/main/EUG/ServiceAreaAnalysis.py); 3) spatial overlay (e.g., intersect) between taxlots and service areas. The last step is done in ArcGIS Pro.

# SPR
## Heatmaps

Maps are shown in the `maps` folder. 

# EWEB
## [FERNS dashboard](https://lcog.maps.arcgis.com/apps/dashboards/f003689bcb7f45eca5be6f02baada6c0)

The work is to report forest activity acreage on McKenzie Basins. The project transfer note document is saved as G:\projects\UtilityDistricts\eweb\DrinkingWater\EPA319_NPS_grant\ForestApplication\ODF_FACTS_DB\FERNS\FERNS workflow.txt. The process is scripted and corrected on the append step.

FERNS (Forest Activity Electronic Reporting and Notification System) sourced from Oregon Department of Forestry (ODF) presents the spatial and temporal patterns of the forest activity acreage by activity type. Data is [downloaded](https://github.com/dongmeic/LCOG_support/blob/main/EWEB/download_FERNS.py) from the [ODF maps and data page](https://www.oregon.gov/ODF/AboutODF/Pages/MapsData.aspx). The processed data is stored [here](https://services5.arcgis.com/9s1YtFmLS0YTl10F/arcgis/rest/services/FERNS_for_McKenzie_Catchments/FeatureServer). The task is to update the [dashboard](https://lcog.maps.arcgis.com/home/item.html?id=f003689bcb7f45eca5be6f02baada6c0) using the model created by Joel Donnelly, which is exported to [python scripts](https://github.com/dongmeic/LCOG_support/tree/main/EWEB) and run in the ArcPy environment using ArcGIS Pro Notebooks (see the notebooks and "FERNS_Model.aprx" in the path set [here](https://github.com/dongmeic/LCOG_support/blob/main/EWEB/FERNS_for_AGO_step1.py)) Edit the [dashboard](https://lcog.maps.arcgis.com/home/item.html?id=f003689bcb7f45eca5be6f02baada6c0) on the "Data last updated" after running the notebooks by step. Copy the batch file `T:\DCProjects\GitHub\LCOG_support\EWEB\run_to_update_ferns.bat` in the user folder (e.g., `C:\Users\clid****`, '****' is the four digit LCOG ID), and run the batch file in Command Prompt will run through the steps from data download to dashboard update. Update the dashboard monthly.

## [Illegal camp notice](https://lcog.maps.arcgis.com/home/webmap/viewer.html?webmap=e200b60e56bc4abdbc3b6ba09eca89bf)

The work is to report illegal camp site for watershed protection. The project transfer note document is saved as G:\projects\UtilityDistricts\eweb\DrinkingWater\IllegalCampCoordination\READ ME - Illegal Camping Report Procedure.docx. The process is scripted and corrected on the filling in missing ownership step. The task is scheduled to run daily.

[Step 1](https://github.com/dongmeic/LCOG_support/blob/main/EWEB/illegal_camp_notice_1.py): check the most recent data entry and the output folder to decide whether there is a new notice and process spatial join to get the taxlot and nearby owner when owner information is missing in case there is a new notice;

[Step 2](https://github.com/dongmeic/LCOG_support/blob/main/EWEB/illegal_camp_notice_2.py): reorganize the spatial join table, add the required fields such as "above_intake" and "photos", and format the table;

[Step 3](https://github.com/dongmeic/LCOG_support/blob/main/EWEB/illegal_camp_notice_3.py): export the map with the reported campsite(s) on the same day;

[Step 4](https://github.com/dongmeic/LCOG_support/blob/main/EWEB/illegal_camp_notice_4.py): add the image to the table and send out an email notification for review;

[Step 5](https://github.com/dongmeic/LCOG_support/blob/main/EWEB/illegal_camp_notice_5.py): after the review, decide whether there is a need to edit the map manually and remove the added image; run this script to add the updated map and send out the notice to the group.
