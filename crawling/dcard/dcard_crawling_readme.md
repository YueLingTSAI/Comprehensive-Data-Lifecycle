# DCARD爬蟲資料夾內容
總共兩個py檔案

## 1. db_config.py
第一次執行爬蟲前請執行下述指令
以創建資料表
```
python db_config.py
```

## 2. dcard_crawler.py
主要爬蟲程式
目前設定爬取進五年內
於google自訂化搜尋引擎中
有關DCARD查詢路易莎及CAMA的搜尋結果

它的特性是
會跟著日期變動
而變動搜尋結果順序及查詢到的資料深度
故可以定期去改便日期參數(詳見程式碼中d1825天的設定)

# 執行步驟
## 1. 建立虛擬環境

## 2. 將以下兩個物件新增至linux環境變數
### google custom api
每天每費限額100個請求
https://console.cloud.google.com/
```
export GOOGLE_API_KEY='你的金鑰'
```
### google自訂化搜尋引擎
建好之後找到自己的搜尋引擎ID
https://programmablesearchengine.google.com/controlpanel/all?hl=zh-tw

```
export GOOGLE_SEARCH_ENGINE_ID='你的ID'
```

## 3. 安裝套件
```
pip install requests pandas python-dotenv sqlalchemy pymysql
pip install mysql-connector-python
```

## 4. 執行爬蟲程式
```
python dcard_crawler.py
```
