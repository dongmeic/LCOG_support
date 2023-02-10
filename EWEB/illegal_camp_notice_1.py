import arcpy, os
from datetime import datetime, date
from homeless import *
import time
from arcgis import GIS
from arcgis.features import FeatureLayerCollection
import pandas as pd
gis = GIS('home')

arcpy.env.overwriteOutput = True

outpath = r'G:\projects\UtilityDistricts\eweb\DrinkingWater\IllegalCampCoordination\Recieved'
path = outpath + '\\IllegalCampNotification_pro'
url = 'https://services5.arcgis.com/9s1YtFmLS0YTl10F/ArcGIS/rest/services/ZHomeless_Camp_Trash_Collector/FeatureServer'
camp_site = url + '/0'

# get the most recent date
listdates1 = []
cursor = arcpy.da.SearchCursor(camp_site, "Date")
for row in cursor:
    listdates1.append(row)

listdates = [dt[0] for dt in listdates1 if dt[0] is not None]    
maxdate = max(listdates)

# check whether there is a need to report
maxdatestr = str(maxdate)
datestr = maxdatestr.split('.')[0].split(' ')[0]
res = convert_date(datestr)
Y = res[1]
m = res[2]
d = res[3]
outfolder = os.path.join(outpath, Y, m+'_'+d)
outfolder_yr = os.path.join(outpath, Y)
filename = 'IllegalCampNotice_'+m+'_'+d+'_'+Y[2:4]+'.xlsx'
file = os.path.join(outfolder, filename)

if os.path.exists(outfolder) & os.path.exists(file):
    print('No need to report!')
    # get current date and time
    current_datetime = datetime.now()
    print("Current date & time : ", current_datetime)

    # convert datetime obj to string
    str_current_datetime = str(current_datetime)

    # create a file object along with extension
    file_name = str_current_datetime.split(' ')[0].replace('-', '') +".txt"
    file = open(file_name, 'w')

    print("File created : ", file.name)
    file.close()
    
