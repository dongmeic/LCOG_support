import win32com.client as win32
import pandas as pd
from homeless import *
import os
import openpyxl
from datetime import date
import sys

def main(args):
    print(args)
    add_pic = args[1].lower()=="true"
    print(f"Add... an updated picture? {add_pic}")
    #return
    outpath = r'\\clsrv111.int.lcog.org\GIS\projects\UtilityDistricts\eweb\DrinkingWater\IllegalCampCoordination\Recieved'
    path = outpath + '\\IllegalCampNotification_pro'
    res = convert_date(str(date.today()))
    #res = convert_date(str(date(2023, 1, 26)))
    Y = res[1]
    m = res[2]
    d = res[3]
    outfolder = os.path.join(outpath, Y, m+'_'+d)
    outfile = f"{outfolder}\IllegalCampNotice_{m+'_'+d+'_'+Y[2:4]}.xlsx"

    if add_pic:     
        wb = openpyxl.load_workbook(outfile)
        ws = wb.active

        pic_path=path+'\\MapUpdated.jpg'
        img = openpyxl.drawing.image.Image(path+'\\MapUpdated.jpg')
        img.height = 255*3
        img.width = 330*3
        img.anchor = 'C5'
        ws.add_image(img)

        wb.save(outfile)
        print("Added the updated image...")

    data = pd.read_excel(outpath+'\\Illegal Camping Report Mailing List.xlsx')
    #data = pd.read_excel('testemail.xlsx')
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    
    mailto = 'LCOGIllegalCampandDebrisCleanup@lcog.org'
    #mailto = 'dchen@lcog.org'
    mail.To = mailto
    mail.CC = ";".join(data['address'])
    mail.Subject = f'Illegal Camping Report {str(date.today())}'
    mail.Body =  """
    Hello, 

    Please see the attached for today's Illegal Camping Report. 
    For questions about this report or the application please contact myself or Chrissy Barrows at LCOG.

    Thank you,
    Dongmei 

    """
    mail.Attachments.Add(outfile)

    mail.Send()
    print("Sent out the emails...")
    
if __name__ == "__main__":
    main(sys.argv)
