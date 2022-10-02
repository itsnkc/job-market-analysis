import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

plt.rcParams['font.family'] = ['Arial Unicode MS'] # 顯示中文

df1 = pd.read_excel('ds_all_update.xlsx', sheet_name='comp_cnt') # 資料科學
df2 = pd.read_excel('de_all_update.xlsx', sheet_name='comp_cnt') # 資料工程
df3 = pd.read_excel('da_all_update.xlsx', sheet_name='comp_cnt') # 資料分析

#print(df3.query("clm == 'company_industry'")) # select

# 合併資料
#df = df1.append(df2, ignore_index=True)
#df = df.append(df3, ignore_index=True)

# 1.area
#fig, ax = plt.subplots(figsize=(17, 8))
#plt.xticks(rotation=45) # 座標傾斜角度
#plt = sns.countplot(x='Area', hue='Group', data=df, palette='rocket') 
#plt.set_title('Area', fontsize=30)
#plt.legend(labels=['Data Science', 'Data Engineering', 'Data Analysis'], loc=1)

# 2.experience
#fig, ax = plt.subplots(figsize=(17, 8))
#plt.xticks(rotation=45) # 座標傾斜角度
#plt = sns.countplot(x='Experience', hue='Group', data=df, palette='mako' 
 #             , order=['經歷不拘','1年以上','2年以上','3年以上','4年以上','5年以上'
 #                        ,'6年以上','7年以上','8年以上','10年以上'])
#plt.set_title('Experience', fontsize=30)
#plt.legend(labels=['Data Science', 'Data Engineering', 'Data Analysis'], loc=1)

# 3.industry
#fig, ax = plt.subplots(figsize=(15, 8))
#df = df3.query("column == 'company_industry'")
#plt = sns.barplot(x='count', y='item', data=df, palette='flare') # Paired藍色系
#plt.set_title('Industry (Data Analysis)', fontsize=30)

# 4.major
#fig, ax = plt.subplots(figsize=(15, 8))
#df = df3.query("column == 'major'")
#plt = sns.barplot(x='count', y='item', data=df, palette='viridis') 
#plt.set_title('Major (Data Analysis)', fontsize=30)

# 5.jobCategory
#fig, ax = plt.subplots(figsize=(15, 8))
#df = df3.query("column == 'job'")
#plt = sns.barplot(x='count', y='item', data=df, palette='Spectral')
#plt.set_title('Job Category (Data Analysis)', fontsize=30)

# 6.skill
#fig, ax = plt.subplots(figsize=(15, 8))
#df = df3.query("column == 'skill'")
#plt = sns.barplot(x='count', y='item', data=df, palette='icefire')
#plt.set_title('Skill (Data Analysis)', fontsize=30)

# 7.specialty
fig, ax = plt.subplots(figsize=(20, 10))
plt.xticks(rotation=45) # 座標傾斜角度
df = df3.query("column == 'specialty'")
plt = sns.barplot(x='item', y='count', data=df, palette='hls') 
plt.set_title('Specialty (Data Analysis)', fontsize=30)
