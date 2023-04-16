import pandas as pd
import os, re, time, requests, sys, json, shutil, os.path
from datetime import datetime, date
import numpy as np
import geopandas as gpd
from sqlalchemy import create_engine

pd.options.mode.chained_assignment = None

path = r'T:\DCProjects\Support\Lane\HfG'
inpath = path + '\\DataFromThem'
who = pd.read_csv(inpath + '\\who_helped_others.csv')

# application question history
aqh = pd.read_csv(inpath + '\\ApplicationQuestionHistory.csv')

# oa - online applications
oa = pd.read_csv(inpath + '\\OnlineApplications.csv')

# application members
am = pd.read_csv(inpath + '\\ApplicationMembers.csv')

# application contacts
ac = pd.read_csv(inpath + '\\ApplicationContacts.csv')

# applicant income
ai = pd.read_csv(inpath + '\\ApplicantIncome.csv')

engine = create_engine(   
"mssql+pyodbc:///?odbc_connect="
"Driver%3D%7BODBC+Driver+17+for+SQL+Server%7D%3B"
"Server%3Drliddb.int.lcog.org%2C5433%3B"
"Database%3DRLIDGeo%3B"
"Trusted_Connection%3Dyes%3B"
"ApplicationIntent%3DReadWrite%3B"
"WSID%3Dclwrk4087.int.lcog.org%3B")

zip_sql = '''
SELECT 
zipcode AS ZipCode,
mailcity AS City,
Shape.STAsBinary() AS geometry
FROM dbo.ZIPCode;
'''

# this group has one id matched with two addresses and the addresses return different results from geocoding
adr2cor = ['1665 Oak Patch Rd , Eugene, OR 97402', 
 '1699 N Terry St , Eugene, OR 97402', 
 '1468 Harvard Drive , Springfield, OR 97477',
 '1190 W 6Th Ave , Eugene, OR 97402',
 '62F28 Main Street #1, Springfield, OR 97478',
'341 E 12Th Ave , Eugene, OR 97401',
'1880 Cleveland St , Eugene, OR 97405',
'717 Hwy 99 N , Eugene, OR 97402',
'792 Clone St , Yoncalla, OR 97499',
'19554 Debra Dr , Springfield, OR 97477',
'96100 Mills Rd Apt 710, Houston, TX 77070']
adrcored = ['1665 Oak Patch Rd 229, Eugene, OR 97402', 
 '1699 N Terry St Spc 35, Eugene, OR 97402', 
 '1468 Harbor Dr , Springfield, OR 97477',
 '1190 W 6Th Ave # 295, Eugene, OR 97402',
 '6228 Main St Apt 1, Springfield, OR 97478',
'341 E 12Th Ave 573-99-1014, Eugene, OR 97401',
'1880 Cleveland St Apt 1, Eugene, OR 97405',
'717 Highway 99 N. T-9, B-4, Eugene, OR 97402',
'792 Clone St 7, Yoncalla, OR 97499',
'1955 Debra Dr , Springfield, OR 97477',
'9100 Mills Rd Apt 710, Houston, TX 77070']

# this group has one id matched with two addresses and the addresses return the same from geocoding
adr2cor0 = ['1624 Water St None, Springfield, OR 97477',
           '1025 West Hilliard Lane , Eugene, OR 97404',
           '40 Owosso Dr Unit 15, Eugene, OR 97404',
           '1491 5Th Street 23, Springfield, OR 97477',
           '1973 18Th Street 4, Springfield, OR 97477',
           '255High Street #318, Eugene, OR 97401',
           'Eugene Mission , Eugene, OR 97402',
           '1950 Laurel Ave Ne Apt 15, Salem, OR 97301',
           '310 Pitney Lane Unit 5, Junction City, OR 97448',
           '755 East Broadway #62 , Eugene, OR 97402',
           '1120 W 24Th Avenue , Eugene, OR 97405',
           '448 W. 12Th 3, Eugene, OR 97401',
           '3618 W 18Th Ave Apt 2 , Eugene, OR 97402',
           '1547 City View St 201, Eugene, OR 97402',
           '969 Highway 99 N # 13/14 , Eugene, OR 97402',
           '1995 Amazon Pkw , Eugene, OR 97402',
           '615 Commercial St Ne (Day Shelter Homeless) , Salem, OR 97301',
           '1096 N Street , Springfield, OR 97477',
           '2527 Lakeview Dr. Apt 102, Eugene, OR 97408',
           '111N N Garfield St # 4, Eugene, OR 97402',
           'Rv On River Rd. , Eugene, OR 97404',
           'White Bird Clinic 341 E 12Th Ave , Eugene, OR 97401',
           '555 Tyler Street 22, Eugene, OR 97401',
           '100 Port Rd 4, Pt Arena, CA 95468',
           '87687 Hwy 101 2, Florence, OR 97439',
           'Rv On River Rd. , Eugene, OR 97404',
           '732 64Th Street , Springfield, OR 97478',
           '305 1/2 23Rd St , Springfield, OR 97477',
           '4675 Goodpasture Loop Apt 136 , Eugene, OR 97401',
           '335 W. 2Nd Ave 102, Eugene, OR 97402',
           '3655 W. 13Th Ave. C-110, Eugene, OR 97402',
           '298 E Oregon Sp M28, Creswell, OR 97426',
           '76251 Rainbow St Unit 25 , Oakridge, OR 97463',
           '1602 Water Street , Springfield, OR 97477',
           '4069 Southway Lp , Springfield, OR 97478',
           '435 River Lp2 , Eugene, OR 97404',
           '56676 Mckenzie Hwy , Mc Kenzie Brg, OR 97413',
           '388 Hwy 99 N. , Eugene, OR 97402',
           '1141 1/2  Main St , Springfield, OR 97404',
           '5664 A Street , Springfield, OR 97478']
adrcored0 = ['1624 Water St , Springfield, OR 97477',
            '1025 W Hilliard Ln , Eugene, OR 97404',
            '40 Owosso Dr # 15, Eugene, OR 97404',
            '1491 5Th Street Apt 23, Springfield, OR 97477',
            '1973 18Th St Apt 4, Springfield, OR 97477',
            '255 High St Apt 318, Eugene, OR 97401',
            '1542 W 1St Ave Eugene Mission, Eugene, OR 97402',
            '1950 Laurel Ave Ne, Apt 15, Salem, OR 97301',
            '310 Pitney Ln Unit 5, Junction City, OR 97448',
            '755 E Broadway #62 , Eugene, OR 97402',
            '1120 W 24Th Ave , Eugene, OR 97405',
            '448 W 12Th Ave Apt 3, Eugene, OR 97401',
            '3618 W 18Th Ave Apt 2, Eugene, OR 97402',
            '1547 City View St Apt 201, Eugene, OR 97402',
            '969 Highway 99 N #13/14, Eugene, OR 97402',
            '1995 Amazon Pkwy , Eugene, OR 97405',
            '615 Commercial St Ne , Salem, OR 97301',
            '1096 N St , Springfield, OR 97477',
            '2527 Lakeview Dr Apt 102, Eugene, OR 97408',
            '111 N Garfield St # 4, Eugene, OR 97402',
            'River Rd. In Motorhome , Eugene, OR 97404',
            '341 E 12Th Ave , Eugene, OR 97401',
            '555 Tyler Street 22, Eugene, OR 97402',
            '100 Port Rd , Pt Arena, CA 95468',
            '87687 Highway 101 Apt 2, Florence, OR 97439',
            'River Rd. In Motorhome , Eugene, OR 97404',
            '732 64Th St , Springfield, OR 97478',
            '305 23Rd St , Springfield, OR 97477',
            '4675 Goodpasture Loop Apt 136, Eugene, OR 97401',
            '335 W. 2Nd Ave 102, Eugene, OR 97401',
            '3655 W 13Th Ave C-110, Eugene, OR 97402',
            '298 E Oregon Sp , Creswell, OR 97426',
            '76251 Rainbow St Unit 25, Oakridge, OR 97463',
            '1602 Water St , Springfield, OR 97477',
            '4069 Southway Loop , Springfield, OR 97478',
            '435 River Loop 2 , Eugene, OR 97404',
            '56676 Mckenzie Hwy , Mckenzie Bridge, OR 97413',
            '388 Highway 99 N , Eugene, OR 97402',
            '1141 Main St , Springfield, OR 97404',
            '5664 A St , Springfield, OR 97478']

# this group has one id matched with three addresses
adr2cor1 = ['2515 Frontier Dr Apt, Eugene, OR 97401',
           '448 W. 12Th 3, Eugene, OR 97408',
           '448 W. 12Th 3, Eugene, OR 97401']
adrcored1 = ['2515 Frontier Dr Apt 17, Eugene, OR 97401',
            '448 W 12Th Ave Apt 3, Eugene, OR 97401',
            '448 W 12Th Ave Apt 3, Eugene, OR 97401']
adr2cor2 = adr2cor + adr2cor0 + adr2cor1
adrcored2 = adrcored + adrcored0 + adrcored1
adrcor_dict = {adr2cor2[i]: adrcored2[i] for i in range(len(adr2cor2))}

