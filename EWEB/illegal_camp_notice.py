import arcpy, os
from datetime import datetime
from homeless import *

arcpy.env.overwriteOutput = True

outpath = r'G:\projects\UtilityDistricts\eweb\DrinkingWater\IllegalCampCoordination\Recieved'
path = outpath + '\\IllegalCampNotification_pro'
camp_site = 'https://services5.arcgis.com/9s1YtFmLS0YTl10F/ArcGIS/rest/services/ZHomeless_Camp_Trash_Collector/FeatureServer/0'

# get the most recent date
listdates1 = []
cursor = arcpy.da.SearchCursor(camp_site, "Date")
for row in cursor:
    listdates1.append(row)

listdates = [dt[0] for dt in listdates1 if dt[0] is not None]    
maxdate = max(listdates)

# check whether there is a need to report
datestr = maxdatestr.split('.')[0].split(' ')[0]
res = convert_date(datestr)
Y = res[1]
m = res[2]
d = res[3]
outfolder = os.path.join(outpath, Y, m+'_'+d)
outfolder_yr = os.path.join(outpath, Y)

if os.path.exists(outfolder):
    print('No need to report!')
else:
    print('Making the report...')
    if not os.path.exists(outfolder_yr):
        os.makedirs(outfolder_yr)
    else:
        os.makedirs(outfolder)
    print('Created the new folder...')
    
    # copy the feature layer to edit the fields
    arcpy.management.CopyFeatures(camp_site, path + '\\MyProject4.gdb\\datacopy')
    print('Copied the data...')
    # add feature to convert dates
    arcpy.management.AddFields(path + '\\MyProject4.gdb\\datacopy', [['Date_str', "TEXT", 'datestr', 255, getDateStr(maxdate), '']])

    expression = "getDateStr(!Date!)"

    codeblock = """
    def getDateStr(date):
        def convert_date(datestr):
            datestrlist = datestr.split('-')
            Y = datestrlist[0]
            m = str(int(datestrlist[1]))
            d = str(int(datestrlist[2]))
            res = m+'/'+d+'/'+Y
            return res

        if date is None:
            res = None
        else:
            strdate = str(date)
            datestr = strdate.split(' ')[0]
            res = convert_date(datestr)
        return res"""

    # convert the date field for feature selection
    arcpy.management.CalculateField(path + '\\MyProject4.gdb\\datacopy', 'Date_str',  expression, "PYTHON3", codeblock)
    print('Formatted the date...')
    # select the most recent date
    selres = arcpy.SelectLayerByAttribute_management(path + '\\MyProject4.gdb\\datacopy',
                                                     "NEW_SELECTION", f"Date_str = '{getDateStr(maxdate)}'")
    arcpy.management.CopyFeatures(selres, path + '\\MyProject4.gdb\\most_recent')
    print('Selected the most recent data...')
    
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
    
    arcpy.analysis.SpatialJoin(selres, fc, path + '\\MyProject4.gdb\\HomelessCampSite_SpatialJoin14c', "JOIN_ONE_TO_ONE", "KEEP_ALL",'Status "Status" true true false 50 Text 0 0,First,#,Homeless Camp Site,Status,0,50;Comments "Comments" true true false 500 Text 0 0,First,#,Homeless Camp Site,Comments,0,500;Date "Date" true true false 8 Date 0 0,First,#,Homeless Camp Site,Date,-1,-1;Submitted_by "Submitted By" true true false 50 Text 0 0,First,#,Homeless Camp Site,Submitted_by,0,50;Dogs_present "Dogs present" true true false 50 Text 0 0,First,#,Homeless Camp Site,Dogs_present,0,50;Unruly_inhabitants "Unruly inhabitants" true true false 50 Text 0 0,First,#,Homeless Camp Site,Unruly_inhabitants,0,50;Hazardous_materials_present "Hazardous materials present" true true false 50 Text 0 0,First,#,Homeless Camp Site,Hazardous_materials_present,0,50;Biohazards_present "Biohazards present" true true false 50 Text 0 0,First,#,Homeless Camp Site,Biohazards_present,0,50;Size_of_encampment "Size of encampment" true true false 50 Text 0 0,First,#,Homeless Camp Site,Size_of_encampment,0,50;GlobalID "GlobalID" false false true 38 GlobalID 0 0,First,#,Homeless Camp Site,GlobalID,-1,-1;maptaxlot_hyphen "maptaxlot_hyphen" true true false 17 Text 0 0,First,#,Lane County Taxlots,maptaxlot_hyphen,0,17;ownname "ownname" true true false 128 Text 0 0,First,#,Lane County Taxlots,ownname,0,128;addr1 "addr1" true true false 64 Text 0 0,First,#,Lane County Taxlots,addr1,0,64;ownercity "ownercity" true true false 40 Text 0 0,First,#,Lane County Taxlots,ownercity,0,40;ownerprvst "ownerprvst" true true false 30 Text 0 0,First,#,Lane County Taxlots,ownerprvst,0,30;ownerzip "ownerzip" true true false 10 Text 0 0,First,#,Lane County Taxlots,ownerzip,0,10;geocity_name "geocity_name" true true false 32 Text 0 0,First,#,Lane County Taxlots,geocity_name,0,32;ugb_name "ugb_name" true true false 32 Text 0 0,First,#,Lane County Taxlots,ugb_name,0,32;longitude "longitude" true true false 8 Double 8 38,First,#,Lane County Taxlots,longitude,-1,-1;latitude "latitude" true true false 8 Double 8 38,First,#,Lane County Taxlots,latitude,-1,-1', "INTERSECT", None, '')
    
    print('Completed a spatial join with taxlot...')
    
    arcpy.conversion.TableToExcel(path + '\\MyProject4.gdb\\HomelessCampSite_SpatialJoin14c', path+'\\most_recent.xlsx')
    