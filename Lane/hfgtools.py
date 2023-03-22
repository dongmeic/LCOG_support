import pandas as pd
import os, re

def categorize_response(x):
    #print(x)
    wf = re.search("WILLAMETTE fAMILY|WF|wam fam|wamfam|fam", x, re.IGNORECASE)
    lh = re.search("Legacy Health", x, re.IGNORECASE)
    em = re.search("julie hansen|eugene mission", x, re.IGNORECASE)
    family = re.search("mom|daughter|son|father|mother|sister|brother|family|niece|wife|parent|cousin|step child|spouse|daugheter|daighter|daugter|husband|uncle|aunt|legal guardian|Dad", x, re.IGNORECASE)
    friend = re.search("girlfriend|friend|Frend|coworker|Roommate|neighbor", x, re.IGNORECASE)
    manager = re.search("Case Manager|Caser manager|cm|Case Mgr|case manger|NCM|Case Management|Case Managment|Case  Manager|casemanager|Case Mnager", x, re.IGNORECASE)
    hfg = re.search("HFG|Homes For Good|Home4Good|homes fro Good|Home for Good|flyer|541-682-2550|Resident Services|Cappy|Sarah Stanley|Kat |JJ|Laci Pope|Dustin|Johanna|L. Pope|Waitlist connect|Duncan|Melissa Hartman|Maclain Barney|don", x, re.IGNORECASE)
    btsa = re.search("Black Thistle street aid|Bridgette", x, re.IGNORECASE)
    rn = re.search("Relief Nursery", x, re.IGNORECASE)
    csi = re.search("ColumbiaCare", x, re.IGNORECASE)
    ccs = re.search("Catholic community services", x, re.IGNORECASE)
    sc = re.search("ShelterCare|Ruby Renfro|SC Staff", x, re.IGNORECASE)
    sce = re.search("Sunshine Care Environments", x, re.IGNORECASE)
    lcsw = re.search('LCSW', x, re.IGNORECASE)
    lc = re.search("Lane COunty", x, re.IGNORECASE)
    step = re.search("STEP|Gretchen Stupke|Lindsay|Gretchen Stupke", x, re.IGNORECASE)
    cw = re.search("Case Worker|caseworker", x, re.IGNORECASE)
    cs = re.search("Community Share|Community Sharing", x, re.IGNORECASE)
    lcbh = re.search("LCBH|Lane County Behavioral Health", x, re.IGNORECASE)
    lcdp = re.search("Dovetail", x, re.IGNORECASE)
    cg = re.search("caregiver", x, re.IGNORECASE)
    cfnc =  re.search("Coast Fork Nursing Center", x, re.IGNORECASE)
    svdp = re.search("SVDP|St. Vincent de paul|Vikki Perpinan|Melissa Swick|Sarah Koski|Jeff Wolfe|Amber Fitch|Vikki  Perpinan|Vikki M Perpinan|VikkiPerpinan", x, re.IGNORECASE)
    oslp = re.search("Oregon Supported Living Program", x, re.IGNORECASE)
    lila = re.search("Independent Living|LILA", x, re.IGNORECASE)
    an = re.search("Advocates Northwest", x, re.IGNORECASE)
    wbc = re.search("White Bird|David Joseph|Whitebird", x, re.IGNORECASE)
    cht = re.search("Claire Hutton", x, re.IGNORECASE)
    ps = re.search("Peer Support", x, re.IGNORECASE)
    lhc = re.search("Laurel Hill Center", x, re.IGNORECASE)
    s = re.search("staff", x, re.IGNORECASE)
    hs = re.search("Housing Specialist", x, re.IGNORECASE)
    a =  re.search("advocate", x, re.IGNORECASE)
    slmh = re.search("South Lane Mental Health", x, re.IGNORECASE)
    gsih = re.search("G Street Integrated Health", x, re.IGNORECASE)
    cch = re.search("Cornerstone Community Housing", x, re.IGNORECASE)
    cri = re.search("USCRI", x, re.IGNORECASE)
    hiva = re.search("HIV Alliance|Ali Sanchez", x, re.IGNORECASE)
    ohop = re.search("OHOP", x, re.IGNORECASE)
    naacp = re.search("NAACP", x, re.IGNORECASE)
    hn = re.search("Navigator", x, re.IGNORECASE)
    css = re.search("CSS|Community Supported Shelters|Destinee Thompson", x, re.IGNORECASE)
    odhs = re.search("HS", x, re.IGNORECASE)
    sllea = re.search("SLLEA", x, re.IGNORECASE)
    sds = re.search("Senior and Disabled Services", x, re.IGNORECASE)
    rcsa = re.search("Redwood Cove Senior Apartments|Del Norte Senior Center", x, re.IGNORECASE)
    ta = re.search("Trisha Aspiranti|Trish Aspiranti|Trisha Aspiranti|Trisha Aspirnanti", x, re.IGNORECASE)
    epl = re.search("library", x, re.IGNORECASE)
    allc = re.search("Allies LLC", x, re.IGNORECASE)
    hsa = re.search("Hope for safety alliance", x, re.IGNORECASE)
    aer = re.search("Avanti ElderCare Resources", x, re.IGNORECASE)
    ch = re.search("Community Health", x, re.IGNORECASE)
    lqp = re.search("La-Quan Pope|LaQuan Pope", x, re.IGNORECASE)
    mhi = re.search("Mainstreamhousing Inc.|Heath Stark", x, re.IGNORECASE)
    ws = re.search("Worksource|work source|worksouce", x, re.IGNORECASE)
    si = re.search("Sponsors Inc|sPONSORS|megan oniel|Meghan Oneill|Megan O'Neill|Megan Oniell|Megan Oneill", x, re.IGNORECASE)
    cco = re.search("Louis Diaz Medina|Sonja Hyslip|Disaster Case Manager", x, re.IGNORECASE)
    rs = re.search("Rural Street|rural outreach", x, re.IGNORECASE)
    dc = re.search("Daisy CHAIN", x, re.IGNORECASE)
    sv = re.search("opportunity village", x, re.IGNORECASE)
    hhc = re.search("Helping Hands", x, re.IGNORECASE)
    if family:
        res = 'family'
    elif em:
        res = 'Eugene Mission'
    elif lh:
        res = 'Legacy Health'
    elif wf:
        res = 'Willamette Family'
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
    elif lqp:
        res = 'La-Quan Pope'
    elif aer:
        res = 'Avanti ElderCare Resources'
    elif ch:
        res = 'Community Health'
    elif cht:
        res = 'Claire Hutton'
    elif ta:
        res = 'Trisha Aspiranti'
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
    elif cg:
        res = 'casegiver'
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
        res = 'LCOG SDS'   
    elif a:
        res = 'advocate'
    elif friend:
        res = 'friend'
    elif step:
        res = 'SNAP Training & Employment Program'
    elif manager:
        res = 'case manager'
    else:
        res = 'others'
    return res