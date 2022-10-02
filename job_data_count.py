import pandas as pd

'''
清理:
科系 major[]
技能 skill[]
擅長工具 specialty[]
職務類別 jobCategory[]
'''

df = pd.read_excel('ds_all_update.xlsx')

# 科系 major
mj = []    
major = []
major_cnt = {}

for ma in df['major']:
    mj.append(ma.replace('[','').replace(']','').replace('\'','').replace(' ','').split(','))

for ma in mj:
    for s in range(len(ma)):
        if ma[s]!='':
            major.append(ma[s]) 

for ma in major: # 統計次數
    k = ma
    v = major.count(ma)
    if k not in major_cnt:
        major_cnt[k] = v

#[print(key, value) for key, value in major_cnt.items()]

# 技能 skill
sk = []
skill = []
skill_cnt = {}

for s in df['skill'].replace('[','').replace(']',''):
    if s == '[]':
        continue
    else:
        sk.append(s.replace('[','').replace(']','').split(','))
for j in sk:
    sDict = dict(zip(j[::2], j[1::2]))
    for key, value in sDict.items():
        skill.append(value.replace('description','').replace('\'','').replace(':','').replace('}','').replace(' ',''))

for s in skill: # 統計次數
    k = s
    v = skill.count(s)
    if k not in skill_cnt:
        skill_cnt[k] = v

#[print(key, value) for key, value in skill_cnt.items()]

# 擅長工具 specialty
tools = []
specialty = [] # 職務類別
specialty_cnt = {}

for tool in df['specialty']:
    if type(tool) != float:
        tools.append(tool.split(' | '))

for tool in tools:
    for c in range(len(tool)):
        specialty.append(tool[c]) 

for tool in specialty: # 統計次數
    k = tool
    v = specialty.count(tool)
    if k not in specialty_cnt:
        specialty_cnt[k] = v

#[print(key, value) for key, value in specialty_cnt.items()]

# 職務類別 jobCategory
job_cate = []
jobCategory = [] # 職務類別
jobCategory_cnt = {}

for job in df['jobCategory']:
    job_cate.append(job.split(' | '))

for job in job_cate:
    for c in range(len(job)):
        if job[c]!='':
            jobCategory.append(job[c]) 

for job in jobCategory: # 統計次數
    k = job
    v = jobCategory.count(job)
    if k not in jobCategory_cnt:
        jobCategory_cnt[k] = v

#[print(key, value) for key, value in jobCategory_cnt.items()]

df1 = pd.DataFrame(list(major_cnt.items()), columns=['item','count'])
df2 = pd.DataFrame(list(skill_cnt.items()), columns=['item','count'])
df3 = pd.DataFrame(list(specialty_cnt.items()), columns=['item','count'])
df4 = pd.DataFrame(list(jobCategory_cnt.items()), columns=['item','count'])

df1 = df1.append(df2, ignore_index=True)
df1 = df1.append(df3, ignore_index=True)
df1 = df1.append(df4, ignore_index=True)

df1.to_excel('ds_all_count.xlsx', sheet_name='cnt')
