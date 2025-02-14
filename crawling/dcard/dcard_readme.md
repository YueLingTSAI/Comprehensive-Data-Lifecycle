# 建立虛擬環境

# 放入環境變數
## 啟用google custom api
每天每費限額100個請求
https://console.cloud.google.com/
```
export GOOGLE_API_KEY='你的金鑰'
```
## 建立一個google自訂化搜尋引擎
建好之後找到搜尋引擎ID
https://programmablesearchengine.google.com/controlpanel/all?hl=zh-tw

```
export GOOGLE_SEARCH_ENGINE_ID='你的ID'
```
# 安裝套件
```
pip install requests pandas python-dotenv sqlalchemy pymysql

pip install mysql-connector-python
```

# 總共兩個py檔案
## db_config.py
第一次執行以創建資料表
```
python db_config.py
```

## dcard_crawler.py
主要執行爬蟲
目前設定五年內
因為google自訂化搜尋引擎會跟著日期變動而變動搜尋結果順序
亦即會影響查詢到的資料深度
故可以定期改變天數設定(詳見程式碼中d1825天的設定)

```
python dcard_crawler.py
```
