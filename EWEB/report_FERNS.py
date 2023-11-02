import win32com.client
from win32com.client import Dispatch, constants
import geopandas as gpd
import pandas as pd
import sys
from datetime import date

today = date.today()
inpath = r"\\clsrv111.int.lcog.org\GIS\projects\UtilityDistricts\eweb\DrinkingWater\EPA319_NPS_grant\ForestApplication\ODF_FACTS_DB\FERNS"
data = gpd.read_file(inpath + "\\FERNS_Model\\FERNS_Final_Products.gdb", layer="FERNSSummary_McKenzie_Joined")
sys.stdout = open(f"{inpath}\\FERNS_log.txt", "a")
print(f"Current update includes {data.shape[0]} records and below shows the summarized acres by activity type:\n")
print(data.groupby('ActType').agg(SumAcres = pd.NamedAgg(column = 'SUM_calc_acres', aggfunc = sum)))
print("\n")

const=win32com.client.constants
olMailItem = 0x0
obj = win32com.client.Dispatch("Outlook.Application")
newMail = obj.CreateItem(olMailItem)
newMail.To = 'CBARROWS@Lcog.org'
#newMail.To = 'DCHEN@Lcog.org'
newMail.Subject = f'Complete FERNS update {str(today)}'
#newMail.Subject = 'test'
newMail.BodyFormat = 2
newMail.HTMLBody = f"""
<HTML><BODY><p>Hi Chrissy,</p> 

This is an auto-generated email from updating the FERNS dashboard. The program running log is located at {inpath}\\FERNS_log.txt. This email notifies you that the update has been completed automatically, and you only need to edit the date info on the <a href='https://lcog.maps.arcgis.com/apps/dashboards/f003689bcb7f45eca5be6f02baada6c0#mode=edit'>dashboard</a>. </p> 

<p>Have a great day!</p></BODY></HTML>

"""
newMail.Send()
print("Sent out the email...")
sys.stdout.close()