"""Generate the synthetic Rabt professional-network dataset (star schema).
Usage: python generate_dataset.py [output_dir]
Writes CSVs to <output_dir>/csv and an Excel workbook to <output_dir>.
"""
import numpy as np, pandas as pd, sys, os
rng=np.random.default_rng(2026)
OUT=sys.argv[1] if len(sys.argv)>1 else "data"
os.makedirs(f"{OUT}/csv",exist_ok=True)
# ---------- Date
dates=pd.date_range('2025-01-01','2026-10-31')
dd=pd.DataFrame({'Date':dates})
dd['Year']=dd.Date.dt.year; dd['MonthNo']=dd.Date.dt.month
dd['Month']=dd.Date.dt.strftime('%b'); dd['YearMonth']=dd.Date.dt.strftime('%Y-%m')
dd['Quarter']='Q'+dd.Date.dt.quarter.astype(str)
dd['Weekday']=dd.Date.dt.strftime('%a'); dd['WeekdayNo']=(dd.Date.dt.weekday+1)%7+1  # Sun=1
dd['IsWeekend']=dd.Date.dt.weekday.isin([4,5])  # Fri/Sat
ram=((dd.Date>='2025-03-01')&(dd.Date<='2025-03-30'))|((dd.Date>='2026-02-18')&(dd.Date<='2026-03-19'))
dd['IsRamadan']=ram
# ---------- Skills
skills=[('Power BI','Data & BI'),('SQL','Data & BI'),('Excel','Data & BI'),('Python','Programming'),('Tableau','Data & BI'),
('Data Analysis','Data & BI'),('Machine Learning','AI'),('Generative AI','AI'),('Cybersecurity','Security'),('Cloud (Azure/AWS)','Cloud'),
('ERP (Odoo/SAP)','Business Systems'),('CRM','Business Systems'),('Project Management','Business'),('Business Analysis','Business'),
('Digital Marketing','Business'),('Java','Programming'),('UI/UX','Design'),('Communication','Soft Skills'),('Arabic/English','Soft Skills'),('Agile/Scrum','Business')]
dsk=pd.DataFrame(skills,columns=['Skill','SkillCategory']); dsk.insert(0,'SkillID',range(1,len(dsk)+1))
# ---------- Members
cities=['Riyadh','Jeddah','Dammam','Khobar','Makkah','Madinah','Tabuk','Abha','Qassim','NEOM']
cw=np.array([.34,.2,.09,.07,.06,.06,.06,.04,.05,.03])
inds=['Information Technology','Telecommunications','Banking & Finance','Government','Healthcare','Energy','Retail','Education','Consulting','Logistics']
iw=np.array([.2,.1,.13,.12,.08,.08,.08,.08,.07,.06])
sen=['Student','Entry','Associate','Mid-Senior','Manager','Director']; sw=np.array([.18,.22,.2,.22,.13,.05])
N=6000
jd=rng.choice(dates[dates<'2026-10-01'],N)
# growth: more joins later
w=np.linspace(1,2.4,len(dates[dates<'2026-10-01'])); w/=w.sum()
jd=rng.choice(dates[dates<'2026-10-01'],N,p=w)
dm=pd.DataFrame({'MemberID':np.arange(1,N+1),'JoinDate':jd,'City':rng.choice(cities,N,p=cw),
 'Industry':rng.choice(inds,N,p=iw),'Seniority':rng.choice(sen,N,p=sw),
 'Gender':rng.choice(['Female','Male'],N,p=[.46,.54]),
 'AgeBand':rng.choice(['18-24','25-34','35-44','45+'],N,p=[.27,.43,.21,.09])})
