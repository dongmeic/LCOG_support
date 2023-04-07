import win32com.client as win32
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

outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = 'dchen@lcog.org'
mail.Subject = f'Complete FERNS update {str(today)}'
mail.Body = inpath+'\\FERNS_log.txt'
mail.Send()
print("Sent out the email...")
sys.stdout.close()