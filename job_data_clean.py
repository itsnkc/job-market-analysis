import pandas as pd

# 關鍵字設定
de_keywords = ['資料工程', '數據工程', 'ETL', '資料庫', 'Data Engineering', 'Data Engineer','資料探勘工程'
            , '數據分析工程', '資料分析工程', '數據架構', '資料倉儲', 'Data Infra Engineer', '數據處理'
            , '資料處理', '數據應用', '資料應用', '數據(資深)工程師']

ds_keywords = ['資料科學', '機器學習', '深度學習', '人工智慧', '演算法', '影像辨識', 'Data science'
               , 'Data Scientist', 'AI', '數據科學', '影像', '智慧', '電腦視覺']

da_keywords = ['資料分析', '數據分析', '商業分析', 'Data Analyst', '分析師'
               , '研究員', 'Analyst', 'BI', '統計']

df = pd.read_excel('da_all.xlsx')

# 更新data
for i in range (len(df)):
    # 更新reject
    reject = 'Y'
    for j in da_keywords:
        if j in df['name'][i]:
            reject = 'N'
    df.loc[i, 'reject'] = reject

df.to_excel('da_all_update.xlsx')
