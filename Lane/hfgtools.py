import pandas as pd
import os, re
from datetime import datetime, date

pd.options.mode.chained_assignment = None

inpath = r'T:\DCProjects\Support\Lane\HfG\DataFromThem'
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


def calculate_age(dob):
    born = datetime.strptime(dob, '%Y-%m-%d')
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def getNames(df, detailed_name):
    names = list(df.loc[df['Detailed Name']==detailed_name, 'name'].unique())
    return '|'.join(names)

def categorize_p8_s(x):
    #print(x)
    wf = re.search("WILLAMETTE fAMILY|WF|wam fam|wamfam|fam", x, re.IGNORECASE)
    lh = re.search("Legacy Health", x, re.IGNORECASE)
    em = re.search("julie hansen|eugene mission", x, re.IGNORECASE)
    cm = re.search(getNames(df=who, detailed_name='Community Member'), x, re.IGNORECASE)
    family = re.search("mom|daughter|son|father|mother|sister|brother|family|niece|wife|parent|cousin|step child|spouse|daugheter|daighter|daugter|husband|uncle|aunt|legal guardian|Dad|Relative|adult", x, re.IGNORECASE)
    friend = re.search("girlfriend|friend|Frend|coworker|Roommate|neighbor", x, re.IGNORECASE)
    manager = re.search("Case Manager|Caser manager|cm|Case Mgr|case manger|NCM|Case Management|Case Managment|Case  Manager|casemanager|Case Mnager|DCM|mananager", x, re.IGNORECASE)
    hfg = re.search("HFG|Homes For Good|Home4Good|homes fro Good|Home for Good|flyer|541-682-2550|Resident Services|Cappy|Sarah Stanley|Kat |JJ|Dustin|Johanna|Pope|Waitlist connect|Duncan|Melissa Hartman|Maclain Barney|don|Email"+'|'+getNames(df=who, detailed_name='Homes for Good Staff'), x, re.IGNORECASE)
    btsa = re.search("Black Thistle street aid|Bridgette", x, re.IGNORECASE)
    rn = re.search("Relief Nursery", x, re.IGNORECASE)
    csi = re.search("ColumbiaCare", x, re.IGNORECASE)
    ccs = re.search("Catholic community services"+'|'+getNames(df=who, detailed_name='Catholic Community Services Staff'), x, re.IGNORECASE)
    sc = re.search("ShelterCare|Ruby Renfro|SC Staff|Catrina|Amanda|Dana|Alison Pfaff"+'|'+getNames(df=who, detailed_name='Sheltercare Staff'), x, re.IGNORECASE)
    sce = re.search("Sunshine Care Environments", x, re.IGNORECASE)
    lcsw = re.search('LCSW|Social worker', x, re.IGNORECASE)
    lc = re.search("Lane COunty|Deborah L"+'|'+getNames(df=who, detailed_name='Lane County Staff Member'), x, re.IGNORECASE)
    step = re.search("STEP|Lindsay", x, re.IGNORECASE)
    cw = re.search("Case Worker|caseworker", x, re.IGNORECASE)
    cs = re.search("Community Share|Community Sharing", x, re.IGNORECASE)
    lcbh = re.search("LCBH|Lane County Behavioral Health", x, re.IGNORECASE)
    lcdp = re.search("Dovetail", x, re.IGNORECASE)
    cg = re.search("caregiver|Care Provider", x, re.IGNORECASE)
    cfnc =  re.search("Coast Fork Nursing Center", x, re.IGNORECASE)
    svdp = re.search("SVDP|St. Vincent de paul|Vikki Perpinan|Melissa Swick|Sarah Koski|Jeff Wolfe|Amber Fitch|Vikki  Perpinan|Vikki M Perpinan|VikkiPerpinan|Trisha Aspiranti|Trish Aspiranti|Trisha Aspiranti|Trisha Aspirnanti|Ashely", x, re.IGNORECASE)
    oslp = re.search("Oregon Supported Living Program", x, re.IGNORECASE)
    lila = re.search("Independent Living|LILA", x, re.IGNORECASE)
    an = re.search("Advocates Northwest", x, re.IGNORECASE)
    wbc = re.search("White Bird|David Joseph|Whitebird", x, re.IGNORECASE)
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
    cc = re.search("cc", x, re.IGNORECASE)
    
    if wf:
        res = 'Willamette Family'
    elif ftc:
        res = 'Friends of the Children'
    elif em:
        res = 'Eugene Mission'
    elif cc:
        res = 'The Child Center'
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
        res = 'Lane County Rural Street Outreach team'
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
        res = 'Allies LLC'
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
        res = 'Senior Disability Service'   
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
        res = 'casegiver'
    else:
        res = 'unknown'
    return res

