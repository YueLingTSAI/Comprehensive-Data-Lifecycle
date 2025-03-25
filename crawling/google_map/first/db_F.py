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
        for review in reviews:
            # 確保 content 不是 None，如果是空值就設為空字串
            review['content'] = review['content'].strip() if review['content'] else ''
                
            try:
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
            except Exception as e:
                print(f"插入單筆評論時發生錯誤: {str(e)}")
                continue
        
        conn.commit()
        print(f"已成功儲存 {success_count} 則評論到資料庫（共 {len(reviews)} 則）")
        
    except Exception as e:
        print(f"資料庫操作時發生錯誤: {str(e)}")
        conn.rollback()
        
    finally:
        cur.close()
        conn.close()