dm=dm.sort_values('JoinDate').reset_index(drop=True); dm['MemberID']=np.arange(1,N+1)
dm['JoinDate']=dm.JoinDate.dt.date
# ---------- Companies (fictional)
pre=['Najd','Sahab','Raqam','Masar','Waha','Bayan','Thuraya','Rawabi','Nukhba','Afaq','Sadeem','Qimam','Jusoor','Manara','Tamkeen','Ruwad','Dana','Itqan','Ufuq','Basma']
suf=['Tech','Analytics','Solutions','Digital','Systems','Group','Labs','Consulting']
names=set()
while len(names)<120: names.add(f"{rng.choice(pre)} {rng.choice(suf)}")
names=sorted(names)
dc=pd.DataFrame({'CompanyID':range(1,121),'Company':names,'Industry':rng.choice(inds,120,p=iw),
 'CompanySize':rng.choice(['1-50','51-200','201-1000','1000+'],120,p=[.25,.3,.27,.18]),'HQCity':rng.choice(cities,120,p=cw)})
# ---------- Jobs
titles={'Data & BI':['Data Analyst','BI Developer','Reporting Analyst','Data Engineer'],'AI':['ML Engineer','AI Specialist'],
'Business':['Business Analyst','Project Coordinator','Product Analyst'],'Security':['SOC Analyst','Cybersecurity Specialist'],
'Business Systems':['ERP Consultant','CRM Analyst'],'Programming':['Software Developer','Python Developer'],'Cloud':['Cloud Engineer'],'Design':['UI/UX Designer']}
cats=list(titles); catw=np.array([.3,.1,.17,.1,.1,.12,.06,.05])
J=1800
pdts=rng.choice(dates[dates<'2026-10-20'],J,p=np.linspace(1,2,len(dates[dates<'2026-10-20']))/np.linspace(1,2,len(dates[dates<'2026-10-20'])).sum())
jc=rng.choice(cats,J,p=catw)
jobs=[]
for i in range(J):
    c=jc[i]; co=dc.iloc[rng.integers(0,120)]
    lvl=rng.choice(['Internship','Entry','Associate','Mid-Senior','Manager'],p=[.12,.3,.25,.23,.1])
    base={'Internship':4,'Entry':9,'Associate':13,'Mid-Senior':20,'Manager':30}[lvl]*1000
    sal=int(round(base*rng.uniform(.85,1.3),-2)) if lvl!='Internship' else int(round(rng.uniform(2500,5000),-2))
    jobs.append({'JobID':i+1,'CompanyID':int(co.CompanyID),'PostDate':pd.Timestamp(pdts[i]).date(),'JobTitle':rng.choice(titles[c]),
      'JobFamily':c,'City':rng.choice(cities,p=cw),'ExperienceLevel':lvl,'WorkType':rng.choice(['On-site','Hybrid','Remote'],p=[.55,.33,.12]),
      'MonthlySalarySAR':sal,'IsSaudizationTarget':bool(rng.random()<.7)})
fj=pd.DataFrame(jobs)
# job skills bridge
catskill={c:dsk[dsk.SkillCategory==c].SkillID.tolist() for c in dsk.SkillCategory.unique()}
fam2cat={'Data & BI':['Data & BI','Programming','AI'],'AI':['AI','Programming','Data & BI'],'Business':['Business','Data & BI','Soft Skills'],
'Security':['Security','Cloud','Programming'],'Business Systems':['Business Systems','Business','Data & BI'],'Programming':['Programming','Cloud','AI'],
'Cloud':['Cloud','Security','Programming'],'Design':['Design','Business','Soft Skills']}
br=[]
SKW={1:2.2,2:2.0,3:1.6,4:1.8,6:1.7,16:0.45,5:0.8,8:1.2}
for r in fj.itertuples():
    pool=sum([catskill[c] for c in fam2cat[r.JobFamily]],[])
    wts=np.array([SKW.get(int(x),1.0) for x in pool]); wts=wts/wts.sum()
    for s in rng.choice(pool,min(len(pool),rng.integers(2,5)),replace=False,p=wts): br.append((r.JobID,int(s)))
