# 進入虛擬環境
# 安裝套件
```
pip install requests beautifulsoup4 mysql-connector-python
```

# 總共三個py檔案
## ppt_config.py
讓ptt_crawler.py引用
記錄所有目前蒐集到的PTT看版
因為爬蟲網址結構是
https://www.ptt.cc/bbs/{看板名稱}/search?page={頁數}&q={關鍵字}
故希望蒐集各看板
未來如果要新增比較方便

## ptt_db.py
讓ptt_crawler引用
連接資料庫相關
在第一次執行時要先
```
python ptt_db.py
```

## ptt_crawler.py
主要爬蟲程式
等資料庫準備好後執行
```
python ptt_crawler.py
```
