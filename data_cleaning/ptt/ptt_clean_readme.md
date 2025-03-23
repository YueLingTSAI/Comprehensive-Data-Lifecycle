# PTT清洗程式資料夾內容

## 目錄結構

ptt
│── analysis
│   │── config
│   │   │── database.ini
│   │   │── gcp_key.json
│   │── scripts
│   │   │── __init__.py
│   │   │── db_handler.py
│   │   │── sentiment_analyzer.py
│   │   │── text_processor.py
│   │   │── topic_classifier.py
│   │   │── vectorizer.py
│   │── main.py
│── ptt_clean_readme.md

## 目錄說明

### config/：儲存設定檔

database.ini：資料庫連線設定

gcp_key.json：Google Cloud API 金鑰

### scripts/：包含各種 Python 腳本

__init__.py：初始化模組

db_handler.py：資料庫處理

sentiment_analyzer.py：情感分析

text_processor.py：文本處理

topic_classifier.py：主題分類

vectorizer.py：向量化文本

### main.py
主程式

### ptt_clean_readme.md
清洗說明文件