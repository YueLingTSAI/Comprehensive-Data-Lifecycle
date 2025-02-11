import mysql.connector
from datetime import datetime
from typing import Optional

# 資料庫連線設定
DATABASE_CONFIG = {
    "user": "sophia",
    "password": "123456dv107",
    "host": "labdb.coded2.fun",
    "database": "SOPHIA",
}


def create_connection():
    """建立資料庫連線"""
    try:
        return mysql.connector.connect(**DATABASE_CONFIG)
    except mysql.connector.Error as err:
        print(f"無法連接到資料庫: {err}")
        return None


def create_tables():
    """建立必要的資料表"""
    connection = create_connection()
    if not connection:
        return

    try:
        cursor = connection.cursor()

        # 建立 ptt_crawled_pages 資料表
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ptt_crawled_pages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                page_url VARCHAR(255) NOT NULL COMMENT '頁面URL',
                crawl_time DATETIME NOT NULL COMMENT '爬取時間',
                UNIQUE INDEX idx_page_url (page_url)
            ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
        """
        )

        # 建立 ptt 資料表
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ptt (
                id INT AUTO_INCREMENT PRIMARY KEY,
                keyword VARCHAR(255) NOT NULL COMMENT '關鍵字',
                article_title TEXT NOT NULL COMMENT '文章標題',
                content_text TEXT NOT NULL COMMENT '擷取的內文或留言',
                content_type ENUM('article', 'comment') NOT NULL COMMENT '內容類型',
                post_time DATETIME COMMENT '發文日期',
                crawl_time DATETIME COMMENT '爬蟲日期',
                article_url VARCHAR(255) NOT NULL COMMENT '文章URL',
                comment_author VARCHAR(255) DEFAULT NULL COMMENT '留言作者',
                INDEX idx_keyword (keyword),
                INDEX idx_post_time (post_time),
                INDEX idx_crawl_time (crawl_time),
                INDEX idx_content_type (content_type),
                INDEX idx_article_url (article_url)
            ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci
        """
        )

        connection.commit()
        print("資料表建立成功")

    except mysql.connector.Error as err:
        print(f"建立資料表時發生錯誤: {err}")
    finally:
        if "cursor" in locals():
            cursor.close()
        connection.close()


def store_mention(
    keyword: str,
    article_title: str,
    content_text: str,
    content_type: str,
    post_time: datetime,
    article_url: str,
    comment_author: Optional[str] = None,
):
    """儲存提及到資料庫"""
    connection = create_connection()
    if not connection:
        return

    try:
        cursor = connection.cursor()

        # 檢查是否已經存在相同的文章 URL 和內容類型
        check_sql = """
        SELECT id FROM ptt 
        WHERE article_url = %s 
        AND content_type = %s
        AND content_text = %s
        """
        cursor.execute(check_sql, (article_url, content_type, content_text))
        if cursor.fetchone():
            print(f"跳過重複內容: {article_title}")
            return

        # 插入新記錄
        sql = """
        INSERT INTO ptt 
        (keyword, article_title, content_text, content_type, post_time, crawl_time, article_url, comment_author)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        data = (
            keyword,
            article_title,
            content_text,
            content_type,
            post_time,
            datetime.now(),
            article_url,
            comment_author,
        )

        cursor.execute(sql, data)
        connection.commit()
        print(f"成功儲存 {content_type}: {article_title[:50]}...")

    except mysql.connector.Error as err:
        print(f"儲存資料時發生錯誤: {err}")
        if connection:
            connection.rollback()
    finally:
        if "cursor" in locals():
            cursor.close()
        connection.close()


def store_crawled_page(page_url: str):
    """記錄已爬取的頁面"""
    connection = create_connection()
    if not connection:
        return

    try:
        cursor = connection.cursor()

        sql = """
        INSERT IGNORE INTO ptt_crawled_pages (page_url, crawl_time)
        VALUES (%s, %s)
        """

        cursor.execute(sql, (page_url, datetime.now()))
        connection.commit()

    except mysql.connector.Error as err:
        print(f"儲存爬取紀錄時發生錯誤: {err}")
        if connection:
            connection.rollback()
    finally:
        if "cursor" in locals():
            cursor.close()
        connection.close()


def is_url_crawled(url: str) -> bool:
    """檢查 URL 是否已經爬取過"""
    connection = create_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1 FROM ptt_crawled_pages WHERE page_url = %s", (url,))
        return cursor.fetchone() is not None

    except mysql.connector.Error as err:
        print(f"檢查 URL 時發生錯誤: {err}")
        return False
    finally:
        if "cursor" in locals():
            cursor.close()
        connection.close()


def main():
    create_tables()
    print("資料庫初始化完成")


if __name__ == "__main__":
    main()