bjs=pd.DataFrame(br,columns=['JobID','SkillID']).drop_duplicates()
# ---------- Applications
apps=[]; aid=1
stages=['Applied','Viewed','Interview','Offer','Hired']
for r in fj.itertuples():
    pop={'Internship':14,'Entry':12,'Associate':8,'Mid-Senior':6,'Manager':4}[r.ExperienceLevel]*(1.4 if r.WorkType=='Remote' else 1)
    n=rng.poisson(pop)
    for _ in range(n):
        ad=pd.Timestamp(r.PostDate)+pd.Timedelta(days=int(rng.exponential(5)))
        if ad>dates[-1]: continue
        # funnel
        p=[.62,.38,.32,.78]  # Applied->Viewed, Viewed->Interview, Interview->Offer, Offer->Hired
        st=0
        for k in range(4):
            if rng.random()<p[k]: st=k+1
            else: break
        status=stages[st]
        if st<4 and rng.random()<.55 and st>=1: status='Rejected'
        apps.append({'ApplicationID':aid,'JobID':r.JobID,'MemberID':int(rng.integers(1,N+1)),'ApplyDate':ad.date(),
          'Source':rng.choice(['Easy Apply','Company Website','Referral','Recruiter InMail'],p=[.55,.25,.12,.08]),
          'FurthestStage':stages[st],'Status':status,'DaysToFirstResponse':(int(rng.gamma(2,3.5))+1) if st>=1 else None})
        aid+=1
fa=pd.DataFrame(apps)
# ---------- Posts (engagement)
types=['Text','Image','Video','Document','Article','Poll']; tw=[.3,.28,.12,.14,.08,.08]
reach={'Text':1.0,'Image':1.35,'Video':1.6,'Document':1.9,'Article':.8,'Poll':1.5}
topics=['Career Tips','Data & BI','AI','Achievement','Hiring','Industry News','Vision 2030','Learning & Certificates']
topw=[.16,.16,.15,.12,.1,.11,.08,.12]
P=22000
pd_=rng.choice(dates,P,p=np.linspace(1,2.2,len(dates))/np.linspace(1,2.2,len(dates)).sum())
posts=[]
HW=np.array([1,.5,.3,.2,.2,.4,1,2,3.5,4,3.5,3,3,3,3,2.5,2.5,3,3.5,4,4.5,4,3,2]);HW=HW/HW.sum()
for i in range(P):
    d=pd.Timestamp(pd_[i]); t=rng.choice(types,p=tw); tp=rng.choice(topics,p=topw)
    wk=.75 if d.weekday() in (4,5) else 1.0
    rm=.85 if ((d>=pd.Timestamp('2025-03-01'))&(d<=pd.Timestamp('2025-03-30')))|((d>=pd.Timestamp('2026-02-18'))&(d<=pd.Timestamp('2026-03-19'))) else 1
    imp=int(rng.lognormal(6.3,0.9)*reach[t]*wk*rm*(1.3 if tp in('Achievement','AI') else 1))
    er=rng.beta(2,60)*(1.5 if tp=='Achievement' else 1)*(1.3 if t=='Poll' else 1)
    re=int(imp*er); cm=int(re*rng.uniform(.05,.25)*(2 if t=='Poll' else 1)); rp=int(re*rng.uniform(.02,.1))
    posts.append({'PostID':i+1,'MemberID':int(rng.integers(1,N+1)),'PostDate':d.date(),'PostHour':int(rng.choice(range(24),p=HW)),
      'PostType':t,'Topic':tp,'Impressions':imp,'Reactions':re,'Comments':cm,'Reposts':rp,'Clicks':int(imp*rng.uniform(.005,.03))})
fp=pd.DataFrame(posts)
fp['PostHour']=fp.PostHour
# ---------- Save
dd['Date']=dd.Date.dt.date
tables={'DimDate':dd,'DimMember':dm,'DimCompany':dc,'DimSkill':dsk,'FactJobPostings':fj,'BridgeJobSkill':bjs,'FactApplications':fa,'FactPosts':fp}
for k,v in tables.items(): v.to_csv(f'{OUT}/csv/{k}.csv',index=False,encoding='utf-8-sig')
with pd.ExcelWriter(f'{OUT}/Rabt_Professional_Network_Dataset.xlsx') as xw:
    for k,v in tables.items(): v.to_excel(xw,sheet_name=k,index=False)
for k,v in tables.items(): print(k,len(v))
