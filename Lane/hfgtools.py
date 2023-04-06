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
        res = 'Community Members'
    elif x in ['case manager', 'support staff', 'case worker', 'advocate', 'Licensed Clinical Social Worker','peer support specialist', 'personal agent', 'caregiver', 'Senior & Disability Services', 'The Child Center', 'Relief Nursery', 'Daisy C.H.A.I.N.', 'Easterseals Oregon', 'EasyCare Inc', 'Community Share', 'Allies, LLC', 'Connected Lane County', 'Lane Workforce Partnership', 'Lane Independent Living Alliance', 'SLLEA', 'Pearl Buck Center', 'Sponsors, Inc', 'Eugene Mission', 'Laurel Hill Center', 'Oregon Supported Living Program', 'Friends of the Children', 'Community Organized Relief Effort', 'Oregon Social Learning Center', 'Resource Connections of Oregon', 'Hope & Safety Alliance', 'HIV Alliance', 'Helping Hands Coalition', 'Meals on Wheels', 'Domestic Violence Clinic', 'Abilitree', 'Goodwill Job Connections', 'Campbell Community Center', 'Mckenzie Personnel Systems', 'Black Thistle Street Aid', 'USCRI', 'Advocates Northwest', 'Sunshine Care Environments', 'Avanti ElderCare Resources', 'NAACP']:
        res = 'Human Services'
    elif x in ['housing specialist', 'Housing Navigator', 'SquareOne Villages', 'Everyone Village', 'Sheltercare', 'Mainstream Housing, Inc', 'Cornerstone Community Housing', 'Green Leaf Village', 'Community Supported Shelters', 'Redwood Cove Senior Apartments']:
        res = 'Housing Services'
    elif x in ['counselor',  'Pacific Women’s Center', 'PeaceHealth', 'Oregon Medical Group', 'Looking Glass', 'Center for Family Development', 'Community Health', 'Springfield Treatment Center', 'Trillium', 'Willamette Family', 'White Bird Clinic', 'Facey Medical Group', 'G Street Integrated Health', 'Emergence', 'Coast Fork Nursing Center', 'Landmark Health', 'Orchid Health Fern Ridge Clinic', 'Options', 'Serenity Lane', 'ColumbiaCare Services', 'South Lane Mental Health', 'Legacy Health']:
        res = 'Health Services'
    elif x in ['SNAP Training & Employment Program', 'Temporary Assistance for Needy Families', 'Lane County Behavioral Health', 'Lane County Dovetail Program', 'Worksource Oregon', 'Housing Choice Voucher Program Section 8', 'Lane County', 'ODHS', 'Employment Department', 'Women, Infants, and Children', 'Oregon Secretary of State', 'State of Oregon', 'Medicaid', 'Department of Labor', 'Oregon Health Authority', 'HOPWA', 'Developmental Disabilities Services', 'Lane County Rural Street Outreach', 'Washington County Housing Services', 'Oregon Secretary of State']:
        res = 'Government Services'
    elif x == 'Homes For Good':
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
    hfg = re.search("Homes for Good|HFG|ho n es for good|home for goods|Homegorgood|home goods|Homesforgood|Homes4Good|Don|Homes 4 good|Home4Good|Housing For Good|Village Oaks|good for homes|Housetogood|Good Homes|Your|Housing for Good|list|Houses For Good|Home for good|office|HGF|Sarah Wilson|Walk|Drive|Homes fo Good|h 4 g|h4g|BOB|JJ|Booth|rays food place|Homesfor good|Bridges on Broadway|Drove|came|lobby|Hones for good|541-682-2550|Resident Services|Cappy|Sarah Stanley|Kat |JJ|Dustin|Johanna|Pope|Waitlist connect|Duncan|Melissa Hartman|Maclain Barney|don|already|RSS|pop up|Homes for a good|home for goods|homes for goods"+'|'+getNames(df=who, detailed_name='Homes for Good Staff'), x, re.IGNORECASE)
    svdp = re.search("Vincent|SVDP|SVPD|Second chance|St.|St V|sleep|Swick|Sarah Koski|Jeff|Amber|Vikki|Aspiranti|Aspirnanti|Ashely", x, re.IGNORECASE)
    fb = re.search("Facebook|Fb|F b|Favebook|Face book|Facebok", x, re.IGNORECASE)
    hsp = re.search("manger|Mnager|Manaement|mangement|manageent|Manger|Mnagement|Manager|manger|Case Mgr|case worker|Social Services|Counselor|Oasis|Family Coach|Service Navigator|caseworker|CM|peer support|Nurse|Personal Agent|PA|Management|social service agency|Social worker|Advocate|COUNSELER|Peer Support|caregiver|Care Provider|Service Coordinator|Intake worker|support staff|advisor|PSS|adviser|Legal Aid|worker|social|case|advo", x, re.IGNORECASE)
    lc = re.search("Lane county|lanecounty|County worker|Probation"+'|'+getNames(df=who, detailed_name='Lane County Staff Member'), x, re.IGNORECASE)                
    hsa = re.search("Hope and safety|Womenspace|woman’s space|Laura blackwell|Help and safety|Hope n safety|women space|Women's space", x, re.IGNORECASE)
    css = re.search("CSS|Community Supported|Destinee Thompson", x, re.IGNORECASE)
    hs = re.search("Housing Specialist|housing services|Housing Coordinator|Housing cordinator|housing authority|Housing advocate|Housing advo|resident services coordinator|navigator|Housing help|Housings authorities|AHO|My housing", x, re.IGNORECASE)
    odhs = re.search("HS|ODHS|DHS|Human Resources|Human Resorces|welfare|voc|D.h.s|D.h s", x, re.IGNORECASE)
    ftc = re.search("Friends of", x, re.IGNORECASE)
    ccs = re.search("CCS|Catholic comm|Cathlico community|food bank|Community Service", x, re.IGNORECASE)
    lhc = re.search("Laurel", x, re.IGNORECASE)
    ff= re.search("mom|daughter|son|father|mother|sister|brother|family|niece|wife|parent|cousin|step child|spouse|daugheter|daighter|daugter|daugther|husband|uncle|aunt|legal guardian|Dad|Relative|adult|friend|Familial|mouth|Causin|Community members|girlfriend|Frend|coworker|Roommate|neighbor|Coworker|fmaily|Co-worker|Co worker|vecino|landlord|Freind|work|talk|friemd|Firend|gma|grandma|tenant|duaghter|room mate|froiend|Firend|fr|f|Sibling|barkhimer|kids|Community|Current|employer|boss|apt mgr|aquaintence|aquaintance|Acquaintance|the guest house|wom|w"+'|'+getNames(df=who, detailed_name='Community Member'), x, re.IGNORECASE)
    ew = re.search("Weekly", x, re.IGNORECASE)
    sc = re.search("ShelterCare|Ruby Renfro|SC Staff|Catrina|Amanda|Dana|Alison Pfaff|Shelter care", x, re.IGNORECASE)
    cc = re.search("Child Center", x, re.IGNORECASE)
    wbc = re.search("White Bird|Whitebird", x, re.IGNORECASE)
    headst = re.search("Head Start|Headstart", x, re.IGNORECASE)
    lcog = re.search("Senior & Disability Services|Senior and Disable|Senior Disable|Senior and Disability|Senior and disabilities|Senior or Disabled Service|Senior Services|Senior & Disabiliy|sds|S&D|Senior & Disabled|Senior Citizens Disability", x, re.IGNORECASE)
    cfnc = re.search("Coast Fork Nursing Center", x, re.IGNORECASE)
    rg = re.search("register guard|RegisterGuard|RG", x, re.IGNORECASE)
    tri = re.search("Trillium|Chelsea|insurance", x, re.IGNORECASE)
    s8 = re.search("Section 8|baimbridge|Balmbridge|s8|Voucher|section8", x, re.IGNORECASE)
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
    si = re.search("Sponsor|megan|Meghan|Spnors|Spobnsor's|sponsers|Sponosors"+'|'+getNames(df=who, detailed_name='Sponsors Inc Staff'), x, re.IGNORECASE)
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
    email = re.search("mail|newsletter|link|emai|eamil|Enail|Emial|enail|Emqil|Eamil", x, re.IGNORECASE)
    flyer = re.search("flyer|Fkyer|flier", x, re.IGNORECASE)
    text = re.search("text|message|rext|Massage", x, re.IGNORECASE)
    web = re.search("web|internet|intenter|computer|intetnet|211|site|line|self|keep", x, re.IGNORECASE)
    wfp = re.search("workforce|work force", x, re.IGNORECASE)
    eo = re.search("Employment", x, re.IGNORECASE)
    gf = re.search("Green Leaf", x, re.IGNORECASE)
    ap = re.search("applied|Previous|always", x, re.IGNORECASE)
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
    mc = re.search("councilor|my Dr.|doctor|mental health provider|Medical Provider|Counseling|Councelor|mentor|Hospital|therapist|therapy|Jose Maria santana|councilor|Amelia Jans|clinic", x, re.IGNORECASE)
    wsc = re.search("Women’s Center", x, re.IGNORECASE)
    ph = re.search("Peace", x, re.IGNORECASE)
    lp = re.search("Love", x, re.IGNORECASE)
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
    oa = re.search("drive|Drove|came|lobby|booth|pop up", x, re.IGNORECASE)
    
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
    elif lp:
        res = 'Love Project'  
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
    elif call:
        res = 'Phone call'
    elif gg:
        res = 'Google'
    elif web:
        res = 'website'
    elif oa:
        res = 'other agencies'
    elif ff:
        res = 'family and friends'
    elif email:
        res = 'Email'
    elif flyer:
        res = 'flyer'
    elif text:
        res = 'text message'
    elif svdp:
        res = 'St. Vincent de Paul'
    else:
        res = 'unknown'
    return res

