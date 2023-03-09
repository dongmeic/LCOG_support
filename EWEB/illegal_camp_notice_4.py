import win32com.client as win32
from homeless import *
import os
import openpyxl
from datetime import datetime
from geopandas import gpd

outpath = r'\\clsrv111.int.lcog.org\GIS\projects\UtilityDistricts\eweb\DrinkingWater\IllegalCampCoordination\Recieved'
path = outpath + '\\IllegalCampNotification_pro'
dt = gpd.read_file(path + '\\MyProject4.gdb', layer= 'most_recent')
res = convert_date(dt.date.values[0].split('T')[0])
#res = convert_date(str(date(2023, 1, 26)))
Y = res[1]
m = res[2]
d = res[3]
outfolder = os.path.join(outpath, Y, m+'_'+d)

pic_path=path+'\\Map.jpg'
outfile = f"{outfolder}\IllegalCampNotice_{m+'_'+d+'_'+Y[2:4]}.xlsx"

wb = openpyxl.load_workbook(outfile)
ws = wb.active

img = openpyxl.drawing.image.Image(path+'\\Map.jpg')
img.height = 255*3
img.width = 330*3
img.anchor = 'C7'
ws.add_image(img)

wb.save(outfile)
print("Added the image...")

outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
input_format = '%m/%d/%Y'
output_format = '%Y-%m-%d'
datetime_object = datetime.strptime(res[0], input_format)
dateinfo = datetime.strftime(datetime_object, output_format)
#dateinfo = date.today().strftime("%m-%d-%Y")
mail.To = 'dchen@lcog.org'
mail.Subject = f'Illegal Camp Notice to Review {dateinfo}'
mail.Body = outfile
mail.Send()
print("Sent out the email...")