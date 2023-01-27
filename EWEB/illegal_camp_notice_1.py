import arcpy, os
from datetime import datetime, date
from homeless import *
import time

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
    
    featureclass = path + '\\MyProject.gdb\\datacopy'
    ti_m = os.path.getmtime(path + '\\MyProject.gdb')
    m_ti = time.ctime(ti_m)
    t_obj = time.strptime(m_ti)
    T_stamp = time.strftime("%Y-%m-%d %H:%M:%S", t_obj)
    todaystr = str(date.today())
    
    if (arcpy.Exists(featureclass)) & (T_stamp.split(' ')[0] == todaystr):
        print('Got the data copy...')
    else:
        # copy the feature layer to edit the fields
        print('Making a copy of the data and this will take a while...')
        arcpy.management.CopyFeatures(camp_site, featureclass)
        print('Copied the data...')
    # add feature to convert dates
    field_names = [f.name for f in arcpy.ListFields(featureclass)]
    newfield = 'Date_str'
    if newfield not in field_names:
        arcpy.management.AddFields(featureclass, [[newfield, "TEXT", 'datestr', 255, '1/18/2023 10:52:35 PM', '']])
        print('Added a date string field...')

    expression = "getDateStr(!Date!)"

    # convert the date field for feature selection
    arcpy.management.CalculateField(featureclass, newfield, expression, "PYTHON3", codeblock)
    print('Formatted the date...')
    # select the most recent date
    selres = arcpy.SelectLayerByAttribute_management(featureclass,
                                                     "NEW_SELECTION", f"Date_str = '{getDateStr(maxdate)}'")
    arcpy.management.CopyFeatures(selres, path + '\\MyProject.gdb\\most_recent')
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
    
    arcpy.analysis.SpatialJoin(selres, fc, path + '\\MyProject.gdb\\HomelessCampSite_SpatialJoin', "JOIN_ONE_TO_ONE", "KEEP_ALL",'Status "Status" true true false 50 Text 0 0,First,#,Homeless Camp Site,Status,0,50;Comments "Comments" true true false 500 Text 0 0,First,#,Homeless Camp Site,Comments,0,500;Date "Date" true true false 8 Date 0 0,First,#,Homeless Camp Site,Date,-1,-1;Submitted_by "Submitted By" true true false 50 Text 0 0,First,#,Homeless Camp Site,Submitted_by,0,50;Dogs_present "Dogs present" true true false 50 Text 0 0,First,#,Homeless Camp Site,Dogs_present,0,50;Unruly_inhabitants "Unruly inhabitants" true true false 50 Text 0 0,First,#,Homeless Camp Site,Unruly_inhabitants,0,50;Hazardous_materials_present "Hazardous materials present" true true false 50 Text 0 0,First,#,Homeless Camp Site,Hazardous_materials_present,0,50;Biohazards_present "Biohazards present" true true false 50 Text 0 0,First,#,Homeless Camp Site,Biohazards_present,0,50;Size_of_encampment "Size of encampment" true true false 50 Text 0 0,First,#,Homeless Camp Site,Size_of_encampment,0,50;GlobalID "GlobalID" false false true 38 GlobalID 0 0,First,#,Homeless Camp Site,GlobalID,-1,-1;maptaxlot_hyphen "maptaxlot_hyphen" true true false 17 Text 0 0,First,#,Lane County Taxlots,maptaxlot_hyphen,0,17;ownname "ownname" true true false 128 Text 0 0,First,#,Lane County Taxlots,ownname,0,128;addr1 "addr1" true true false 64 Text 0 0,First,#,Lane County Taxlots,addr1,0,64;ownercity "ownercity" true true false 40 Text 0 0,First,#,Lane County Taxlots,ownercity,0,40;ownerprvst "ownerprvst" true true false 30 Text 0 0,First,#,Lane County Taxlots,ownerprvst,0,30;ownerzip "ownerzip" true true false 10 Text 0 0,First,#,Lane County Taxlots,ownerzip,0,10;geocity_name "geocity_name" true true false 32 Text 0 0,First,#,Lane County Taxlots,geocity_name,0,32;ugb_name "ugb_name" true true false 32 Text 0 0,First,#,Lane County Taxlots,ugb_name,0,32;longitude "longitude" true true false 8 Double 8 38,First,#,Lane County Taxlots,longitude,-1,-1;latitude "latitude" true true false 8 Double 8 38,First,#,Lane County Taxlots,latitude,-1,-1', "INTERSECT", None, '')
    
    print('Completed a spatial join with taxlot...')
    
    arcpy.conversion.TableToExcel(path + '\\MyProject.gdb\\HomelessCampSite_SpatialJoin', path+'\\most_recent.xlsx')
    
    print('Exported the join table...')
    