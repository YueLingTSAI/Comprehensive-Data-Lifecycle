# YouTube爬蟲資料夾內容

## 1. yt_api.py
主要爬蟲程式，同時會建立資料表和江爬取的資料彙整成csv檔案
以關鍵字的方式查詢所有關於 YouTube 上 CAMA 和 Lousa 的評論
特色是會檢視已存過的影片ID，避免重複爬取留言
```
python yt_api.py
```

# 執行步驟
## 1. 建立虛擬環境

## 2. 將以下物件新增至linux環境變數
### YouTube Data API v3
每天免費限額100個請求
https://console.cloud.google.com/
```
export YOUTUBE_API_KEYS='你的金鑰'
```

## 3. 安裝套件
```
pip3 install google-api-python-client sql alchemy pymysql python-dateutil langdetect
pip3 install mysql-connector-python
```

## 4. 執行爬蟲程式
```
python yt_api.py
```