oldnms = [x for x in oa.columns if len(x) > 10] + ['Relationship', 'Citizenship']
newnms = ['KeyID', 'MailAdr1', 'MailAdr2', 'LegalAdr1', 'LegalAdr2', 'Mobile',
          'OtrContact', 'EmancMinor', 'HHSize', 'HHMinors', 'IncAnnual',
          'InChecking', 'IncSavings', 'Investment', 'IncRealEst','IncomeOthr',
          'AsChecking', 'AstSavings', 'AstInvestm', 'AstRealEst', 'AstOther',
          'QuestIDs', 'OptOt92006', 'PrAgencyID', 'ApplicatTS', 'AddrsValid',
          'LotteryNm', 'Citizenshp', 'AccntEmail', 'Relatship', 'Citizship']
colnm_dict = {oldnms[i]:newnms[i] for i in range(len(oldnms))}

ethn_dict = {1:"Hispanic or Latino", 0:"Not Hispanic or Latino"}
race_dict = {'1':"White", 
             '2':"Black/African American", 
             '3':"American Indian/Alaska Native", 
             '4':"Asian", 
             '5':"Native Hawaiian/Other Pacific Islander",
             '6':"Other"}
citizen_dict = {"EC": "Eligible Citizen", 
                "EN":"Eligible Non-Citizen", 
                "IC":"Ineligible Child of head of household",
                "IN":"Ineligible Noncitizen",
                "ND":"No Documentation Submitted",
                "PV":"Pending Verification"}

def get_counts_pip(points, polygon, idcol, cntnm):
    pip_df = get_pip(points=points, polygon=polygon, idcol=idcol)
    cnt = pip_df[idcol].value_counts().rename_axis(idcol).reset_index(name=cntnm)
    return cnt

def combine_counts_pip(pntlist, polygon, idcol, cntnmlist):
    out = polygon
    for i in range(2):
        cnt=get_counts_pip(pntlist[i], polygon, idcol, cntnmlist[i])
        out=out.merge(cnt, on=idcol, how='left')
    return out

def race_check(x, race):
    if race in x:
        res = 1
    else:
        res = 0
    return res

def reorganize_loc(export=True):
    locdf = gpd.read_file(path+'\\output\\all_locations.shp')
    locdf['CorAddress'] = locdf.Address.map(adrcor_dict)
    locdf.loc[locdf.CorAddress.isnull(), 'CorAddress'] = locdf.loc[locdf.CorAddress.isnull(), 'Address']
    nlocdf = locdf.drop_duplicates(subset=['CorAddress'])
    nlocdf.drop(columns=['Address'], inplace = True)
    nlocdf.rename(columns={'CorAddress':'Address'}, inplace=True)
    if export:
        nlocdf.to_file(path+'\\output\\cor_all_locations.shp')
    return nlocdf

def map_race(a):
    lst = a.split(',')
    lst = [*map(lambda x: x.replace(' ', ''), lst)]
    lst = [*map(lambda x:race_dict[x], lst)]
    return lst

def mixed_race(x):
    if len(x) > 1:
        res = 1
    else:
        res = 0
    return res

def unique(list1):
    """
    This function takes a list and returns a list of unique values
    """
    x = np.array(list1)
    return list(np.unique(x))

def age(x):
    if x <= 2:
        res = 'Infants (0-2)'
    elif x > 2 and x <= 12:
        res = 'Children (3-12)'
    elif x > 12 and x <= 17:
        res = 'Teenagers (13-17)'
    elif x >= 18 and x <= 65:
        res = 'Adults (18-65)'
    else:
        res = 'Seniors (65+)'
    return res

disa_dict = {0:"No", 1:"Yes"}

def reorganize_am(df):
    am = get_name_id(df)
    am['Race'] = am.Race.apply(lambda x: ', '.join(re.sub("[^0-9]","",x)))
    am['RaceNotes'] = am.Race.apply(lambda x: map_race(x))
    am['MultiRace'] = am.RaceNotes.apply(lambda x: mixed_race(x))
    am['RaceNotes'] = am.RaceNotes.str.join(',')
    am['White'] = am.RaceNotes.apply(lambda x: race_check(x, race='White'))
    am['African'] = am.RaceNotes.apply(lambda x: race_check(x, race='African'))
    am['IndianAlsk'] = am.RaceNotes.apply(lambda x: race_check(x, race='Indian/Alaska'))
    am['Asian'] = am.RaceNotes.apply(lambda x: race_check(x, race='Asian'))
    am['HawaiianOr'] = am.RaceNotes.apply(lambda x: race_check(x, race='Hawaiian/Other'))
    am['RaceOther'] = am.Race.apply(lambda x: race_check(x, race='6'))
    am.loc[am.MultiRace==0, 'Race2'] = am.loc[am.MultiRace==0, 'RaceNotes']
    am.loc[am.MultiRace==1, 'Race2'] = 'Multiracial'
    am['CitizNotes'] = am.Citizenship.map(citizen_dict)
    am['EthniNotes'] = am.Ethnicity.map(ethn_dict)
    am['AgeNotes'] = am.Age.apply(lambda x: age(x))
    am['DisaNotes'] = am.Disabled.map(disa_dict)
    return am 

def reorganize_oa(df):
    df = get_name_id(df)
    oa = get_address_df(df)
    adrcols = ['MailAddress1', 'MailAddress2', 'MailCity', 'LegalAddress1','LegalAddress2', 'LegalCity']
    oa[adrcols] = oa[adrcols].apply(lambda x: title_col(x))
    return oa

def title_col(v):
    return list(map(lambda x: check_str(x), v))

def check_str(x):
    if x is not None:
        x = str(x).title()
    else:
        x = None
    return x

def reorganize_aqh():
    t0 = time.time()
    sel_p7 = ((aqh.Preference=='P7') & (aqh.Answer=='Yes') & ~(aqh.Response.astype(str) == 'nan'))
    aqh.loc[sel_p7, 'P7SCat'] = aqh[sel_p7]['Response'].apply(lambda x: categorize_p7_s(x))
    aqh.loc[sel_p7, 'P7BCat'] = aqh[sel_p7]['P7SCat'].apply(lambda x: categorize_p7_b(x))
    sel_p8 = ((aqh.Preference=='P8') & (aqh.Answer=='Yes'))
    aqh.loc[aqh.Response=='Kat', 'Response'] = 'Kat '
    aqh.loc[sel_p8, 'P8SCat'] = aqh[sel_p8]['Response'].apply(lambda x: categorize_p8_s(x))
    aqh.loc[sel_p8, 'P8BCat'] = aqh[sel_p8]['P8SCat'].apply(lambda x: categorize_p8_b(x))
    sel_p9 = ((aqh.Preference=='P9') & ~(aqh.Response.astype(str) == 'nan'))
    aqh.loc[sel_p9, 'P9SCat'] = aqh[sel_p9]['Response'].apply(lambda x: categorize_p9_s(x))
    aqh.loc[sel_p9, 'P9BCat'] = aqh[sel_p9]['P9SCat'].apply(lambda x: categorize_p9_b(x))
    aqh.loc[sel_p9, 'P9Cat'] = aqh[sel_p9]['Response'].apply(lambda x: categorize_p9_c(x))
    elapsed = (time.time() - t0) / 60
    print('Elapsed time for reorganizing question history: %.2fminutes' % (elapsed))
    return aqh

def get_address_df(df):
    df.loc[df.LegalAddress2.isnull(), 'LegalAddress2'] = ''
    df.loc[df.MailAddress2.isnull(), 'MailAddress2'] = ''
    nonaddr = ['na', 'Homeless', 'In vehicle','homeless','HOMELESS','Eugene','My car','None',
               'general delivery', 'live on the streets', 'In vehicle']
    sel = (oa.LegalAddress1.notnull()) & (~oa.LegalAddress1.isin(nonaddr)) & (oa.LegalCity.notnull())
    df.loc[sel, 'Address'] = df[sel].apply(lambda row: get_full_address(
                                         row.LegalAddress1, 
                                         row.LegalAddress2, 
                                         row.LegalCity, 
                                         row.LegalState, 
                                         row.LegalZIP), axis=1)
    excl = 'General Delivery Melissa A Fletcher'
    sel2 = (oa.LegalAddress1.isnull()) & (oa.MailAddress1.notnull()) & (oa.MailAddress1 != excl)
    df.loc[sel2, 'Address'] = df[sel2].apply(lambda row: get_full_address(
                                         row.MailAddress1, 
                                         row.MailAddress2, 
                                         row.MailCity, 
                                         row.MailState, 
                                         row.MailZIP), axis=1)
    df['CorAddress'] = df.Address.map(adrcor_dict)
    df.loc[df.CorAddress.isnull(), 'CorAddress'] = df.loc[df.CorAddress.isnull(), 'Address']
    df.drop(columns=['Address'], inplace = True)
    df.rename(columns={'CorAddress':'Address'}, inplace=True)
    return df

def get_name_id(df):
    df['Age'] = df['DOB'].apply(lambda x: calculate_age(x))
    df.loc[df.NameMiddle.isnull(), 'NameMiddle'] = ''
    df.loc[df.SSN.isnull(), 'SSN'] = 0
    df['ID'] = df[['NameFirst', 'NameMiddle', 'NameLast', 'Age', 'SSN']].apply(lambda row: '-'.join([row.NameFirst, row.NameMiddle, row.NameLast, str(row.Age), str(int(row.SSN))]), axis=1)
    return df