else:
    print('Making the report...')
    if not os.path.exists(outfolder_yr):
        os.makedirs(outfolder_yr)
        print('Created the new Year folder...')
    elif not os.path.exists(outfolder):
        os.makedirs(outfolder)
        print('Created the new folder...')
    else:
        print('Folder already exists but missing the file...')
    

    flyrs = FeatureLayerCollection(url)
    fl = flyrs.layers[0]
    sdf = pd.DataFrame.spatial.from_layer(fl)
    sdf['datestr'] = sdf.Date.apply(lambda x: str(x).split(' ')[0])
    sdf_s = sdf[sdf.datestr == maxdatestr.split(' ')[0]]
    df = convert_dtypes_arcgis(sdf_s)
    df.drop(columns='datestr', inplace=True)
    datacopy = df.spatial.to_featureclass(path + '\\MyProject4.gdb\\most_recent')
    print(f'Most recent data saved at {datacopy}')
    
    sdeFile = path + "\\RLIDDB.sde"

    if os.path.exists(sdeFile):
        os.remove(sdeFile)

    # connect to RLIDGeo to get taxlot data
    conn = arcpy.CreateDatabaseConnection_management(out_folder_path=path,
                                              out_name="RLIDDB.sde",
                                              database_platform="SQL_SERVER",
                                              instance="rliddb.int.lcog.org,5433",
                                              account_authentication="OPERATING_SYSTEM_AUTH",
                                              database="RLIDGeo")

    arcpy.env.workspace = conn.getOutput(0)
    fc = "RLIDGeo.DBO.Taxlot"
    
    cs_fc = path + '\\MyProject4.gdb\\most_recent'
    spatialJoin = path + '\\MyProject4.gdb\\HomelessCampSite_SpatialJoin'
    
    arcpy.analysis.SpatialJoin(cs_fc, fc, spatialJoin, "JOIN_ONE_TO_ONE", "KEEP_ALL",'Status "Status" true true false 50 Text 0 0,First,#,Homeless Camp Site,Status,0,50;Comments "Comments" true true false 500 Text 0 0,First,#,Homeless Camp Site,Comments,0,500;Date "Date" true true false 8 Date 0 0,First,#,Homeless Camp Site,Date,-1,-1;Submitted_by "Submitted By" true true false 50 Text 0 0,First,#,Homeless Camp Site,Submitted_by,0,50;Dogs_present "Dogs present" true true false 50 Text 0 0,First,#,Homeless Camp Site,Dogs_present,0,50;Unruly_inhabitants "Unruly inhabitants" true true false 50 Text 0 0,First,#,Homeless Camp Site,Unruly_inhabitants,0,50;Hazardous_materials_present "Hazardous materials present" true true false 50 Text 0 0,First,#,Homeless Camp Site,Hazardous_materials_present,0,50;Biohazards_present "Biohazards present" true true false 50 Text 0 0,First,#,Homeless Camp Site,Biohazards_present,0,50;Size_of_encampment "Size of encampment" true true false 50 Text 0 0,First,#,Homeless Camp Site,Size_of_encampment,0,50;GlobalID "GlobalID" false false true 38 GlobalID 0 0,First,#,Homeless Camp Site,GlobalID,-1,-1;maptaxlot_hyphen "maptaxlot_hyphen" true true false 17 Text 0 0,First,#,Lane County Taxlots,maptaxlot_hyphen,0,17;ownname "ownname" true true false 128 Text 0 0,First,#,Lane County Taxlots,ownname,0,128;addr1 "addr1" true true false 64 Text 0 0,First,#,Lane County Taxlots,addr1,0,64;ownercity "ownercity" true true false 40 Text 0 0,First,#,Lane County Taxlots,ownercity,0,40;ownerprvst "ownerprvst" true true false 30 Text 0 0,First,#,Lane County Taxlots,ownerprvst,0,30;ownerzip "ownerzip" true true false 10 Text 0 0,First,#,Lane County Taxlots,ownerzip,0,10;geocity_name "geocity_name" true true false 32 Text 0 0,First,#,Lane County Taxlots,geocity_name,0,32;ugb_name "ugb_name" true true false 32 Text 0 0,First,#,Lane County Taxlots,ugb_name,0,32;longitude "longitude" true true false 8 Double 8 38,First,#,Lane County Taxlots,longitude,-1,-1;latitude "latitude" true true false 8 Double 8 38,First,#,Lane County Taxlots,latitude,-1,-1', "INTERSECT", None, '')
    
    print('Completed a spatial join with taxlot...')
    
    field_names = [f.name for f in arcpy.ListFields(spatialJoin)]
    newfields = ["Nearby_owner", "Nearby_owner_address"]
    missing_own = [row[0] is None for row in arcpy.da.SearchCursor(spatialJoin, "ownname")]
    res = arcpy.GetCount_management(spatialJoin)
    if any(missing_own):
        print(f"Owner name is missing in the {sum(missing_own)} of {res[0]} counts")
        taxlots_w_ownernm = arcpy.management.SelectLayerByAttribute(fc, "NEW_SELECTION", "ownname IS NOT NULL", None)
        for newfield in newfields:
            if newfield not in field_names:
                arcpy.management.AddField(spatialJoin, newfield, "TEXT", 255)

        with arcpy.da.UpdateCursor(spatialJoin, ["ownname", 'Nearby_owner', 'Nearby_owner_address', "TARGET_FID"]) as cursor:
            i = 0
            for row in cursor:
                row[3] = df.OBJECTID.values[i]
                i+=1
                if row[0] is None:
                    selres2 = arcpy.management.SelectLayerByAttribute(spatialJoin, "NEW_SELECTION", "ownname IS NULL", None)
                    spatialJoin2 = path + '\\MyProject4.gdb\\CampSite_SpatialJoin'
                    arcpy.analysis.SpatialJoin(selres2, taxlots_w_ownernm, spatialJoin2, "JOIN_ONE_TO_ONE", "KEEP_ALL", 'Join_Count "Join_Count" true true false 4 Long 0 0,First,#,Camp Site,Join_Count,-1,-1;TARGET_FID "TARGET_FID" true true false 4 Long 0 0,First,#,Camp Site,TARGET_FID,-1,-1;Status "Status" true true false 50 Text 0 0,First,#,Camp Site,Status,0,50;Comments "Comments" true true false 500 Text 0 0,First,#,Camp Site,Comments,0,500;Date "Date" true true false 8 Date 0 0,First,#,Camp Site,Date,-1,-1;Submitted_by "Submitted By" true true false 50 Text 0 0,First,#,Camp Site,Submitted_by,0,50;Dogs_present "Dogs present" true true false 50 Text 0 0,First,#,Camp Site,Dogs_present,0,50;Unruly_inhabitants "Unruly inhabitants" true true false 50 Text 0 0,First,#,Camp Site,Unruly_inhabitants,0,50;Hazardous_materials_present "Hazardous materials present" true true false 50 Text 0 0,First,#,Camp Site,Hazardous_materials_present,0,50;Biohazards_present "Biohazards present" true true false 50 Text 0 0,First,#,Camp Site,Biohazards_present,0,50;Size_of_encampment "Size of encampment" true true false 50 Text 0 0,First,#,Camp Site,Size_of_encampment,0,50;maptaxlot_hyphen "maptaxlot_hyphen" true true false 17 Text 0 0,First,#,Camp Site,maptaxlot_hyphen,0,17;ownname "ownname" true true false 128 Text 0 0,First,#,Camp Site,ownname,0,128;addr1 "addr1" true true false 64 Text 0 0,First,#,Camp Site,addr1,0,64;ownercity "ownercity" true true false 40 Text 0 0,First,#,Camp Site,ownercity,0,40;ownerprvst "ownerprvst" true true false 30 Text 0 0,First,#,Camp Site,ownerprvst,0,30;ownerzip "ownerzip" true true false 10 Text 0 0,First,#,Camp Site,ownerzip,0,10;geocity_name "geocity_name" true true false 32 Text 0 0,First,#,Camp Site,geocity_name,0,32;ugb_name "ugb_name" true true false 32 Text 0 0,First,#,Camp Site,ugb_name,0,32;longitude "longitude" true true false 8 Double 0 0,First,#,Camp Site,longitude,-1,-1;latitude "latitude" true true false 8 Double 0 0,First,#,Camp Site,latitude,-1,-1;maptaxlot_hyphen_1 "maptaxlot_hyphen" true true false 17 Text 0 0,First,#,Taxlots,maptaxlot_hyphen,0,17;ownname_1 "ownname" true true false 128 Text 0 0,First,#,Taxlots,ownname,0,128;addr1_1 "addr1" true true false 64 Text 0 0,First,#,Taxlots,addr1,0,64;ownercity_1 "ownercity" true true false 40 Text 0 0,First,#,Taxlots,ownercity,0,40;ownerprvst_1 "ownerprvst" true true false 30 Text 0 0,First,#,Taxlots,ownerprvst,0,30;ownerzip_1 "ownerzip" true true false 10 Text 0 0,First,#,Taxlots,ownerzip,0,10;geocity_name_1 "geocity_name" true true false 32 Text 0 0,First,#,Taxlots,geocity_name,0,32;ugb_name_1 "ugb_name" true true false 32 Text 0 0,First,#,Taxlots,ugb_name,0,32;longitude_1 "longitude" true true false 8 Double 8 38,First,#,Taxlots,longitude,-1,-1;latitude_1 "latitude" true true false 8 Double 8 38,First,#,Taxlots,latitude,-1,-1', "CLOSEST", None, '')
                    values = [rowv for rowv in arcpy.da.SearchCursor(spatialJoin2, ["ownname_1", "addr1_1"])]
                    row[1] = values[0][0]
                    row[2] = values[0][1]
                cursor.updateRow(row)
        print("Updated nearby owner name and address...")

    arcpy.conversion.TableToExcel(spatialJoin, path+'\\most_recent.xlsx')

    print('Exported the join table...')
