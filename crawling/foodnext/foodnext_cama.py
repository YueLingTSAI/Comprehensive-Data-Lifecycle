from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime
import pymysql
import time
import requests
import re

# 設置目標網址
TARGET_URL = "https://www.foodnext.net/search"

# 設定 Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 無頭模式（背景執行）
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--remote-debugging-port=9222")

# 啟動 WebDriver
service = Service()
driver = webdriver.Chrome(service=service, options=options)

# 定義分類規則
CLASSIFICATION_RULES = {
    "產品相關類": r"新品|推出|升級|新口感|全新|情人節|新上市",
    "行銷活動類": r"優惠|折扣|促銷|回饋|特價|半價|買一送一|限時|會員|送禮|禮盒|預購|聯名|合作|feat|聯合|攜手|異業結盟|策略聯盟|跨界",
    "品牌發展類": r"展店|加盟|拓點|新店|旗艦店|門市|分店|據點|開設|進駐|擴展|投資|併購|IPO|上市|櫃|股東|股價|公開發行",
    "市場趨勢類": r"市場|產業趨勢|市佔率|商機|成長|趨勢|未來展望|策略|品牌形象|消費行為|市場研究|評鑑|品牌競爭|品牌選擇",
    "品牌類": r"星巴克|伯朗|西雅圖|超商|成真咖啡|黑沃咖啡|Flash Coffee|怡客咖啡",
}

# 自動分類函數
def classify_article(title, content):
    for category, pattern in CLASSIFICATION_RULES.items():
        if re.search(pattern, title, re.IGNORECASE) or re.search(pattern, content, re.IGNORECASE):
            return category
    return "未分類"

# 轉換日期格式
def format_date(date_str):
    """自動偵測並轉換 `YYYY/MM/DD` 和 `YYYY-MM-DD` 格式"""
    try:
        if "/" in date_str:  # `2025/01/11`
            return datetime.strptime(date_str, "%Y/%m/%d").strftime("%Y-%m-%d")
        elif "-" in date_str:  # `2025-01-11`
            return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
        else:
            return None  # 不是預期格式時返回 None
    except ValueError:
        return None

# MySQL 連線函式
def connect_to_db():
    try:
        conn = pymysql.connect(
            host="請填入你的資料庫主機IP",
            user="請填入你的資料庫帳號",
            password="請填入你的資料庫密碼",
            db="請填入你的資料庫名稱",
            charset="utf8mb4"
        )
        return conn
    except pymysql.MySQLError as e:
        print(f"MySQL 連線錯誤: {e}")
        return None

# 初始化 MySQL 資料庫
def setup_database():
    try:
        conn = connect_to_db()
        if not conn:
            print("無法連接到資料庫")
            return
        
        cur = conn.cursor()
        # 創建資料表，確保 url 是唯一索引，防止重複儲存
        cur.execute("""
            CREATE TABLE IF NOT EXISTS foodnext_cama (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255),
                url VARCHAR(255) UNIQUE,  
                date DATE,
                content TEXT,
                classified VARCHAR(50)
            )
        """)
        conn.commit()
        conn.close()
        print("✅ 資料庫初始化完成")
    except pymysql.MySQLError as e:
        print(f"❌ 設定資料庫時發生錯誤: {e}")

# 插入文章資料（防止重複儲存）
def insert_article_data(data):
    conn = connect_to_db()
    if not conn:
        return
    
    cur = conn.cursor()
    try:
        for article in data:
            classified = classify_article(article['title'], " ".join(article['relevant_contents']))
            formatted_date = format_date(article['date'])
            if formatted_date is None:
                print(f"⚠️ 日期格式錯誤: {article['date']}，跳過此文章")
                continue
            sql = """
                INSERT INTO foodnext_cama (title, url, date, content, classified)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                title = VALUES(title),
                date = VALUES(date),
                content = VALUES(content),
                classified = VALUES(classified)
            """
            cur.execute(sql, (
                article['title'],
                article['url'],
                formatted_date,
                "\n".join(article['relevant_contents']),
                classified
            ))
        conn.commit()
        print(f"✅ 成功插入或更新 {len(data)} 篇文章至資料庫")
    except pymysql.MySQLError as e:
        print(f"❌ 插入資料時發生錯誤: {e}")
    finally:
        conn.close()

# 取得搜尋結果中的文章連結
def get_article_links():
    driver.get(TARGET_URL)
    print("✅ Loaded page: " + driver.title)

    search_box = driver.find_element(By.CLASS_NAME, 'form-control')
    search_box.clear()
    search_box.send_keys("cama")
    search_box.submit()
    print("🔍 搜尋成功")

    time.sleep(2)  # 等待搜尋結果載入
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all('div', class_='search-result')

    article_links = []
    for result in results:
        link_tag = result.find('a')
        if link_tag and link_tag['href']:
            link = link_tag['href']
            if not link.startswith("http"):
                link = "https://www.foodnext.net" + link
            article_links.append(link)

    print(f"📑 找到 {len(article_links)} 篇文章連結")
    return article_links

def clean_content(text):
    # 定義過濾的正則表達式
    patterns = [
        r'（?圖片來源[：:＝][^）]*）?',  # 匹配 (圖片來源：XXX) 或 圖片來源：XXX
        r'（?內容提供[：:＝][^）]*）?'  # 匹配 (內容提供：XXX) 或 內容提供：XXX
    ]
    
    for pattern in patterns:
        text = re.sub(pattern, '', text).strip()  # 使用正則表達式刪除匹配的內容

    return text


# 爬取文章內容並過濾延伸閱讀
def fetch_article_content(article_links):
    article_data = []

    for link in article_links:
        try:
            response = requests.get(link, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            title_tag = soup.find('h3', class_='font-alt mt0')
            title = title_tag.text.strip() if title_tag else "未找到標題"

            date_tag = soup.find('p', class_='date')
            if not date_tag:
                date_span = soup.select_one('p.nm span.date')
                date = date_span.get_text(strip=True) if date_span else "未找到日期"
            else:
                date = date_tag.get_text(strip=True)

            formatted_date = format_date(date) if date else None
            if formatted_date is None:
                print(f"⚠️ 日期格式錯誤: {date}，跳過此文章")
                continue  # 直接跳過這篇文章

            content_div = soup.find('div', class_='post-content')
            relevant_paragraphs = []
            if content_div:
                paragraphs = content_div.find_all('p')
                for paragraph in paragraphs:
                    text = paragraph.text.strip()
                    text = clean_content(text)
                    if "cama" in text.lower() and "▶" not in text and "延伸閱讀" not in text:
                        relevant_paragraphs.append(text)

            if relevant_paragraphs:
                article_data.append({
                    "url": link,
                    "title": title,
                    "date": formatted_date,
                    "relevant_contents": relevant_paragraphs
                })
                print(f"📝 找到相關內容於 {link}")
                print(f"📅 日期: {date}")

        except requests.exceptions.RequestException as e:
            print(f"❌ 爬取 {link} 時發生錯誤: {e}")

    return article_data

# 主程式
try:
    setup_database()  # 初始化資料庫
    article_links = get_article_links()  # 取得文章連結
    article_data = fetch_article_content(article_links)  # 爬取內容
    insert_article_data(article_data)  # 儲存至 MySQL
    print("✅ 所有資料已成功保存")
except Exception as e:
    print(f"❌ 發生錯誤: {e}")
finally:
    driver.quit()