def get_oa_gdf(df, export=False):
    oa = reorganize_oa(df)
    locdf = gpd.read_file(path+'\\output\\cor_all_locations.shp')
    df = oa.merge(locdf, on='Address')
    oa_gdf = gpd.GeoDataFrame(df, geometry='geometry')
    if export:
        oa.to_csv(path + '\\output\\online_application.csv', index=False)
        oa_gdf.rename(columns=colnm_dict, inplace=True)
        oa_gdf.to_file(path+'\\output\\online_application.shp')
    return oa, oa_gdf

def get_am_gdf(oa, am, export=False):
    am = reorganize_am(am)
    oa = reorganize_oa(oa)
    oa, oa_gdf = get_oa_gdf(oa)
    cols = ['KeyApplication', 'Language', 'MailAddress1', 'MailAddress2',
       'MailCity', 'MailState', 'MailZIP', 'MailZIP4', 'LegalAddress1',
       'LegalAddress2', 'LegalCity', 'LegalState', 'LegalZIP', 'LegalZIP4', 'Address']
    am_df = am.merge(oa[cols], on = 'KeyApplication')
    cols.append('geometry')
    amdf = am.merge(oa_gdf[cols], on = 'KeyApplication')
    am_gdf = gpd.GeoDataFrame(amdf, geometry='geometry')
    if export:
        am_df.to_csv(path + '\\output\\application_members.csv', index=False)
        am_gdf.rename(columns=colnm_dict, inplace=True)
        am_gdf.to_file(path+'\\output\\application_members.shp')
    return am_df, am_gdf
    
# points in polygons
def get_pip(points, polygon, idcol):
    id_list = list(polygon[idcol].values)
    df = pd.DataFrame().reindex_like(points).dropna()
    polygon = polygon.to_crs(crs=points.crs)
    for ID in id_list:
        pol = (polygon.loc[polygon[idcol]==ID])
        pol.reset_index(drop = True, inplace = True)
        pip_mask = points.within(pol.loc[0, 'geometry'])
        pip_data = points.loc[pip_mask].copy()
        pip_data[idcol]= ID
        df = df.append(pip_data)
    df.reset_index(inplace=True, drop=True)
    df = df.drop(columns='geometry')
    return df

def readZipCode():
    ZipCode = gpd.GeoDataFrame.from_postgis(zip_sql, engine, geom_col='geometry')
    ZipCode.crs = "EPSG:2914"
    return ZipCode

zip_shp = readZipCode()

def get_mailAdr_df(export=True):
    excl = 'General Delivery Melissa A Fletcher'
    cols = ['KeyApplication', 'MailAddress1', 'MailAddress2', 'MailCity', 'MailState', 'MailZIP']
    mail = oa[(oa.LegalAddress1.isnull()) & (oa.MailAddress1.notnull()) & (oa.MailAddress1 != excl)][cols]
    mail.loc[mail.MailAddress2.isnull(), 'MailAddress2'] = ''
    print(f"there are {mail.shape[0]} records with a mail address")
    mail['Address'] = mail.apply(lambda row: get_full_address(
                                         row.MailAddress1, 
                                         row.MailAddress2, 
                                         row.MailCity, 
                                         row.MailState, 
                                         row.MailZIP), axis=1)
    maildf = mail[['MailAddress1', 'MailAddress2', 'MailCity', 'MailState', 'MailZIP', 'Address']].drop_duplicates()
    print(f"there are {maildf.shape[0]} unique mail addresses")
    t0 = time.time()
    lonlat_df = get_lonlat_df(maildf.Address.unique())
    elapsed = (time.time() - t0) / 60
    print('Elapsed time for geocoding: %.2fminutes' % (elapsed))
    if export:
        mail.to_csv(path+'\\output\\mail_address.csv', index=False)
        lonlat_df.to_file(path+'\\output\\mail_locations.shp')
    return mail, maildf, lonlat_df

def get_legalAdr_df(export=True):
    nonaddr = ['na', 'Homeless', 'In vehicle','homeless','HOMELESS','Eugene','My car','None',
               'general delivery', 'live on the streets', 'In vehicle']
    cols = ['KeyApplication', 'LegalAddress1', 'LegalAddress2', 'LegalCity', 'LegalState', 'LegalZIP']
    legal = oa[(oa.LegalAddress1.notnull()) & (~oa.LegalAddress1.isin(nonaddr)) & (oa.LegalCity.notnull())][cols]
    legal.loc[legal.LegalAddress2.isnull(), 'LegalAddress2'] = ''
    legal['Address'] = legal.apply(lambda row: get_full_address(
                                         row.LegalAddress1, 
                                         row.LegalAddress2, 
                                         row.LegalCity, 
                                         row.LegalState, 
                                         row.LegalZIP), 
            axis=1)
    t0 = time.time()
    lonlat_df = get_lonlat_df(legal.Address.unique())
    elapsed = (time.time() - t0) / 60
    print('Elapsed time for geocoding: %.2fminutes' % (elapsed))
    if export:
        legal.to_csv(path+'\\output\\legal_address.csv', index=False)
        lonlat_df.to_file(path+'\\output\\locations.shp')
    return legal, lonlat_df

def get_lonlat_df(toCheck):
    lat = list(map(lambda x: get_loc_info(x)['lat'], toCheck))
    lng = list(map(lambda x: get_loc_info(x)['lng'], toCheck))
    adr = list(map(lambda x: get_loc_info(x)['adr'], toCheck))
    df = pd.DataFrame(np.array([toCheck, lng, lat, adr]).T, columns=['Address', 'Longitude', 'Latitude', 'Location'])
    gdf = gpd.GeoDataFrame(df, crs="EPSG:4326", geometry=gpd.points_from_xy(df.Longitude, df.Latitude))
    return gdf

def get_loc_info(x='Alvadore, OR'):
    
    GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

    params = {
        'address': x,
        'sensor': 'false',
        'region': 'usa',
        'key': 'AIzaSyAk8bBxbwFmP_adCiSIK4CzqkNl6CdjLqc'
    }

    # Do the request and get the response data
    req = requests.get(GOOGLE_MAPS_API_URL, params=params)
    res = req.json()
    if res['status'] == 'ZERO_RESULTS':
        print(f'{x} returns no results')
    else:
        # Use the first result
        result = res['results'][0]
        geodata = dict()
        geodata['lat'] = result['geometry']['location']['lat']
        geodata['lng'] = result['geometry']['location']['lng']
        geodata['adr'] = result['formatted_address']
        #print('{address}. (lat, lng) = ({lat}, {lng})'.format(**geodata))
        return geodata

def get_full_address(address1, address2, city, state, zipcode): #ID
    #print(ID)
    zipcode = str(int(zipcode))
    if len(zipcode) == 4:
        zipcode = '0'+zipcode
    address = address1.title() + ' ' + address2.title() + ', ' + city.title() + ', ' + state + ' ' + zipcode
    return address

def calculate_age(dob):
    born = datetime.strptime(dob, '%Y-%m-%d')
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def getNames(df, detailed_name):
    names = list(df.loc[df['Detailed Name']==detailed_name, 'name'].unique())
    return '|'.join(names)

