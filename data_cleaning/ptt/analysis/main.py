import os
import logging
import time
from scripts.vectorizer import TextVectorizer
from scripts.db_handler import DatabaseHandler

# 設定區塊
TEST_MODE = False  # 控制是否為測試模式
TEST_RECORDS = 5   # 測試模式時要處理的筆數
BATCH_SIZE = 100   # 批量處理的記錄數量

# 設定 GCP 認證
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    "/home/joelle/ptt/analysis/config/gcp_key.json"
)

# 設定日誌
logging.basicConfig(
    filename="/home/joelle/ptt/analysis/logs/analysis.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# 在 main.py 最開始加入測試代碼
def test_db_connection():
    try:
        db_handler = DatabaseHandler('/home/joelle/ptt/analysis/config/database.ini')
        conn = db_handler.get_connection()
        if conn.is_connected():
            print("資料庫連接正常")
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM ptt_2")
            result = cursor.fetchone()
            print(f"ptt_2 表格中有 {result[0]} 筆資料")
        conn.close()
    except Exception as e:
        print(f"資料庫連接測試失敗: {str(e)}")

test_db_connection()


def main():
    start_time = time.time()
    try:
        db_handler = DatabaseHandler('/home/joelle/ptt/analysis/config/database.ini')
        vectorizer = TextVectorizer()

        # 新增需要的欄位
        db_handler.add_new_columns()

        # 根據測試模式決定要處理的記錄數
        records = db_handler.get_unprocessed_records(limit=TEST_RECORDS if TEST_MODE else None)
        
        if not records:
            print("沒有未處理的記錄")
            return
            
        print(f"開始處理 {len(records)} 筆資料")
        
        # 步驟 1: 批量向量化文本
        print("步驟 1: 正在向量化文本...")
        vectorized_records = vectorizer.batch_vectorize(records, batch_size=BATCH_SIZE)
        
        # 步驟 2: 計算結果
        print("步驟 2: 正在計算結果...")
        results = vectorizer.calculate_results(vectorized_records)
        
        if TEST_MODE:
            for id, sentiment, score, topic in results:
                print(f"\n處理 ID {id}:")
                print(f"- 情感: {sentiment}")
                print(f"- 分數: {score}")
                print(f"- 主題: {topic}")
        
        # 步驟 3: 更新資料庫 - 使用單條更新而非批量更新
        print("步驟 3: 正在更新資料庫...")
        # commented out: updated = db_handler.batch_update_records(results)
        
        # 使用單條更新
        success_count = 0
        for id, sentiment, score, topic in results:
            try:
                db_handler.update_record(id, sentiment, score, topic)
                print(f"成功更新ID: {id}")
                success_count += 1
            except Exception as e:
                print(f"更新ID {id} 時出錯: {str(e)}")
        
        elapsed_time = time.time() - start_time
        print(f"\n分析完成！總共處理 {len(records)} 筆資料，成功更新 {success_count} 筆記錄，耗時 {elapsed_time:.2f} 秒")

    except Exception as e:
        error_msg = f"主程序錯誤: {str(e)}"
        print(error_msg)
        logging.error(error_msg)
        
    elapsed_time = time.time() - start_time
    print(f"總執行時間: {elapsed_time:.2f} 秒")

if __name__ == "__main__":
    main()