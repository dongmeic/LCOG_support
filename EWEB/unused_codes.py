datapath = max([i for i in subfolderlist if "Ferns_Noaps_Polygons" in i], key=os.path.getmtime)
download_date = datapath.split("Ferns_Noaps_Polygons_")[1][0:8]

for row in arcpy.da.SearchCursor(camp_site, ["Date", "OBJECTID"]):
    while row[0] == maxdate:
        selres = arcpy.SelectLayerByAttribute_management(camp_site,
                                                            "ADD_TO_SELECTION", f"OBJECTID = {row[1]}")
arcpy.management.CopyFeatures(selres, path + '\\MyProject4.gdb\\most_recent')

cs_fc = path + '\\MyProject4.gdb\\most_recent'
with arcpy.da.UpdateCursor(cs_fc, "OBJECTID") as cursor:
    for row in cursor:
        if row[0] > 0:
            cursor.deleteRow()

targetCursor = arcpy.da.InsertCursor(cs_fc,"*")
targetCursor.insertRow(row)

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

featureclass = path + '\\MyProject4.gdb\\datacopy'
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
    