def categorize_p7_s(x):
    ff = re.search("at ex|With gf|with ex|an Ex|my ex|mom|daughter|son|father|Mother|sister|brother|family|niece|wife|parent|cousin|step child|spouse|daugheter|daighter|daugter|daugther|husband|uncle|aunt|guardian|Dad|Relative|adult|friend|Familial|Causin|girlfriend|Frend|Roommate|neighbor|fmaily|Freind|friemd|Firend|gma|grandma|duaghter|froiend|Firend|Sibling|barkhimer|kids|aquaintence|aquaintance|Acquaintance|fiend|Famoly|familiy|fiend|Parent|Families|casa de amigo|Parwnts|in laws|someone else's|faniky|property|in-laws|neice", x, re.IGNORECASE)
    svdp = re.search("Vincent|SVDP|SVPD|Second chance|St.V|St V|sleep|Swick|Sarah Koski|Jeff|Amber|Vikki|Aspiranti|Aspirnanti|Ashely|st. |First place|1st place|Avdp|Dawn to dawn|Dusk to Dawn|Dusk 2 Drawn|outreach pallet homes",x, re.IGNORECASE)
    cf = re.search("couch|sofa|housesitting|from house to house|Place to place|surfing", x, re.IGNORECASE)
    wf = re.search("Willamette|Willammette|WF|wallamete|wamfam|wam fam|willimatte|Wilammette", x, re.IGNORECASE)
    tc = re.search("treatment|recovery|rehabilitation", x, re.IGNORECASE)
    sha = re.search("Sherman", x, re.IGNORECASE)
    a = re.search("Alluvium", x, re.IGNORECASE)
    st = re.search("tent|street|ave|Eugene|drive|highway|Camp|st |river|RD|park|Outside|armitage|moving around|glenwood|woods|Out side|outdoors", x, re.IGNORECASE)
    v = re.search("car|trailer|van|rv|Vehicle|motor|truck|5th wheel|automobile|jeep|Toyota|Vehcile", x, re.IGNORECASE)
    th = re.search("transitional|Oxford|tranistional|Transition|tranistional|transtional|Transition|Transactional|Transitiopnal|Trans. Housing", x, re.IGNORECASE)
    lg = re.search("new roads|looking glass|lookingglass", x, re.IGNORECASE)
    wb = re.search("About to|Losing|Getting|Just|day notice|90|wil|ends|last resort|going to be", x, re.IGNORECASE)
    e = re.search("Emergency", x, re.IGNORECASE)
    si = re.search("Sponsor|megan|Meghan|Spnors|Spobnsor's|sponsers|Sponosors|Sponsons|sponsosrs"+'|'+getNames(df=who, detailed_name='Sponsors Inc Staff'), x, re.IGNORECASE)
    gh = re.search("guest house|GuestHouse|guess house", x, re.IGNORECASE)
    em = re.search("julie hansen|mission|Mision", x, re.IGNORECASE)
    sv = re.search("Square one|Opportunity|OPPERTUNITY|Opertunity|Dwayne|Rosa Village", x, re.IGNORECASE)
    h = re.search("Studios|hotel|Comfort Suites|Econo Lodge", x, re.IGNORECASE)
    m = re.search("motel", x, re.IGNORECASE)
    bob = re.search("Bridges on Broadway|B O B|BOB|Bridges on  broadway|Bridges on \nbroadway|Bridges of broadway", x, re.IGNORECASE)
    sc = re.search("ShelterCare|Ruby Renfro|SC Staff|Catrina|Amanda|Dana|Alison Pfaff|Shelter care", x, re.IGNORECASE)
    pjr = re.search("Project Roomkey|Project room key|ProjectRoomkey", x, re.IGNORECASE)
    ev = re.search("Everyone", x, re.IGNORECASE)
    s = re.search("shelter|hut|Sheleter", x, re.IGNORECASE)
    css = re.search("CSS|Community Supported Shelters|Destinee Thompson|Safe Spot|Conestoga Hut|Community Supported", x, re.IGNORECASE)
    r = re.search("Sober|hub",x, re.IGNORECASE)
    t = re.search("Temporary|currently|RENTING|temp housing", x, re.IGNORECASE)
    fema = re.search("FEMA", x, re.IGNORECASE)
    c = re.search("condemed", x, re.IGNORECASE)
    g = re.search("garage|storage|barn|back yard|Backyard", x, re.IGNORECASE)
    hw = re.search("halfway", x, re.IGNORECASE)
    up = re.search("habitation|home security issue|unsafe environment|uninhabitable", x, re.IGNORECASE)
    rest = re.search("rest|entertainment center|back room", x, re.IGNORECASE)
    oasis = re.search("Oasis", x, re.IGNORECASE)
    hfg = re.search("homes for good", x, re.IGNORECASE)
    lp = re.search("Eugene|Springfield|Florence|Portland|rural|Oregon|California|CA|Or 9|Cottage Grove|Nevada| ST|county|Hwy|garfield| dr|Braeman Village|W 24th|Roosevelt|Harlow|Broadway|Redwood|Venta|Veneta|Antelope Way", x, re.IGNORECASE)
    ml = re.search("McKenzie Living", x, re.IGNORECASE)
    fh = re.search("Foster home", x, re.IGNORECASE)
    
    if wf:
        res = "Willamette Family"
    elif svdp:
        res = "SVDP Shelter"
    elif oasis:
        res = "OASIS"
    elif v:
        res = "in a vehicle"
    elif ff:
        res = "family/friends'"
    elif cf:
        res = "couch surfing"
    elif sha:
        res = "Sherman Housing Authority"
    elif hfg:
        res = "Homes For Good"
    elif up:
        res = "uninhabitable place"
    elif fema:
        res = "FEMA housing"
    elif a:
        res = "Alluvium"
    elif pjr:
        res = "Project Roomkey"
    elif ml:
        res = "McKenzie Living"
    elif th:
        res = "transitional housing"
    elif rest:
        res = "rest areas"
    elif e:
        res = "Emergency shelter"
    elif ev:
        res = "Everyone Village"
    elif si:
        res = "Sponsors"
    elif gh:
        res = "Guest House"
    elif em:
        res = "Eugene Mission"
    elif sv: 
        res = "SquareOne Villages"
    elif h:
        res = "hotel"
    elif m:
        res = "motel"
    elif r:
        res = "Inpatient Drug Rehab"
    elif tc:
        res = "treatment center"
    elif bob:
        res = "Bridges on Broadway"
    elif css:
        res = "Community Supported Shelters"
    elif sc:
        res = "ShelterCare"
    elif s:
        res = "shelter"
    elif lg:
        res = "Looking Glass"
    elif st:
        res = "tent"
    elif t:
        res = "temporary housing"
    elif c:
        res = "condemned property"
    elif g:
        res = "mixed-use space"
    elif hw:
        res = "halfway housing"
    elif fh:
        res = "foster home"
    elif wb:
        res = "soon to be homeless"
    elif lp:
        res = "unclassified location"
    else:
        res = "unspecified location"
    return res

def categorize_p7_b(x):
    if x in ["Willamette Family", "treatment center", "Guest House", "Inpatient Drug Rehab", "McKenzie Living"]:
        res = "Treatment Facility"
    elif x in ["SVDP Shelter", "ShelterCare", "Community Supported Shelters", "shelter", "Eugene Mission", "Emergency shelter", "Project Roomkey", "Everyone Village", "FEMA housing"]:
        res = "Shelter"
    elif x in ["Sponsors", "halfway housing"]:
        res = "Correctional Institution" 
    elif x in ["Looking Glass", "OASIS", "foster home"]:
        res = "Community Services Organization"
    elif x in ["Bridges on Broadway", "Homes For Good"]:
        res = "Homes For Good"
    elif x in ["SquareOne Villages", "Sherman Housing Authority"]:
        res = "Affordable Housing"
    elif x in ["transitional housing", "temporary housing"]:
        res = "Temporary Housing"
    elif x in ["condemned property", "mixed-use space", "uninhabitable place", "rest areas"]:
        res = "Uninhabitable Space"
    elif x in ["hotel", "motel"]:
        res = "Hotel Or Motel"
    elif x in ["family/friends'", "couch surfing"]:
        res = "Community Members'"
    elif x in ["in a vehicle", "Alluvium", "tent"]:
        res = "Vehicle Or Tent"
    else:
        res = "Unclassified or Unspecified Location"
    return res

def reorganizeP7():
    df = aqh[(aqh.Preference=='P7') & (aqh.Answer=='Yes') & ~(aqh.Response.astype(str) == 'nan')]
    df.loc[:, 'P7SCat'] = df.copy()['Response'].apply(lambda x: categorize_p7_s(x))
    df.loc[:, 'P7BCat'] = df.copy()['P7SCat'].apply(lambda x: categorize_p7_b(x))
    return df

