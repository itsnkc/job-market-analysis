import time
import random
import requests
import pandas as pd

class Job104Market():
    
    # 取得搜尋結果頁面data
    def job_list(self, keyword, max_mun=10, filter_params=None):
        jobs = []
        total_count = 0

        url = 'https://www.104.com.tw/jobs/search/list'
        query = f'ro=0&kwop=7&keyword={keyword}&expansionType=area,spec,com,job,wf,wktm&mode=s&jobsource=2018indexpoc'
        if filter_params:
            # 加上篩選參數，要先轉換為 URL 參數字串格式
            query += ''.join([f'&{key}={value}' for key, value, in filter_params.items()])

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
            'Referer': 'https://www.104.com.tw/jobs/search/',
        }
               
        page = 1
        while len(jobs) < max_mun:
            params = f'{query}&page={page}'
            r = requests.get(url, params=params, headers=headers)
            if r.status_code != requests.codes.ok:
                print('請求失敗', r.status_code)
                data = r.json()
                print(data['status'], data['statusMsg'], data['errorMsg'])
                break

            data = r.json()
            total_count = data['data']['totalCount']
            jobs.extend(data['data']['list'])

            if (page == data['data']['totalPage']) or (data['data']['totalPage'] == 0):
                break
            page += 1
            time.sleep(random.uniform(5, 10))

        return total_count, jobs[:max_mun]

    # 取得職缺詳細資料頁面data
    def get_job(self, job_id):
        url = f'https://www.104.com.tw/job/ajax/content/{job_id}'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
            'Referer': f'https://www.104.com.tw/job/{job_id}'
        }

        r = requests.get(url, headers=headers)
        if r.status_code != requests.codes.ok:
            print('請求失敗', r.status_code)
            time.sleep(random.uniform(5, 10))
            return

        data = r.json()
        return data['data']
    
    # 資料清理>>搜尋結果data
    def job_list_transform(self, job_list):
        """將職缺資料轉換格式、補齊資料"""
        appear_date = job_list['appearDate']
        apply_num = int(job_list['applyCnt'])
        company_addr = f"{job_list['jobAddrNoDesc']} {job_list['jobAddress']}"

        job_url = f"https:{job_list['link']['job']}"
        job_company_url = f"https:{job_list['link']['cust']}"

        # 擷取job_id
        job_id = job_url.split('/job/')[-1]
        if '?' in job_id:
            job_id = job_id.split('?')[0]
            
        # 結區comp_id
        comp_id = job_company_url.split('/company/')[-1]
        if '?' in comp_id:
            comp_id = comp_id.split('?')[0]

        salary_high = int(job_list['salaryLow'])
        salary_low = int(job_list['salaryHigh'])

        job_list = {
            'job_id': job_id,
            'type': job_list['jobType'], # 工作性質
            'name': job_list['jobName'],  # 職缺名稱
            
            'appear_date': appear_date,  # 更新日期
            'job_url': job_url,  # 職缺網頁
            'job_company_url': job_company_url,  # 公司介紹網頁
            
            'apply_num': apply_num, # 應徵人數
            'apply_text': job_list['applyDesc'],  # 應徵人數描述
            
            'comp_id': comp_id,
            'company_name': job_list['custName'],  # 公司名稱
            'company_industry': job_list['coIndustryDesc'],  # 公司產業
            'company_zone': job_list['jobAddrNoDesc'], # 工作地區
            'company_addr': company_addr,  # 工作地址
            'company_landmark': job_list['landmark'], # 附近地標(捷運站)
            
            'period': job_list['periodDesc'],  # 經驗年份
            
            'salary': job_list['salaryDesc'],  # 薪資描述
            'salary_high': salary_high,  # 薪資最高
            'salary_low': salary_low,  # 薪資最低
            
            'tags': job_list['tags'],  # 標籤
        }
        return job_list
    
    # 資料清理>>職缺詳細data
    def job_detail_transform(self, job_detail):

        # 擷取技能（擅長工具）
        sk = []
        for i in range(len(job_detail['condition']['specialty'])):
            sk.append(job_detail['condition']['specialty'][i]['description'])
        specialty = ' | '.join(sk)
        
        # 擷取職務類別
        jc = []
        for n in range(len(job_detail['jobDetail']['jobCategory'])):
            jc.append(job_detail['jobDetail']['jobCategory'][n]['description'])
        jobCategory = ' | '.join(jc)    
        
        job_detail = {
            
            # condition 條件要求區
            'education': job_detail['condition']['edu'],  # 學歷要求
            'major': job_detail['condition']['major'],  # 科系要求
            'other': job_detail['condition']['other'],  # 其他條件
            'skill': job_detail['condition']['skill'],  # 工作技能
            'specialty': specialty,  # 擅長工具
            
            # jobDetail 工作內容區
            'businessTrip': job_detail['jobDetail']['businessTrip'], # 出差外派
            'jobCategory': jobCategory, # 職務類別
            'jobDescription': job_detail['jobDetail']['jobDescription'], # 工作內容描述
            'manageResp': job_detail['jobDetail']['manageResp'], # 管理責任
            'needEmp': job_detail['jobDetail']['needEmp'], # 需求人數
            'startWorkingDay': job_detail['jobDetail']['startWorkingDay'], # 可上班日
            'vacationPolicy': job_detail['jobDetail']['businessTrip'], # 休假制度
            'workPeriod': job_detail['jobDetail']['workPeriod'], # 上班時段
            'remoteWork': job_detail['jobDetail']['remoteWork'], # 遠端工作
            
        }
        return job_detail

#---------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    job104_search = Job104Market()

    filter_params = {
        #'area': '6001001000',  # 地區：台北市
        'area': '6001001012',  # 地區：台北市中正區
        'jobcat': '2007000000', # 職務類別：資訊系統管理類
        #'jobcat': '2007000000,2003002002,2003002008,2004001010', # 職務類別：資訊系統管理類
        'ro': '1', # 全職=1, 全部=0
        'kwop': '1' # 只搜尋職務名稱
    }
    
    #keywords = '資料工程 數據工程 ETL 資料庫 Data Engineering' # 職缺搜尋關鍵字
    #keywords = '資料分析 數據分析 商業分析 Data Analyst'
    keywords = '資料科學 機器學習 深度學習 人工智慧 演算法 影像辨識 Data science' 
    #job_group = 'de' # DS=資料科學, DE=資料工程, DA=資料分析
    job_group = {'group_name': 'ds'} # DS=資料科學, DE=資料工程, DA=資料分析
    
    total_count, jobs = job104_search.job_list(keywords, max_mun=1000, filter_params=filter_params)

    print('搜尋結果職缺總數：', total_count)
    print(filter_params['area'])
    print(len(jobs))
    jobs = [job104_search.job_list_transform(job) for job in jobs]
    
    for x in range (len(jobs)):
        job_info = job104_spider.get_job(jobs[x]['job_id'])
        #job_d.append(job_info)
        #print(job_info)
        #print(type(job_info))
        job_details = job104_search.job_detail_transform(job_info)     
        jobs[x].update(job_details)
        jobs[x].update(job_group)

    #print(jobs)

df = pd.DataFrame(jobs)
df.to_excel(job_group['group_name']+'_'+filter_params['area']+'.xlsx')
