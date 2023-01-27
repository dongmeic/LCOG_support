import pandas as pd
import geopandas as gpd
import os
import requests
from bs4 import BeautifulSoup
from homeless import *
import openpyxl
from win32com.client import Dispatch

outpath = r'G:\projects\UtilityDistricts\eweb\DrinkingWater\IllegalCampCoordination\Recieved'
path = outpath + '\\IllegalCampNotification_pro'

dat = pd.read_excel(path+'\\most_recent.xlsx')
cols2drop = ['OBJECTID', 'Join_Count', 'Unruly_inhabitants']
dat = dat.drop(cols2drop, axis=1)
dat.loc[:, 'TARGET_FID'] = dat.loc[:, 'TARGET_FID'] + 1085

intakepath = r'G:\projects\UtilityDistricts\eweb\DrinkingWater\RiparianEcosystemMarketplace\market_area\REM_area.gdb'
intake_areas = gpd.read_file(intakepath, driver='FileGDB', layer='AboveIntake')
points = gpd.read_file(path + '\\MyProject.gdb', driver='FileGDB', layer='HomelessCampSite_SpatialJoin')
points = points.to_crs(epsg=2914)
print("Read data...")

urlstart ='https://services5.arcgis.com/9s1YtFmLS0YTl10F/arcgis/rest/services/ZHomeless_Camp_Trash_Collector/FeatureServer/0/'
urlend = '/attachments?f=html&token='

datestr = points.Date.values[0].split('T')[0]
res = convert_date(datestr)
Y = res[1]
m = res[2]
d = res[3]
outfolder = os.path.join(outpath, Y, m+'_'+d)
filename = 'IllegalCampNotice_'+m+'_'+d+'_'+Y[2:4]+'.xlsx'
file = os.path.join(outfolder, filename)
print("Got file name...")

for pID in points.index:
    point = points[points.index==pID]
    if all(intake_areas.contains(point)):
        dat.loc[pID, 'Above Intake'] = 'Yes'
    else:
        dat.loc[pID, 'Above Intake'] = 'No'
    FID = dat.loc[pID, 'TARGET_FID']
    url= urlstart+str(FID)+urlend
    resp=requests.get(url)
    links = []
    if resp.status_code==200:
        soup=BeautifulSoup(resp.text,'html.parser')
        for link in soup.findAll('a'):
            links.append(link.get('href'))
    else:
        print("Error")
    attached = [link for link in links if 'attachments' in link]
    if len(attached)==0:
        dat.loc[pID, 'Photos'] = 'NA'
    elif len(attached)==1:
        dat.loc[pID, 'Photos'] = 'https://services5.arcgis.com' + attached[0]
    else:
        dat.loc[pID, 'Photos'] = '; '.join(['https://services5.arcgis.com' + s for s in attached])

print("Edited data...")

dat.loc[:, 'Date'] = dat.Date.astype(str)
dat.to_excel(file, index=False)
print("Exported data...")

dat = pd.read_excel(file)
wb = openpyxl.load_workbook(file)
ws = wb.active
ws = removeFormatting(ws)
for pID in points.index:
    photovalue = dat.loc[pID, 'Photos']
    if photovalue == 'NA':
        print(f"No photos at Point {dat.loc[pID, 'TARGET_FID']}")
    else:
        ws.cell(row=2, column=21).value = 'Yes'
        if ';' in photovalue: 
            urls = photovalue.split('; ')
            for i in range(0, len(urls)):
                ws.cell(row=2, column=22+i).value = '=HYPERLINK("{}", "{}")'.format(urls[i],'Photo '+str(i+1))
                ws.cell(row=2, column=22+i).style = "Hyperlink"
        else:
            ws.cell(row=2, column=22).value = '=HYPERLINK("{}", "{}")'.format(photovalue,'Photo')
            ws.cell(row=2, column=22).style = "Hyperlink"
wb.save(file)
print("Checked photos...")
excel = Dispatch('Excel.Application')
wb = excel.Workbooks.Open(file)
excel.Worksheets(1).Activate()
excel.ActiveSheet.Columns.AutoFit()
wb.Save()
print("Autofitted columns...")