def categorize_p9_b(x):
    if x in ['family and friends', 'text message', 'Email']:
        res = 'Community Members'
    elif x in ['human services', 'Senior & Disability Services', 'The Child Center', 'Relief Nursery', 'Daisy C.H.A.I.N.', 'Easterseals Oregon', 'EasyCare Inc', 'Community Share', 'Allies, LLC', 'Connected Lane County', 'Lane Workforce Partnership', 'Lane Independent Living Alliance', 'SLLEA', 'Pearl Buck Center', 'Sponsors, Inc', 'Eugene Mission', 'Laurel Hill Center', 'Oregon Supported Living Program', 'Friends of the Children', 'Community Organized Relief Effort', 'Oregon Social Learning Center', 'Resource Connections of Oregon', 'Hope & Safety Alliance', 'HIV Alliance', 'Helping Hands Coalition', 'Meals on Wheels', 'Domestic Violence Clinic', 'Abilitree', 'Goodwill Job Connections']:
        res = 'Human Services'
    elif x in ['housing specialist', 'Affordable Housing', 'SquareOne Villages', 'Everyone Village', 'Sheltercare', 'Mainstream Housing, Inc', 'Cornerstone Community Housing', 'transitional housing', 'Green Leaf Village', 'Community Supported Shelters']:
        res = 'Housing Services'
    elif x in ['medical provider or therapist', 'Pacific Women’s Center', 'PeaceHealth', 'Oregon Medical Group', 'Looking Glass', 'Center for Family Development', 'Community Health', 'Springfield Treatment Center', 'Trillium', 'Willamette Family', 'White Bird Clinic', 'Facey Medical Group', 'G Street Integrated Health', 'Emergence', 'Coast Fork Nursing Center', 'Landmark Health', 'Orchid Health Fern Ridge Clinic', 'Options', 'South Lane Mental Health']:
        res = 'Health Services'
    elif x in ['social media', 'Google', 'Reddit', 'Eugene Weekly', 'Register-Guard', 'news', 'website', 'billboard', 'Instagram', 'Public Notice Oregon', 'Facebook']:
        res = 'Media Communications'
    elif x in ['SNAP Training & Employment Program', 'Temporary Assistance for Needy Families', 'Lane County Behavioral Health', 'Lane County Dovetail Program', 'Worksource Oregon', 'Housing Choice Voucher Program Section 8', 'Lane County', 'ODHS', 'Employment Department', 'Women, Infants, and Children', 'Oregon Secretary of State', 'State of Oregon', 'Medicaid', 'Department of Labor', 'Oregon Health Authority', 'HOPWA', 'Developmental Disabilities Services', 'Lane County Rural Street Outreach', 'Washington County Housing Services', 'Oregon Secretary of State']:
        res = 'Government Services'
    elif x in ['Homes For Good', 'flyer', 'Phone call', 'former applicant']:
        res = 'Homes For Good'
    elif x == 'unknown':
        res = 'Unknown'
    else:
        res = 'Community Organization'
    return res

def categorize_p9_c(x):
    email = re.search("mail|newsletter|link|emai|eamil|Enail|Emial|enail|Emqil|Eamil|sent", x, re.IGNORECASE)
    sm = re.search('Facebook|Fb|F b|Favebook|Face book|Facebok|SM|Social media|REDDIT|Instagram', x, re.IGNORECASE)
    flyer = re.search("flyer|Fkyer|flier", x, re.IGNORECASE)
    text = re.search("text|message|rext|Massage", x, re.IGNORECASE)
    news = re.search("Eugene Weekly|register guard|RegisterGuard|RG|News|notice", x, re.IGNORECASE)
    se = re.search('Google|search|check', x, re.IGNORECASE)
    web = re.search("web|internet|intenter|computer|intetnet|affordablehousing|Affordable Housing|affordablehomes|.com|.org|211|site|in line|online|on line", x, re.IGNORECASE)
    call = re.search("call|phone|541", x, re.IGNORECASE)
    ov = re.search("office|drive|came|walk|booth|pop up|drove|went|rays food place|lobby", x, re.IGNORECASE)
    wom = re.search("mouth|talk|hear|ask|meet|visit|said|say", x, re.IGNORECASE)
    
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