def categorize_p8_s(x):
    #print(x)
    wf = re.search("WILLAMETTE fAMILY|WF|wam fam|wamfam|fam", x, re.IGNORECASE)
    lh = re.search("Legacy Health", x, re.IGNORECASE)
    em = re.search("julie hansen|eugene mission", x, re.IGNORECASE)
    cm = re.search(getNames(df=who, detailed_name='Community Member'), x, re.IGNORECASE)
    family = re.search("mom|daughter|son|father|mother|sister|brother|family|niece|wife|parent|cousin|step child|spouse|daugheter|daighter|daugter|daugther|husband|uncle|aunt|legal guardian|Dad|Relative|adult", x, re.IGNORECASE)
    friend = re.search("girlfriend|friend|Frend|coworker|Roommate|neighbor", x, re.IGNORECASE)
    manager = re.search("Case Manager|Caser manager|cm|Case Mgr|case manger|NCM|Case Management|Case Managment|Case  Manager|casemanager|Case Mnager|DCM|mananager", x, re.IGNORECASE)
    hfg = re.search("HFG|Homes For Good|Home4Good|homes fro Good|Home for Good|flyer|541-682-2550|Resident Services|Cappy|Sarah Stanley|Kat |JJ|Dustin|Johanna|Pope|Waitlist connect|Duncan|Melissa Hartman|Maclain Barney|don|Email|Sarah Wilson"+'|'+getNames(df=who, detailed_name='Homes for Good Staff'), x, re.IGNORECASE)
    btsa = re.search("Black Thistle street aid|Bridgette", x, re.IGNORECASE)
    rn = re.search("Relief Nursery", x, re.IGNORECASE)
    csi = re.search("ColumbiaCare", x, re.IGNORECASE)
    ccs = re.search("Catholic community services"+'|'+getNames(df=who, detailed_name='Catholic Community Services Staff'), x, re.IGNORECASE)
    sc = re.search("ShelterCare|Ruby Renfro|SC Staff|Catrina|Amanda|Dana|Alison Pfaff"+'|'+getNames(df=who, detailed_name='Sheltercare Staff'), x, re.IGNORECASE)
    sce = re.search("Sunshine Care Environments", x, re.IGNORECASE)
    lcsw = re.search('LCSW|Social worker', x, re.IGNORECASE)
    lc = re.search("Lane COunty|Deborah L"+'|'+getNames(df=who, detailed_name='Lane County Staff Member'), x, re.IGNORECASE)
    step = re.search("STEP|Lindsay|Lindsey", x, re.IGNORECASE)
    cw = re.search("Case Worker|caseworker", x, re.IGNORECASE)
    cs = re.search("Community Share|Community Sharing", x, re.IGNORECASE)
    lcbh = re.search("LCBH|Lane County Behavioral Health", x, re.IGNORECASE)
    lcdp = re.search("Dovetail", x, re.IGNORECASE)
    cg = re.search("caregiver|Care Provider", x, re.IGNORECASE)
    cfnc =  re.search("Coast Fork Nursing Center", x, re.IGNORECASE)
    svdp = re.search("SVDP|St. Vincent de paul|Vikki Perpinan|Melissa Swick|Sarah Koski|Jeff Wolfe|Amber|Vikki|Aspiranti|Aspiranti|Aspirnanti|Ashely", x, re.IGNORECASE)
    oslp = re.search("Oregon Supported Living Program", x, re.IGNORECASE)
    lila = re.search("Independent Living|LILA", x, re.IGNORECASE)
    an = re.search("Advocates Northwest", x, re.IGNORECASE)
    wbc = re.search("White Bird|David|Whitebird", x, re.IGNORECASE)
    cht = re.search("Claire Hutton", x, re.IGNORECASE)
    ps = re.search("Peer Support|Peers support|Per support|PSS", x, re.IGNORECASE)
    lhc = re.search("Laurel Hill Center"+'|'+getNames(df=who, detailed_name='Laurel Hill Center Staff'), x, re.IGNORECASE)
    s = re.search("staff", x, re.IGNORECASE)
    hs = re.search("Housing Specialist|housing services|Housing Coordinator", x, re.IGNORECASE)
    a =  re.search("advocate", x, re.IGNORECASE)
    slmh = re.search("South Lane Mental Health", x, re.IGNORECASE)
    gsih = re.search("G Street Integrated Health", x, re.IGNORECASE)
    cch = re.search("Cornerstone Community Housing", x, re.IGNORECASE)
    cri = re.search("USCRI", x, re.IGNORECASE)
    hiva = re.search("HIV Alliance|Ali Sanchez"+'|'+getNames(df=who, detailed_name='HIV Alliance Staff '), x, re.IGNORECASE)
    ohop = re.search("OHOP", x, re.IGNORECASE)
    naacp = re.search("NAACP", x, re.IGNORECASE)
    hn = re.search("Navigator", x, re.IGNORECASE)
    css = re.search("CSS|Community Supported Shelters|Destinee Thompson", x, re.IGNORECASE)
    odhs = re.search("HS|ODHS|DHS"+'|'+getNames(df=who, detailed_name='ODHS Staff'), x, re.IGNORECASE)
    sllea = re.search("SLLEA"+'|'+getNames(df=who, detailed_name='Smart Living Learning and Earning with Autism Staff'), x, re.IGNORECASE)
    sds = re.search("Senior and Disabled Services"+'|'+getNames(df=who, detailed_name='Senior Disability Service Staff'), x, re.IGNORECASE)
    rcsa = re.search("Redwood Cove Senior Apartments|Del Norte Senior Center", x, re.IGNORECASE)
    epl = re.search("library", x, re.IGNORECASE)
    allc = re.search("Allies LLC", x, re.IGNORECASE)
    hsa = re.search("Hope for safety alliance", x, re.IGNORECASE)
    aer = re.search("Avanti ElderCare Resources", x, re.IGNORECASE)
    ch = re.search("Community Health", x, re.IGNORECASE)
    mhi = re.search("Mainstreamhousing Inc.|Heath Stark", x, re.IGNORECASE)
    ws = re.search("Worksource|work source|worksouce|Gretchen Stupke", x, re.IGNORECASE)
    si = re.search("Sponsors Inc|sPONSORS|megan|Meghan"+'|'+getNames(df=who, detailed_name='Sponsors Inc Staff'), x, re.IGNORECASE)
    cco = re.search("Louis Diaz Medina|Sonja Hyslip|Disaster Case Manager", x, re.IGNORECASE)
    rs = re.search("Rural Street|rural outreach", x, re.IGNORECASE)
    dc = re.search("Daisy CHAIN", x, re.IGNORECASE)
    sv = re.search("opportunity village", x, re.IGNORECASE)
    hhc = re.search("Helping Hands", x, re.IGNORECASE)
    clc = re.search(getNames(df=who, detailed_name='Connected Lane County Staff '), x, re.IGNORECASE)
    lcc = re.search(getNames(df=who, detailed_name='Lane Community College Staff '), x, re.IGNORECASE)
    sl = re.search(getNames(df=who, detailed_name='Serenity Lane Staff'), x, re.IGNORECASE)
    e = re.search(getNames(df=who, detailed_name='Emergence Staff'), x, re.IGNORECASE)
    pbc = re.search(getNames(df=who, detailed_name='Pearl Buck Center Staff'), x, re.IGNORECASE)
    o = re.search(getNames(df=who, detailed_name='Options Staff '), x, re.IGNORECASE)
    c = re.search("counselor", x, re.IGNORECASE)
    r = re.search("representative|Mckenzie Personnel Systems", x, re.IGNORECASE)
    pa = re.search("Personal Agent", x, re.IGNORECASE)
    cfd = re.search("Center for Family Development", x, re.IGNORECASE)
    ftc = re.search("Friends of the Children", x, re.IGNORECASE)
    ccc = re.search("ccc", x, re.IGNORECASE)
    cc = re.search("cc", x, re.IGNORECASE)
    
    if wf:
        res = 'Willamette Family'
    elif ftc:
        res = 'Friends of the Children'
    elif em:
        res = 'Eugene Mission'
    elif lh:
        res = 'Legacy Health'
    elif dc:
        res = 'Daisy C.H.A.I.N.'
    elif sv: 
        res = 'SquareOne Villages'
    elif hhc:
        res = 'Helping Hands Coalition'
    elif cco:
        res = 'Catholic Charities of Oregon'
    elif rs:
        res = 'Lane County Rural Street Outreach'
    elif ws:
        res = 'Worksource Oregon'
    elif si:
        res = 'Sponsors, Inc'
    elif mhi:
        res = 'Mainstream Housing, Inc'
    elif aer:
        res = 'Avanti ElderCare Resources'
    elif ch:
        res = 'Community Health'
    elif cht:
        res = 'Claire Hutton'
    elif hsa:
        res = 'Hope & Safety Alliance'
    elif allc:
        res = 'Allies, LLC'
    elif epl:
        res = 'Eugene Public Library'
    elif rn:
        res = 'Relief Nursery'
    elif hfg:
        res = 'Homes For Good'
    elif sce:
        res = 'Sunshine Care Environments'
    elif csi:
        res = 'ColumbiaCare Services'
    elif ccs:
        res = 'Catholic Community Services'
    elif sc:
        res = 'ShelterCare'
    elif lcsw:
        res = 'Licensed Clinical Social Worker'
    elif lc:
        res = 'Lane County'
    elif cw:
        res = 'case worker'
    elif lcbh:
        res = 'Lane County Behavioral Health'
    elif lcdp:
        res = 'Lane County Dovetail Program'
    elif cfnc:
        res = 'Coast Fork Nursing Center'
    elif svdp:
        res = 'St. Vincent de Paul'
    elif oslp:
        res = 'Oregon Supported Living Program'
    elif lila:
        res = 'Lane Independent Living Alliance'
    elif an:
        res = 'Advocates Northwest'
    elif wbc:
        res = 'White Bird Clinic'
    elif cs:
        res = 'Community Share'
    elif ch:
        res = 'Claire Hutton'
    elif ps:
        res = 'peer support specialist'
    elif lhc:
        res = 'Laurel Hill Center'
    elif slmh:
        res = 'South Lane Mental Health'
    elif gsih:
        res = 'G Street Integrated Health'
    elif s:
        res = 'support staff'
    elif hs:
        res = 'housing specialist'
    elif cch:
        res = 'Cornerstone Community Housing'
    elif cri:
        res = 'USCRI'
    elif hiva:
        res = 'HIV Alliance'
    elif ohop:
        res = 'Oregon Health Authority'
    elif naacp:
        res = 'NAACP'
    elif hn:
        res = 'Housing Navigator'
    elif css:
        res = 'Community Supported Shelters'
    elif btsa:
        res = 'Black Thistle Street Aid'
    elif rcsa:
        res = 'Redwood Cove Senior Apartments'
    elif odhs:
        res = 'ODHS'
    elif sllea:
        res = 'SLLEA'
    elif sds:
        res = 'Senior & Disability Services'   
    elif a:
        res = 'advocate'
    elif pa:
        res = 'personal agent'
    elif friend:
        res = 'friend'
    elif step:
        res = 'SNAP Training & Employment Program'
    elif manager:
        res = 'case manager'
    elif clc:
        res = 'Connected Lane County'   
    elif lcc:
        res = 'Lane Community College'
    elif sl:
        res = 'Serenity Lane'
    elif e:
        res = 'Emergence'
    elif pbc:
        res = 'Pearl Buck Center'
    elif o:
        res = 'Options'
    elif cm:
        res = 'community member'
    elif c:
        res = 'counselor'
    elif r:
        res = 'Mckenzie Personnel Systems'
    elif cfd:
        res = 'Center for Family Development'
    elif family:
        res = 'family'
    elif cg:
        res = 'caregiver'
    elif ccc:
        res = 'Campbell Community Center'
    elif cc:
        res = 'The Child Center'
    else:
        res = 'unknown'
    return res

