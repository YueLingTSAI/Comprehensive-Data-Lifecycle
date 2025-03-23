# PTT爬蟲資料夾內容
總共三個py檔案

## 1. ppt_config.py
讓ptt_crawler.py引用
會記錄所有目前蒐集到的PTT看版
因為爬蟲網址結構是
https://www.ptt.cc/bbs/{看板名稱}/search?page={頁數}&q={關鍵字}
未來如果要再擴增看板數量比較方便

## 2. ptt_db.py
讓ptt_crawler引用
第一次執行爬蟲前請執行下述指令
以連接資料庫相關設定
```
python ptt_db.py
```

## 3. ptt_crawler.py
主要爬蟲程式


# 執行步驟
## 1. 進入虛擬環境
## 2. 安裝套件
```
pip install requests beautifulsoup4 mysql-connector-python
```

## 3. 執行爬蟲程式
等資料庫準備好後執行
```
python ptt_crawler.py
```
