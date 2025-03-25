# Google_map爬蟲

主要檔案：
1. **first**
2. **second**
3. data

## First檔案
執行第一次google_map評論爬蟲，滾動載入10次，抓取資料。

Code：
```bash=
# 爬蟲程式
googlemap_crawling_F.py

# 資料庫連接
db_F.py
```

## Second檔案
重複執行google_map評論爬蟲，滾動載入1次，只抓取最新資料。
在存入資料庫前，會先進行檢測，如有重複則不儲存。

Code：
```bash=
# 爬蟲程式
googlemap_crawling_S.py

# 資料庫連接
db_S.py
```

## data檔案
從Cama、Louisa官網上隨機挑選50家店面彙整成Csv檔，使爬蟲程式根據指定店家進行資料爬取。

（檔案需與爬蟲程式放在一起）
```bash=
Cama.csv
Louisa.csv
```