def categorize_p8_b(x):
    if x in ['family', 'friend', 'community member']:
        res = 'Community Member'
    elif x in ['case manager', 'support staff', 'case worker', 'advocate', 'Licensed Clinical Social Worker','peer support specialist', 'personal agent', 'caregiver', 'Senior & Disability Services', 'The Child Center', 'Relief Nursery', 'Daisy C.H.A.I.N.', 'Easterseals Oregon', 'EasyCare Inc', 'Community Share', 'Allies, LLC', 'Connected Lane County', 'Lane Workforce Partnership', 'Lane Independent Living Alliance', 'SLLEA', 'Pearl Buck Center', 'Sponsors, Inc', 'Eugene Mission', 'Laurel Hill Center', 'Oregon Supported Living Program', 'Friends of the Children', 'Community Organized Relief Effort', 'Oregon Social Learning Center', 'Resource Connections of Oregon', 'Hope & Safety Alliance', 'HIV Alliance', 'Helping Hands Coalition', 'Meals on Wheels', 'Domestic Violence Clinic', 'Abilitree', 'Goodwill Job Connections', 'Campbell Community Center', 'Mckenzie Personnel Systems', 'Black Thistle Street Aid', 'USCRI', 'Advocates Northwest', 'Sunshine Care Environments', 'Avanti ElderCare Resources', 'NAACP']:
        res = 'Human Services'
    elif x in ['housing specialist', 'Housing Navigator', 'SquareOne Villages', 'Everyone Village', 'Sheltercare', 'Mainstream Housing, Inc', 'Cornerstone Community Housing', 'Green Leaf Village', 'Community Supported Shelters', 'Redwood Cove Senior Apartments']:
        res = 'Housing Services'
    elif x in ['counselor',  'Pacific Women’s Center', 'PeaceHealth', 'Oregon Medical Group', 'Looking Glass', 'Center for Family Development', 'Community Health', 'Springfield Treatment Center', 'Trillium', 'Willamette Family', 'White Bird Clinic', 'Facey Medical Group', 'G Street Integrated Health', 'Emergence', 'Coast Fork Nursing Center', 'Landmark Health', 'Orchid Health Fern Ridge Clinic', 'Options', 'Serenity Lane', 'ColumbiaCare Services', 'South Lane Mental Health', 'Legacy Health']:
        res = 'Health Services'
    elif x in ['SNAP Training & Employment Program', 'Temporary Assistance for Needy Families', 'Lane County Behavioral Health', 'Lane County Dovetail Program', 'Worksource Oregon', 'Lane County', 'ODHS', 'Employment Department', 'Women, Infants, and Children', 'Oregon Secretary of State', 'State of Oregon', 'Medicaid', 'Department of Labor', 'Oregon Health Authority', 'HOPWA', 'Developmental Disabilities Services', 'Lane County Rural Street Outreach', 'Washington County Housing Services', 'Oregon Secretary of State']:
        res = 'Government Services'
    elif x in ['Homes For Good', 'Housing Choice Voucher Program Section 8']:
        res = 'Homes For Good'
    elif x in ['unknown', 'Claire Hutton']:
        res = 'Unknown'
    else:
        res = 'Community Organization'
    return res

def reorganizeP8():
    df = aqh[(aqh.Preference=='P8') & (aqh.Answer=='Yes')]
    df.loc[df.Response=='Kat', 'Response'] = 'Kat '
    df.loc[:, 'P8SCat'] = df.copy()['Response'].apply(lambda x: categorize_p8_s(x))
    df.loc[:, 'P8BCat'] = df.copy()['P8SCat'].apply(lambda x: categorize_p8_b(x))
    return df

