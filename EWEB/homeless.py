
# convert hour format to am/pm
def convert_hour(str_h):
    h = int(str_h)
    if h >= 0 and h <= 11:
        res = [str_h, 'AM']
    elif h == 12:
        res = [str_h, 'PM']
    elif h > 12 and h <=23:
        res = [str(h-12), 'PM']
    return res

# convert date format
def convert_date(datestr):
    datestrlist = datestr.split('-')
    Y = datestrlist[0]
    m = str(int(datestrlist[1]))
    d = str(int(datestrlist[2]))
    res = m+'/'+d+'/'+Y
    return res, Y, m, d

# convert datetime format to string
def getDateStr(date):
    if date is None:
        res = None
    else:
        strdate = str(date)
        datestr = strdate.split(' ')[0]
        res = convert_date(datestr)
    return res

# clean all formats
def removeFormatting(ws):
    # ws is not the worksheet name, but the worksheet object
    for row in ws.iter_rows():
        for cell in row:
            cell.style = 'Normal'
    return ws

def convert_dtypes_arcgis(df):
   # Convert dataframe dtypes which are not compatible with ArcGIS
   # Use builtin Pandas dtype conversion
    df = df.convert_dtypes(infer_objects=True)
   # Then str convert any remaining special object/category fields 
    for col in df.columns:
    # print(col, '/', df[col].dtype)
        if df[col].dtype == 'object':
            df[col] = df[col].astype('str')
   # Return modified df
    return df

def trim_field_value(x):
    return x[0:len(x)]