def categorize_p8_b(x):
    if x in ['family', 'friend', 'community member']:
        res = 'Community Member'
    elif x in ['case manager', 'support staff', 'case worker', 'advocate', 'Licensed Clinical Social Worker', 'counselor', 'peer support specialist', 'personal agent']:
        res = 'Human Services Profession'
    elif x in ['housing specialist', 'Housing Navigator']:
        res = 'Housing Specialist'
    elif x in ['Claire Hutton', 'unknown']:
        res = 'Unknown'
    elif x == 'Homes For Good':
        res = 'Homes For Good'
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
    wf = re.search("Willamette|WF|wallamete|wamfam|wam fam|willimatte", x, re.IGNORECASE)
    af = re.search('affordablehousing|Affordable Housing', x, re.IGNORECASE)
    hfg = re.search("Homes for Good|HFG|ho n es for good|home for goods|Homegorgood|home goods|Homesforgood|Homes4Good|Don|Homes 4 good|Home4Good|Housing For Good|Village Oaks|good for homes|Housetogood|Good Homes|Your|Housing for Good|list|Houses For Good", x, re.IGNORECASE)
    svdp = re.search("St. Vincent|SVDP|St Vincent|Trisha Aspiranti", x, re.IGNORECASE)
    fb = re.search("Facebook|Fb|F b|Favebook", x, re.IGNORECASE)
    hsp = re.search("Manager|Case Mgr|case worker|Social Services|Counselor|Oasis|Family Coach|Service Navigator|caseworker|CM|peer support|Nurse|Personal Agent|PA|Management|therapy|Jose Maria santana|social service agency|Social worker|Advocate|COUNSELER|Peer Support", x, re.IGNORECASE)
    lc = re.search("Lane county|lanecounty", x, re.IGNORECASE)                
    ws = re.search("Hope and safety|Womenspace|woman’s space|Laura blackwell", x, re.IGNORECASE)                
    css = re.search("CSS|Community Supported Shelters|Destinee Thompson", x, re.IGNORECASE)
    hs = re.search("Housing Specialist|housing services|Housing Coordinator|housing authority|Housing advocate|Housing advo|resident services coordinator", x, re.IGNORECASE)
    odhs = re.search("HS|ODHS|DHS", x, re.IGNORECASE)
    ftc = re.search("Friends of", x, re.IGNORECASE)
    ccs = re.search("CCS|Catholic community services", x, re.IGNORECASE)
    lhc = re.search("Laurel Hill Center", x, re.IGNORECASE)
    ff= re.search("mom|daughter|son|father|mother|sister|brother|family|niece|wife|parent|cousin|step child|spouse|daugheter|daighter|daugter|husband|uncle|aunt|legal guardian|Dad|Relative|adult|friend|Familial|word of mouth|Causin|Community members|girlfriend|Frend|coworker|Roommate|neighbor|Coworker|fmaily|Co-worker|Co worker|vecino", x, re.IGNORECASE)
    ew = re.search("Eugene Weekly", x, re.IGNORECASE)
    sc = re.search("ShelterCare|Ruby Renfro|SC Staff|Catrina|Amanda|Dana|Alison Pfaff|Shelter care", x, re.IGNORECASE)
    cc = re.search("The Child Center", x, re.IGNORECASE)
    wbc = re.search("White Bird|Whitebird", x, re.IGNORECASE)
    headst = re.search("Head Start|Headstart", x, re.IGNORECASE)
    lcog = re.search("Senior & Disability Services|Senior and Disable|Senior Disable|Senior and Disability", x, re.IGNORECASE)
    cfnc = re.search("Coast Fork Nursing Center", x, re.IGNORECASE)
    rg = re.search("register guard|RegisterGuard|RG", x, re.IGNORECASE)
    tri = re.search("Trillium|Chelsea", x, re.IGNORECASE)
    s8 = re.search("Section 8", x, re.IGNORECASE)
    stc = re.search("springfield treatment center", x, re.IGNORECASE)
    cfd = re.search("Center for family development|Cfd", x, re.IGNORECASE)
    gg = re.search("Google", x, re.IGNORECASE)
    lib = re.search("library", x, re.IGNORECASE)
    hs = re.search("Housing Specialist|housing services|Housing Coordinator|housing", x, re.IGNORECASE)
    lila = re.search("Independent Living|LILA", x, re.IGNORECASE)
    lcdp = re.search("Dovetail", x, re.IGNORECASE)
    omg = re.search("OMG|Oregon Medical Group", x, re.IGNORECASE)
    seta = re.search("Springfield Eugene Tenant Association", x, re.IGNORECASE)
    clc = re.search('Olivia Goodheart'+'|'+getNames(df=who, detailed_name='Connected Lane County Staff '), x, re.IGNORECASE)
    rn = re.search("Relief Nursery", x, re.IGNORECASE)
    sm = re.search("SM|Social media", x, re.IGNORECASE)
    si = re.search("Sponsors|sPONSORS|megan|Meghan"+'|'+getNames(df=who, detailed_name='Sponsors Inc Staff'), x, re.IGNORECASE)
    ws = re.search("Worksource|work source|worksouce|Gretchen Stupke", x, re.IGNORECASE)
    ccus = re.search("Catholic Charities|Catholic  Charities", x, re.IGNORECASE)
    sllea = re.search("SLLEA"+'|'+getNames(df=who, detailed_name='Smart Living Learning and Earning with Autism Staff'), x, re.IGNORECASE)
    lg = re.search("looking glass", x, re.IGNORECASE)
    nmh = re.search("Northwest Medical Home", x, re.IGNORECASE)
    lcbh = re.search("LCBH|Lane County Behavioral Health", x, re.IGNORECASE)
    em = re.search("julie hansen|mission", x, re.IGNORECASE) 
    mhi = re.search("Mainstreamhousing Inc.|Heath Stark", x, re.IGNORECASE)
    step = re.search("STEP|Lindsay", x, re.IGNORECASE)
    e = re.search('Emergence'+'|'+getNames(df=who, detailed_name='Emergence Staff'), x, re.IGNORECASE)
    th = re.search("transitional housing", x, re.IGNORECASE)
    tanf = re.search("TANF|Kalli Ramsey", x, re.IGNORECASE)
    cg = re.search("caregiver|Care Provider", x, re.IGNORECASE)
    H = re.search("Shelter|Homeless Center", x, re.IGNORECASE)
    dds = re.search("Developmental Disability Services", x, re.IGNORECASE)
    cs = re.search("Community Share|Community Sharing", x, re.IGNORECASE)
    reddit = re.search("REDDIT", x, re.IGNORECASE)
    lh = re.search("Landmark Health", x, re.IGNORECASE)
    
    
    
    lh = re.search("Legacy Health", x, re.IGNORECASE)
    em = re.search("julie hansen|eugene mission", x, re.IGNORECASE)
    cm = re.search(getNames(df=who, detailed_name='Community Member'), x, re.IGNORECASE)
    family = re.search("mom|daughter|son|father|mother|sister|brother|family|niece|wife|parent|cousin|step child|spouse|daugheter|daighter|daugter|husband|uncle|aunt|legal guardian|Dad|Relative|adult", x, re.IGNORECASE)
    friend = re.search("girlfriend|friend|Frend|coworker|Roommate|neighbor", x, re.IGNORECASE)
    
    
    btsa = re.search("Black Thistle street aid|Bridgette", x, re.IGNORECASE)
    
    csi = re.search("ColumbiaCare", x, re.IGNORECASE)
    
    sc = re.search("ShelterCare|Ruby Renfro|SC Staff|Catrina|Amanda|Dana|Alison Pfaff"+'|'+getNames(df=who, detailed_name='Sheltercare Staff'), x, re.IGNORECASE)
    sce = re.search("Sunshine Care Environments", x, re.IGNORECASE)
    lcsw = re.search('LCSW|Social worker', x, re.IGNORECASE)
    lc = re.search("Lane COunty|Deborah L"+'|'+getNames(df=who, detailed_name='Lane County Staff Member'), x, re.IGNORECASE)
    step = re.search("STEP|Gretchen Stupke|Lindsay|Gretchen Stupke", x, re.IGNORECASE)
    cw = re.search("Case Worker|caseworker", x, re.IGNORECASE)
    
    lcbh = re.search("LCBH|Lane County Behavioral Health", x, re.IGNORECASE)
    
    
    cfnc =  re.search("Coast Fork Nursing Center", x, re.IGNORECASE)
    
    oslp = re.search("Oregon Supported Living Program", x, re.IGNORECASE)
    
    an = re.search("Advocates Northwest", x, re.IGNORECASE)
    
    cht = re.search("Claire Hutton", x, re.IGNORECASE)
    ps = re.search("Peer Support|Peers support|Per support|PSS", x, re.IGNORECASE)
    
    s = re.search("staff", x, re.IGNORECASE)
    
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
    
    sds = re.search("Senior and Disabled Services"+'|'+getNames(df=who, detailed_name='Senior Disability Service Staff'), x, re.IGNORECASE)
    rcsa = re.search("Redwood Cove Senior Apartments|Del Norte Senior Center", x, re.IGNORECASE)
    epl = re.search("library", x, re.IGNORECASE)
    allc = re.search("Allies LLC", x, re.IGNORECASE)
    hsa = re.search("Hope for safety alliance", x, re.IGNORECASE)
    aer = re.search("Avanti ElderCare Resources", x, re.IGNORECASE)
    ch = re.search("Community Health", x, re.IGNORECASE)
    
    
    
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
    
    ftc = re.search("Friends of the Children", x, re.IGNORECASE)
    
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
        res = 'Lane County Rural Street Outreach team'
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
        res = 'Allies LLC'
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
        res = 'Senior Disability Service'   
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
        res = 'casegiver'
    else:
        res = 'unknown'
    return res