def categorize_p9_s(x):
    #print(x)
    wf = re.search("Willamette|WF|wallamete|wamfam|wam fam|willimatte", x, re.IGNORECASE)
    af = re.search('affordablehousing|Affordable Housing|affordablehomes', x, re.IGNORECASE)
    hfg = re.search("Homes for Good|HFG|ho n es for good|home for goods|Homegorgood|home goods|Homesforgood|Homes4Good|Don|Homes 4 good|Home4Good|Housing For Good|Village Oaks|good for homes|Housetogood|Good Homes|Your|Housing for Good|list|Houses For Good|Home for good|office|HGF|Sarah Wilson|Walk|Drive|Homes fo Good|h 4 g|h4g|BOB|JJ|Booth|rays food place|Homesfor good|Bridges on Broadway|Drove|came|lobby|Hones for good|541-682-2550|Resident Services|Cappy|Sarah Stanley|Kat |JJ|Dustin|Johanna|Pope|Waitlist connect|Duncan|Melissa Hartman|Maclain Barney|don|already|RSS|pop up|Homes for a good|home for goods|homes for goods|Resource center|lottery|Jacob fox|B O B"+'|'+getNames(df=who, detailed_name='Homes for Good Staff'), x, re.IGNORECASE)
    svdp = re.search("Vincent|SVDP|SVPD|Second chance|St.V|St V|sleep|Swick|Sarah Koski|Jeff|Amber|Vikki|Aspiranti|Aspirnanti|Ashely|st. |First place|1st place", x, re.IGNORECASE)
    fb = re.search("Facebook|Fb|F b|Favebook|Face book|Facebok|Faced book", x, re.IGNORECASE)
    hsp = re.search("manger|Mnager|Manaement|mangement|manageent|Manger|Mnagement|Manager|manger|Case Mgr|case worker|Social Services|Counselor|Oasis|Family Coach|Service Navigator|caseworker|CM|peer support|Nurse|Personal Agent|PA|Management|social service agency|Social worker|Advocate|COUNSELER|Peer Support|caregiver|Care Provider|Service Coordinator|Intake worker|support staff|advisor|PSS|adviser|Legal Aid|worker|social|case|advo|domestic violence support", x, re.IGNORECASE)
    lc = re.search("Lane county|lanecounty|County worker|Probation"+'|'+getNames(df=who, detailed_name='Lane County Staff Member'), x, re.IGNORECASE)                
    hsa = re.search("Hope and safety|Womenspace|woman’s space|Laura blackwell|Help and safety|Hope n safety|women space|Women's space", x, re.IGNORECASE)
    css = re.search("CSS|Community Supported|Destinee Thompson", x, re.IGNORECASE)
    hs = re.search("Housing Specialist|housing services|Housing Coordinator|Housing cordinator|housing authority|Housing advocate|Housing advo|resident services coordinator|navigator|Housing help|Housings authorities|AHO|My housing|housing agency|housing source|Gary Robert|Cynthia Sharp|Beth Johnson|Housing stailbization", x, re.IGNORECASE)
    odhs = re.search("HS|ODHS|DHS|Human Resources|Human Resorces|welfare|voc|D.h.s|D.h s", x, re.IGNORECASE)
    ftc = re.search("Friends of", x, re.IGNORECASE)
    ccs = re.search("CCS|Catholic comm|Cathlico community|food bank|Community Service|Foodbox|Food box", x, re.IGNORECASE)
    lhc = re.search("Laurel", x, re.IGNORECASE)
    ff= re.search("mom|daughter|son|father|Mother|sister|brother|family|niece|wife|parent|cousin|step child|spouse|daugheter|daighter|daugter|daugther|husband|uncle|aunt|legal guardian|Dad|Relative|adult|friend|Familial|Causin|girlfriend|Frend|Roommate|neighbor|fmaily|Freind|friemd|Firend|gma|grandma|duaghter|room mate|froiend|Firend|Sibling|barkhimer|kids|aquaintence|aquaintance|Acquaintance|fiend|Famoly|familiy|fiend", x, re.IGNORECASE)
    ew = re.search("Weekly", x, re.IGNORECASE)
    sc = re.search("ShelterCare|Ruby Renfro|SC Staff|Catrina|Amanda|Dana|Alison Pfaff|Shelter care", x, re.IGNORECASE)
    cc = re.search("Child Center", x, re.IGNORECASE)
    wbc = re.search("White Bird|David|Whitebird", x, re.IGNORECASE)
    headst = re.search("Head Start|Headstart", x, re.IGNORECASE)
    lcog = re.search("Senior & Disability Services|Senior and Disable|Senior Disable|Senior and Disability|Senior and disabilities|Senior or Disabled Service|Senior Services|Senior & Disabiliy|sds|S&D|Senior & Disabled|Senior Citizens Disability|Gienia", x, re.IGNORECASE)
    cfnc = re.search("Coast Fork Nursing Center", x, re.IGNORECASE)
    rg = re.search("register guard|RegisterGuard|RG", x, re.IGNORECASE)
    tri = re.search("Trillium|Chelsea|insurance", x, re.IGNORECASE)
    s8 = re.search("Section 8|baimbridge|Balmbridge|s8|Voucher|section8|Sec 8", x, re.IGNORECASE)
    stc = re.search("treatment", x, re.IGNORECASE)
    cfd = re.search("Center for family development|Cfd", x, re.IGNORECASE)
    gg = re.search("Google|search|inquiry|curious|check|look", x, re.IGNORECASE)
    lib = re.search("library", x, re.IGNORECASE)
    lila = re.search("Independent Living|LILA", x, re.IGNORECASE)
    lcdp = re.search("Dovetail", x, re.IGNORECASE)
    omg = re.search("OMG|Oregon Medical Group", x, re.IGNORECASE)
    seta = re.search("Springfield Eugene Tenant Association|SETA", x, re.IGNORECASE)
    clc = re.search('Olivia Goodheart|See above'+'|'+getNames(df=who, detailed_name='Connected Lane County Staff '), x, re.IGNORECASE)
    rn = re.search("Relief Nursery", x, re.IGNORECASE)
    sm = re.search("SM|Social media", x, re.IGNORECASE)
    si = re.search("Sponsor|megan|Meghan|Spnors|Spobnsor's|sponsers|Sponosors|Sponsons"+'|'+getNames(df=who, detailed_name='Sponsors Inc Staff'), x, re.IGNORECASE)
    ws = re.search("Worksource|work source|worksouce|Gretchen Stupke", x, re.IGNORECASE)
    cco = re.search("Catholic Charities|Catholic  Charities|cco", x, re.IGNORECASE)
    sllea = re.search("SLLEA"+'|'+getNames(df=who, detailed_name='Smart Living Learning and Earning with Autism Staff'), x, re.IGNORECASE)
    lg = re.search("looking glass", x, re.IGNORECASE)
    nmh = re.search("Northwest Medical Home", x, re.IGNORECASE)
    lcbh = re.search("LCBH|Lane County Behavioral Health", x, re.IGNORECASE)
    em = re.search("julie hansen|mission", x, re.IGNORECASE) 
    mhi = re.search("Mainstreamhousing Inc.|Heath Stark", x, re.IGNORECASE)
    step = re.search("STEP|Lindsay|Lindsey", x, re.IGNORECASE)
    e = re.search('Emergence'+'|'+getNames(df=who, detailed_name='Emergence Staff'), x, re.IGNORECASE)
    th = re.search("transitional housing", x, re.IGNORECASE)
    tanf = re.search("TANF|Kalli Ramsey", x, re.IGNORECASE)
    h = re.search("Shelter|Homeless Center", x, re.IGNORECASE)
    dds = re.search("Developmental Disability Services|DDS|Development Disabled Services|Developmental Disabled Services|Developmental Disability Services", x, re.IGNORECASE)
    cs = re.search("Community Share|Community Sharing", x, re.IGNORECASE)
    reddit = re.search("REDDIT", x, re.IGNORECASE)
    lh = re.search("Landmark Health", x, re.IGNORECASE)
    email = re.search("mail|newsletter|link|emai|eamil|Enail|Emial|enail|Emqil|Eamil|Emaol", x, re.IGNORECASE)
    flyer = re.search("flyer|Fkyer|flier", x, re.IGNORECASE)
    text = re.search("text|message|rext|Massage", x, re.IGNORECASE)
    web = re.search("web|internet|intenter|computer|intetnet|211|site|line|self|keep", x, re.IGNORECASE)
    wfp = re.search("workforce|work force", x, re.IGNORECASE)
    eo = re.search("Employment", x, re.IGNORECASE)
    gf = re.search("Green Leaf", x, re.IGNORECASE)
    ap = re.search("applied|Previous|always|familiar", x, re.IGNORECASE)
    news = re.search("News", x, re.IGNORECASE)
    call = re.search("call|phone|541|hotline", x, re.IGNORECASE)
    wic = re.search("wic", x, re.IGNORECASE)
    facey = re.search("Facey", x, re.IGNORECASE)
    oslp = re.search("Oregon Supported Living Program|oslp", x, re.IGNORECASE)
    hud = re.search("hud office|HUD", x, re.IGNORECASE)
    allc = re.search("Allies", x, re.IGNORECASE)
    sos = re.search("sos", x, re.IGNORECASE)
    gsih = re.search("G street", x, re.IGNORECASE)
    ch = re.search("Community Health", x, re.IGNORECASE)
    rs = re.search("outreach|Ali Sanchez|out reach", x, re.IGNORECASE)
    o = re.search("options"+'|'+getNames(df=who, detailed_name='Options Staff '), x, re.IGNORECASE)
    pbc = re.search("pearl"+'|'+getNames(df=who, detailed_name='Pearl Buck Center Staff'), x, re.IGNORECASE)
    ev = re.search("everyone", x, re.IGNORECASE)
    mow = re.search("Meals on Wheels", x, re.IGNORECASE)
    state = re.search("Oregon State|State of Oregon", x, re.IGNORECASE)
    po = re.search("notice", x, re.IGNORECASE)
    slmh = re.search("slmh|Mental Health", x, re.IGNORECASE)
    sv = re.search("Square one|Opportunity|OPPERTUNITY", x, re.IGNORECASE)
    core = re.search("core", x, re.IGNORECASE)
    dc = re.search("Daisy", x, re.IGNORECASE)
    oslc = re.search("fair", x, re.IGNORECASE)
    abi = re.search("Abilitree", x, re.IGNORECASE)
    mc = re.search("councilor|my Dr.|doctor|mental health provider|Medical Provider|Counseling|Councelor|mentor|Hospital|therapist|therapy|Jose Maria santana|councilor|Amelia Jans|clinic|Mental heath|VA", x, re.IGNORECASE)
    wsc = re.search("Women’s Center", x, re.IGNORECASE)
    ph = re.search("Peace", x, re.IGNORECASE)
    hhc = re.search("Helping Hands", x, re.IGNORECASE)
    medic = re.search("Medicaid", x, re.IGNORECASE)
    corn = re.search("Cornerstone", x, re.IGNORECASE)
    wioa = re.search("WIOA", x, re.IGNORECASE)
    bb = re.search("sign|vehicle", x, re.IGNORECASE)
    hiva = re.search("HIV|Ali Sanchez"+'|'+getNames(df=who, detailed_name='HIV Alliance Staff '), x, re.IGNORECASE)
    ohop = re.search("OHOP", x, re.IGNORECASE)
    cla = re.search("Centro|cla", x, re.IGNORECASE)
    easy = re.search("easy|ez cares", x, re.IGNORECASE)
    uo = re.search("Domestic violence clinic", x, re.IGNORECASE)
    es = re.search("Easter", x, re.IGNORECASE)
    oh = re.search("Orchid Health", x, re.IGNORECASE)
    ins = re.search("Instagram|ins", x, re.IGNORECASE)
    rco = re.search("Resource Connection|rco", x, re.IGNORECASE)
    hopwa = re.search("hopwa", x, re.IGNORECASE)
    gjc = re.search("Goodwill", x, re.IGNORECASE)
    lcc = re.search("l.c.c|lcc|community college|cox|Schaun", x, re.IGNORECASE)
    cm = re.search("Deborah|Kairos|All|Employee|chandler|Another applicant|Tentant|Community|Current|employer|boss|apt mgr|Coworker|Co-worker|Co worker|vecino|landlord|coworker|Community members|tenant|Michele|Kiros|Tammi|Tami|word o|mouth|WOM|work|talk|Sarah Owen|assistance|Mike"+'|'+getNames(df=who, detailed_name='Community Member'), x, re.IGNORECASE)
    co = re.search("the guest house|love|child school|Electrónico|church|Many places|other|agency|MAT program|Resident Meeting|grapevice", x, re.IGNORECASE)
    
    if wf:
        res = 'Willamette Family'
    elif af:
        res = 'Affordable Housing'
    elif medic:
        res = 'Medicaid'
    elif wioa:
        res = 'Department of Labor'
    elif wsc:
        res = 'Pacific Women’s Center'
    elif ph:
        res = 'PeaceHealth'
    elif gjc:
        res = 'Goodwill Job Connections'
    elif abi:
        res = 'Abilitree'
    elif corn:
        res = 'Cornerstone Community Housing'
    elif svdp:
        res = 'St. Vincent de Paul'
    elif po:
        res = 'Public Notice Oregon'
    elif sos:
        res = 'Oregon Secretary of State'
    elif hud:
        res = 'Washington County Housing Services'
    elif fb:
        res = 'Facebook'
    elif bb:
        res = 'billboard'
    elif sm:
        res = 'social media'
    elif hsp:
        res = 'human services'
    elif uo:
        res = 'Domestic Violence Clinic'
    elif sv: 
        res = 'SquareOne Villages'
    elif lc:
        res = 'Lane County'
    elif ev:
        res = 'Everyone Village'
    elif mow:
        res = 'Meals on Wheels'
    elif ap:
        res = 'former applicant'  
    elif hhc:
        res = 'Helping Hands Coalition'
    elif state:
        res = 'State of Oregon'
    elif dc:
        res = 'Daisy C.H.A.I.N.'
    elif hiva:
        res = 'HIV Alliance'
    elif hsa:
        res = 'Hope & Safety Alliance'
    elif slmh:
        res = 'South Lane Mental Health'
    elif gsih:
        res = 'G Street Integrated Health'
    elif rco:
        res = 'Resource Connections of Oregon'
    elif oslc:
        res = 'Oregon Social Learning Center'
    elif oh:
        res = 'Orchid Health Fern Ridge Clinic'
    elif core:
        res = 'Community Organized Relief Effort'
    elif css:
        res = 'Community Supported Shelters'
    elif hs:
        res = 'housing specialist'
    elif hopwa:
        res = 'HOPWA'
    elif dds:
        res = 'Developmental Disabilities Services'
    elif odhs:
        res = 'ODHS'
    elif ftc:
        res = 'Friends of the Children'
    elif o:
        res = 'Options'
    elif ccs:
        res = 'Catholic Community Services'
    elif oslp:
        res = 'Oregon Supported Living Program'    
    elif lhc:
        res = 'Laurel Hill Center'
    elif cco:
        res = 'Catholic Charities of Oregon'
    elif em:
        res = 'Eugene Mission'
    elif lh:
        res = 'Landmark Health'
    elif ew:
        res = 'Eugene Weekly'
    elif si:
        res = 'Sponsors, Inc'
    elif pbc:
        res = 'Pearl Buck Center'
    elif ch:
        res = 'Community Health'
    elif lib:
        res = 'Eugene Public Library'
    elif rn:
        res = 'Relief Nursery'
    elif sc:
        res = 'ShelterCare'
    elif facey:
        res = 'Facey Medical Group'
    elif ohop:
        res = 'Oregon Health Authority'
    elif wbc:
        res = 'White Bird Clinic'
    elif headst:
        res = 'Head Start'
    elif lcog:
        res = 'Senior & Disability Services'
    elif rs:
        res = 'Lane County Rural Street Outreach'
    elif cfnc:
        res = 'Coast Fork Nursing Center'
    elif rg: 
        res = 'Register-Guard'
    elif tri:
        res = 'Trillium'
    elif s8:
        res = 'Housing Choice Voucher Program Section 8'
    elif ws:
        res = 'Worksource Oregon'
    elif wfp:
        res = 'Lane Workforce Partnership'
    elif mhi:
        res = 'Mainstream Housing, Inc'
    elif stc:
        res = 'Springfield Treatment Center'
    elif cfd:
        res = 'Center for Family Development'
    elif lila:
        res = 'Lane Independent Living Alliance'
    elif lcdp:
        res = 'Lane County Dovetail Program'
    elif omg:
        res = 'Oregon Medical Group'
    elif seta:
        res = 'Springfield Eugene Tenant Association'
    elif clc:
        res = 'Connected Lane County' 
    elif allc:
        res = 'Allies, LLC'
    elif sllea:
        res = 'SLLEA'
    elif lg:
        res = 'Looking Glass'
    elif lcbh:
        res = 'Lane County Behavioral Health'
    elif step:
        res = 'SNAP Training & Employment Program'
    elif e:
        res = 'Emergence'
    elif gf:
        res = 'Green Leaf Village'
    elif th:
        res = 'transitional housing'
    elif tanf:
        res = 'Temporary Assistance for Needy Families'
    elif h:
        res = 'homeless center or shelter'
    elif cs:
        res = 'Community Share'
    elif eo:
        res = 'Employment Department'
    elif hfg:
        res = 'Homes For Good'
    elif cla:
        res = 'Centro Latino Americano'
    elif easy:
        res = 'EasyCare Inc'
    elif es:
        res = 'Easterseals Oregon'
    elif lcc:
        res = 'Lane Community College'
    elif reddit:
        res = 'Reddit'
    elif ins:
        res = 'Instagram'
    elif news:
        res = 'news'
    elif cc:
        res = 'The Child Center'
    elif wic:
        res = 'Women, Infants, and Children'
    elif mc:
        res = 'medical provider or therapist'
    elif email:
        res = 'Email'
    elif call:
        res = 'Phone call'
    elif gg:
        res = 'Google'
    elif web:
        res = 'website'
    elif flyer:
        res = 'flyer'
    elif text:
        res = 'text message'
    elif cm:
        res = 'community member'
    elif ff:
        res = 'family and friends'
    elif co:
        res = 'community organization'
    else:
        res = 'unknown'
    return res

