# 資料科學就業市場分析-以台北市為例
在資料科學領域中，最常聽到的三大角色是：資料科學家、資料工程師、資料分析師，近期，我積極地準備尋找有關資料科學的職缺。在人力銀行網站中，根據搜尋條件跳出幾百筆、幾千筆的職缺訊息，我開始思考是不是有不同的方法可以去搜尋職缺。

希望能夠有系統性地去分析了解就業市場對於這三個角色的期望，因此發起了這個Side project來分析就業市場，同時也能應用我所學習到的關於這個領域的技能與知識。

在本項目中，根據取得的資料來探索幾個關於資料科學就業市場的問題：
1. 職缺分佈集中於哪些地區? (資料範圍為台北市12個行政區)
2. 該領域需要的經驗水平為何?
3. 有哪些產業積極在該領域發展?
4. 哪些科系是該領域所期望的?
5. 該領域有哪些職務類別?
6. 招募公司最需要的技能與專長為何?

## Technology
- Python, Anaconda
- Web crawler, Requests, pandas, Seaborn, matplotlib

## Search Condition
- 資料來源皆為[104人力銀行](https://www.104.com.tw/jobs/main/)網站
- 依照資料科學家、資料工程師、資料分析師分為三組條件：

|          | 資料科學家 | 資料工程師      | 資料分析師 |
| -------- | ---------- | ------------ | ---------- |
| 關鍵字    | 資料科學、機器學習、深度學習、人工智慧、演算法、影像辨識、Data science     | 資料工程、數據工程、ETL、資料庫、Data Engineering | 資料分析、數據分析、商業分析、Data Analyst      |
| 地區     | 台北市       |          台北市            |  台北市          |
| 職務類別  | 資訊系統管理類 |      資訊系統管理類        |   資訊系統管理類、金融研究員、統計精算人員、市場調查／市場分析         |
| 工作性質  |      全職      |       全職      |      全職      |

- 註：關鍵字的部分只搜尋職務名稱

---

## Web Crawler
從[104人力銀行](https://www.104.com.tw/jobs/main/)網站收集了關於資料科學、資料工程、資料分析的相關職缺資訊。在爬蟲的部分主要使用到[Requests](https://pypi.org/project/requests/)套件。

**1. 搜尋職缺、請求路徑與參數**
依照前述Search Condition條件進行職缺搜尋，從開發人員工具 > Network > Fetch/XHR，檢視動態載入方法的項目 > Headers 查看請求的方式與參數，相關參數如下：

```
Request URL：https://www.104.com.tw/jobs/search/list
Request Methon：GET
Headers Referer：https://www.104.com.tw/jobs/search/


Query String Parameters：

ro: 1
kwop: 1
keyword: python
expansionType: area,spec,com,job,wf,wktm
area: 6001001000
order: 1
asc: 0
page: 1
mode: s
jobsource: 2018indexpoc
```
其中幾個主要控制的篩選參數為area, jobcat, ro, kwop, keyword：

(1) area 地區：參考Area.json

(2) jobcat 職務類別：參考JobCat.json

(3) ro 工作性質：本項目僅搜尋「全職」類的職缺，ro=1

(4) kwop 搜尋關鍵字種類：1=關鍵字只搜尋職務名稱

(5) keyword 關鍵字：職缺關鍵字條件

**2. 取得職缺詳細資料**

由第一步獲取的職缺搜尋結果列表並未包含所有職缺的資訊，因此藉由職缺搜尋結果列表取得之各職缺的job_id作為參數傳入：
```
Request URL：https://www.104.com.tw/job/ajax/content/{job_id}
Request Methon：GET
Headers Referer：https://www.104.com.tw/job/{job_id}
```
**3. 資料結構**
從網頁上回傳的資料為[JSON](https://www.json.org/json-en.html)格式，利用[pandas](https://pandas.pydata.org/)將所爬取的職缺資料轉為DataFrame並輸出至Excel。

完整代碼請參考：job_market_search.py

## Data Clearning
**1. 剔除無關的職缺**

根據前述的Search Condition，雖然已經初步篩選出相關的職缺，不過部分職缺名稱仍與搜尋的職缺關鍵字不符，因此需要先將其排除(新增reject欄位，reject=N為最後要保留的職缺清單)。

經由Search Condition以及Data Clearning的職缺數統整如下：
|          | 資料科學家 | 資料工程師      | 資料分析師 |
| -------- | ---------- | ------------- | ---------- |
|  Search Condition筆數  |  484  | 774 |  769    |
|  Data Clearning後的筆數    | 249       |    505         |  497        |

完整代碼請參考：job_data_clean.py

**2. 相關欄位統計**

為了方便後續圖表統計，須先清理以下欄位:
(1) 科系 major
(2) 技能 skill
(3) 擅長工具 specialty
(4) 職務類別 jobCategory

完整代碼請參考：job_data_count.py

## Data Analysis & Visualization
最後將取得的職缺資料依照前面提到的問題，利用[matplotlib](https://matplotlib.org/)以及[seaborn](https://seaborn.pydata.org/#)套件進行視覺化呈現：（以下資料僅依照本項目的搜尋條件，於9月抓取的104職缺資料為樣本參考）

完整代碼請參考：job_data_visualization.py

1. 職缺分佈集中於哪些地區? (資料範圍為台北市12個行政區)

在台北12個行政區中，可以看出最多公司位於內湖區，而其它的如信義區、大安區、松山區、中山區也有許多職缺，士林區、萬華區、文山區則較少。
![](https://i.imgur.com/8RkyhAu.png)

2. 該領域需要的經驗水平為何?

若不考慮經驗不拘的選項，在該領域中較多雇主期望求職者有2~3年的相關經驗。
![](https://i.imgur.com/1bx7uVy.png)

3. 有哪些產業積極在該領域發展?
- 資料科學
![](https://i.imgur.com/arcuoq5.png)

- 資料工程
![](https://i.imgur.com/lAfbOCf.png)

- 資料分析
![](https://i.imgur.com/2XbGs3q.png)

4. 哪些科系是該領域所期望的?

以三類別的排名來看，皆以資訊工程與資訊管理居多，數理統計類的科系則次之。
- 資料科學
![](https://i.imgur.com/YGHrhas.png)

- 資料工程
![](https://i.imgur.com/76MaQkb.png)
- 資料分析
![](https://i.imgur.com/2KsAACy.png)
5. 該領域有哪些職務類別?

資料科學方面通常為軟體設計工程師以及演算法開發工程師；而資料工程則為軟體設計工程師、資料庫管理人員(DBA)；在資料分析領域的職務類別則較為廣泛，其中最多的為市場調查/市場分析以及系統分析師。
- 資料科學
![](https://i.imgur.com/3cYlgbX.png)

- 資料工程
![](https://i.imgur.com/YYgKuaX.png)
- 資料分析
![](https://i.imgur.com/FuTpZkb.png)
6. 招募公司最需要的技能與專長為何?

資料科學、資料工程、資料分析皆關注於利用資料解決問題或者是設計資料流程，而在技能與專長上各有其專注的部分。

資料科學主要技能為軟體程式設計，當然也少不了Machine Learning；資料工程則為資料庫系統管理維護與資料庫程式設計；資料分析最關注於市場調查資料分析與報告撰寫。

在程式語言的部分，皆以Python居冠；而在資料工程方面更多關於SQL技能以及ETL等大數據處理的相關技能；資料分析則較多關於如何視覺化呈現資料的技能，如Tableau、Power BI等。
- 資料科學
![](https://i.imgur.com/C2AVFIQ.png)
![](https://i.imgur.com/H4SfLsF.png)

- 資料工程
![](https://i.imgur.com/GXKFXQN.png)
![](https://i.imgur.com/1jhZfps.png)
- 資料分析
![](https://i.imgur.com/lLICK1s.png)
![](https://i.imgur.com/OpyQZQL.png)
