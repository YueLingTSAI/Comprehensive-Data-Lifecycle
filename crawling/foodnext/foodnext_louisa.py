from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pymysql
import time
import requests

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

# MySQL 連線函式
def connect_to_db():
    try:
        conn = pymysql.connect(
            host="labdb.coded2.fun",
            user="sophia",
            password="123456dv107",
            db="SOPHIA",
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
            CREATE TABLE IF NOT EXISTS foodnext_louisa (
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255),
                url VARCHAR(255) UNIQUE,  
                date VARCHAR(255),
                content TEXT
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
            sql = """
                INSERT INTO foodnext_louisa (title, url, date, content)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                title = VALUES(title),
                date = VALUES(date),
                content = VALUES(content)
            """
            cur.execute(sql, (
                article['title'],
                article['url'],
                article['date'],
                "\n".join(article['relevant_contents'])
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
    search_box.send_keys("路易莎")
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

            content_div = soup.find('div', class_='post-content')
            relevant_paragraphs = []
            if content_div:
                paragraphs = content_div.find_all('p')
                for paragraph in paragraphs:
                    text = paragraph.text.strip()
                    if "路易莎" in text and "▶" not in text and "延伸閱讀" not in text:
                        relevant_paragraphs.append(text)

            if relevant_paragraphs:
                article_data.append({
                    "url": link,
                    "title": title,
                    "date": date,
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
