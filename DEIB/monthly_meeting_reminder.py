import datetime
from datetime import date, timedelta
import win32com.client
from win32com.client import Dispatch, constants
import pandas as pd
from dateutil import relativedelta

def third_Wednesday(year, month):
    """Return datetime.date for monthly option expiration given year and
    month
    """
    # The 15th is the lowest third day in the month
    third = datetime.date(year, month, 15)
    # What day of the week is the 15th?
    w = third.weekday()
    # Wednesday is weekday 2
    if w != 2:
        # Replace just the day (of month)
        third = third.replace(day=(15 + (2 - w) % 7))
    return third

today = date.today()
year = today.strftime("%Y")
date1 = third_Wednesday(int(year), int(today.strftime("%m")))
cur_m = today.strftime("%B") + ' ' + year
#rota = pd.read_excel(r'T:\DCProjects\DEIB\Facilitator and Notetaker Rotation.xlsx')
rota = pd.read_excel(r'C:\Users\clid1852\OneDrive - lanecouncilofgovernments\DEIB\Facilitator and Notetaker Rotation.xlsx')
cur_fcr = rota.loc[rota.Month == cur_m, 'Facilitator'].values[0]
cur_ntr = rota.loc[rota.Month == cur_m, 'Note Taker'].values[0]
nextmonth = datetime.date.today() + relativedelta.relativedelta(months=2)
ftr_m = nextmonth.strftime("%B") + ' ' + nextmonth.strftime("%Y")
ftr_fcr = rota.loc[rota.Month == ftr_m, 'Facilitator'].values[0]
ftr_ntr = rota.loc[rota.Month == ftr_m, 'Note Taker'].values[0]

const=win32com.client.constants
olMailItem = 0x0
obj = win32com.client.Dispatch("Outlook.Application")
newMail = obj.CreateItem(olMailItem)
newMail.Subject = f'Reminder: DEIB meeting next Wednesday {str(date1)}'
newMail.BodyFormat = 2 # olFormatHTML https://msdn.microsoft.com/en-us/library/office/aa219371(v=office.11).aspx
newMail.HTMLBody =  f"""
<HTML><BODY><p>Hello all,</p> 

<p>Our meeting facilitator and notetaker next week are {cur_fcr} and {cur_ntr}, and in two month are {ftr_fcr} and {ftr_ntr}. Following the links, please find the folders for the <a href="https://lanecouncilofgovernments.sharepoint.com/:f:/r/sites/LCOGDiversityEquityBelonging/Shared%20Documents/Committee%20Meetings/Agendas/2023?csf=1&web=1&e=wBl76p">meeting agenda</a>, and <a href="https://lanecouncilofgovernments.sharepoint.com/:f:/r/sites/LCOGDiversityEquityBelonging/Shared%20Documents/Committee%20Meetings/Meeting%20Notes/2023?csf=1&web=1&e=03DAbf">meeting notes</a>.

Meeting facilitators will need to fill out the agenda details. Thank you! </p> 

<p>Have a great day!</p>

<p>Dongmei on behalf of DEIB Strategic Planning Subcommittee</p></BODY></HTML>
"""
#newMail.To = "dchen@lcog.org"
newMail.To = "LCOGDiversityEquityInclusionBelonging@lcog.org"
#newMail.From = "LCOGDiversityEquityInclusionBelonging@lcog.org"

newMail.Send()