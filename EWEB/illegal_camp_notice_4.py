import win32com.client as win32
from homeless import *
import os
import openpyxl
from datetime import date

outpath = r'\\clsrv111.int.lcog.org\GIS\projects\UtilityDistricts\eweb\DrinkingWater\IllegalCampCoordination\Recieved'
path = outpath + '\\IllegalCampNotification_pro'
res = convert_date(str(date.today()))
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
dateinfo = date.today().strftime("%m-%d-%Y")
mail.To = 'dchen@lcog.org'
mail.Subject = f'Illegal Camp Notice to Review {dateinfo}'
mail.Body = outfile
mail.Send()
print("Sent out the email...")