import pymysql
import os
from dotenv import load_dotenv

def connect_db():
    """建立資料庫連線"""
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_NAME")
    )

def check_duplicate(cur, store_name, rating, content):
    """檢查評論是否已存在，使用店名、評分和評論內容作為條件"""
    sql = """
        SELECT COUNT(*) 
        FROM google_map 
        WHERE store_name = %s 
        AND rating = %s
        AND content = %s
    """
    cur.execute(sql, (store_name, rating, content))
    count = cur.fetchone()[0]
    return count > 0

def insert_data(reviews):
    """將評論資料插入資料庫"""
    if not reviews:
        print("沒有評論資料要儲存")
        return
        
    conn = connect_db()
    cur = conn.cursor()
    
    try:
        # 建立資料表（如果不存在）
        cur.execute("""
            CREATE TABLE IF NOT EXISTS google_map (
                id INT AUTO_INCREMENT PRIMARY KEY,
                brand VARCHAR(10),
                store_name VARCHAR(50),
                rating TINYINT,
                content TEXT NOT NULL DEFAULT '',
                content_time VARCHAR(50),
                crawling_time DATETIME
            )
        """)
        
        # 插入評論資料
        success_count = 0
        duplicate_count = 0
        empty_count = 0
        
        for review in reviews:
            # 確保 content 不是 None
            review['content'] = review['content'].strip() if review['content'] else ''
            
            try:
                # 使用店名、評分和評論內容來檢查重複
                if check_duplicate(cur, 
                                 review['store_name'], 
                                 review['rating'],
                                 review['content']):
                    duplicate_count += 1
                    continue
                    
                sql = """
                    INSERT INTO google_map 
                    (brand, store_name, rating, content, content_time, crawling_time)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cur.execute(sql, (
                    review['brand'],
                    review['store_name'],
                    review['rating'],
                    review['content'],
                    review['content_time'],
                    review['crawling_time']
                ))
                success_count += 1
                if not review['content']:
                    empty_count += 1
                
            except Exception as e:
                print(f"插入單筆評論時發生錯誤: {str(e)}")
                continue
        
        conn.commit()
        print(f"\n已成功儲存 {success_count} 則評論到資料庫")
        print(f"偵測到 {duplicate_count} 則重複評論")
        
    except Exception as e:
        print(f"資料庫操作時發生錯誤: {str(e)}")
        conn.rollback()
        
    finally:
        cur.close()
        conn.close()