def categorize_p9_b(x):
    if x in ['family and friends', 'text message', 'Email', 'community member']:
        res = 'Community Member'
    elif x in ['human services', 'Senior & Disability Services', 'The Child Center', 'Relief Nursery', 'Daisy C.H.A.I.N.', 'Easterseals Oregon', 'EasyCare Inc', 'Community Share', 'Allies, LLC', 'Connected Lane County', 'Lane Workforce Partnership', 'Lane Independent Living Alliance', 'SLLEA', 'Pearl Buck Center', 'Sponsors, Inc', 'Eugene Mission', 'Laurel Hill Center', 'Oregon Supported Living Program', 'Friends of the Children', 'Community Organized Relief Effort', 'Oregon Social Learning Center', 'Resource Connections of Oregon', 'Hope & Safety Alliance', 'HIV Alliance', 'Helping Hands Coalition', 'Meals on Wheels', 'Domestic Violence Clinic', 'Abilitree', 'Goodwill Job Connections']:
        res = 'Human Services'
    elif x in ['housing specialist', 'Affordable Housing', 'SquareOne Villages', 'Everyone Village', 'Sheltercare', 'Mainstream Housing, Inc', 'Cornerstone Community Housing', 'transitional housing', 'Green Leaf Village', 'Community Supported Shelters']:
        res = 'Housing Services'
    elif x in ['medical provider or therapist', 'Pacific Women’s Center', 'PeaceHealth', 'Oregon Medical Group', 'Looking Glass', 'Center for Family Development', 'Community Health', 'Springfield Treatment Center', 'Trillium', 'Willamette Family', 'White Bird Clinic', 'Facey Medical Group', 'G Street Integrated Health', 'Emergence', 'Coast Fork Nursing Center', 'Landmark Health', 'Orchid Health Fern Ridge Clinic', 'Options', 'South Lane Mental Health']:
        res = 'Health Services'
    elif x in ['social media', 'Google', 'Reddit', 'Eugene Weekly', 'Register-Guard', 'news', 'website', 'billboard', 'Instagram', 'Public Notice Oregon', 'Facebook']:
        res = 'Media Communications'
    elif x in ['SNAP Training & Employment Program', 'Temporary Assistance for Needy Families', 'Lane County Behavioral Health', 'Lane County Dovetail Program', 'Worksource Oregon', 'Lane County', 'ODHS', 'Employment Department', 'Women, Infants, and Children', 'Oregon Secretary of State', 'State of Oregon', 'Medicaid', 'Department of Labor', 'Oregon Health Authority', 'HOPWA', 'Developmental Disabilities Services', 'Lane County Rural Street Outreach', 'Washington County Housing Services', 'Oregon Secretary of State']:
        res = 'Government Services'
    elif x in ['Homes For Good', 'Housing Choice Voucher Program Section 8', 'flyer', 'Phone call', 'former applicant']:
        res = 'Homes For Good'
    elif x == 'unknown':
        res = 'Unknown'
    else:
        res = 'Community Organization'
    return res

def categorize_p9_c(x):
    email = re.search("mail|newsletter|link|emai|eamil|Enail|Emial|enail|Emqil|Eamil|sent", x, re.IGNORECASE)
    sm = re.search('Facebook|Fb|F b|Favebook|Face book|Facebok|SM|Social media|REDDIT|Instagram|Faced book', x, re.IGNORECASE)
    flyer = re.search("flyer|Fkyer|flier", x, re.IGNORECASE)
    text = re.search("text|message|rext|Massage", x, re.IGNORECASE)
    news = re.search("Eugene Weekly|register guard|RegisterGuard|RG|News|notice", x, re.IGNORECASE)
    se = re.search('Google|search|check|internet|intenter|computer|intetnet|in line|online|on line', x, re.IGNORECASE)
    web = re.search("web|affordablehousing|Affordable Housing|affordablehomes|.com|.org|211|site", x, re.IGNORECASE)
    call = re.search("call|phone|541", x, re.IGNORECASE)
    ov = re.search("office|drive|came|walk|booth|pop up|drove|went|rays food place|lobby", x, re.IGNORECASE)
    wom = re.search("word of|mouth|talk|heard|ask|meet|visit|said|told|tell", x, re.IGNORECASE)
    
    if email:
        res = 'Email'
    elif sm:
        res = 'Social Media'
    elif flyer:
        res = 'Flyer'
    elif text:
        res = 'Text Message'
    elif call:
        res = 'Phone Call'
    elif news:
        res = 'News'
    elif se:
        res = 'Search Engine'
    elif web:
        res = 'Website'
    elif ov:
        res = 'Office Visit'
    elif wom:
        res = 'Word of Mouth'
    else:
        res = 'Multiple Channels'
    return res

def reorganizeP9():
    df = aqh[(aqh.Preference=='P9') & ~(aqh.Response.astype(str) == 'nan')]
    df.loc[:, 'P9SCat'] = df.copy()['Response'].apply(lambda x: categorize_p9_s(x))
    df.loc[:, 'P9BCat'] = df.copy()['P9SCat'].apply(lambda x: categorize_p9_b(x))
    df.loc[:, 'P9Cat'] = df.copy()['Response'].apply(lambda x: categorize_p9_c(x))
    return df