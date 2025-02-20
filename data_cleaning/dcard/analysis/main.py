import os
import logging
from scripts.analyzer import ContentAnalyzer
from scripts.db_handler import DatabaseHandler

# 設定區塊
TEST_MODE = False  # 控制是否為測試模式(False是正式模式,True是測試模式)
TEST_RECORDS = 5  # 測試模式時要處理的筆數

# 設定 GCP 認證
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    "/home/joelle/dcard/analysis/config/gcp_key.json"
)

# 設定日誌
logging.basicConfig(
    filename="/home/joelle/dcard/analysis/logs/analysis.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def main():
    try:
        db_handler = DatabaseHandler("/home/joelle/dcard/analysis/config/database.ini")
        analyzer = ContentAnalyzer()

        # 新增需要的欄位
        db_handler.add_new_columns()

        # 根據測試模式決定要處理的記錄數
        records = db_handler.get_unprocessed_records(
            limit=TEST_RECORDS if TEST_MODE else None
        )

        print(f"開始處理 {len(records)} 筆資料")
        processed_count = 0

        for record in records:
            try:
                if TEST_MODE:
                    print(f"\n處理 ID {record['id']} 的資料:")
                    print(f"咖啡店: {record['cafe']}")
                    print(f"標題: {record['title']}")
                    print(f"內容: {record['content'][:100]}...")

                # 結合 cafe、title 和 content 進行情感分析
                sentiment, score = analyzer.analyze_sentiment(
                    record["cafe"], record["title"], record["content"]
                )

                # 同樣結合 cafe、title 和 content 進行主題分類
                combined_text = (
                    f"{record['cafe']} {record['title']} {record['content']}"
                )
                topic = analyzer.classify_topic(combined_text)

                if TEST_MODE:
                    print(f"分析結果:")
                    print(f"- 情感: {sentiment}")
                    print(f"- 分數: {score}")
                    print(f"- 主題: {topic}")

                db_handler.update_record(record["id"], sentiment, score, topic)

                processed_count += 1
                if not TEST_MODE and processed_count % 100 == 0:
                    print(f"已處理 {processed_count} 筆資料")

            except Exception as e:
                error_msg = f"處理記錄 {record['id']} 時發生錯誤: {str(e)}"
                print(error_msg)
                logging.error(error_msg)
                continue

        print(f"\n分析完成！總共處理 {processed_count} 筆資料")

    except Exception as e:
        error_msg = f"主程序錯誤: {str(e)}"
        print(error_msg)
        logging.error(error_msg)


if __name__ == "__main__":
    main()
