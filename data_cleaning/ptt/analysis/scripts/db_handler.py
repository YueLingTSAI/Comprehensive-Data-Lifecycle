import mysql.connector
from mysql.connector import Error
import configparser
import logging
from typing import Dict, Any, List, Tuple

class DatabaseHandler:
    def __init__(self, config_path: str):
        self.config = self._read_config(config_path)
        self.logger = logging.getLogger(__name__)

    def _read_config(self, config_path: str) -> Dict[str, Any]:
        config = configparser.ConfigParser()
        config.read(config_path)
        return dict(config['database'])

    def get_connection(self):
        try:
            return mysql.connector.connect(
                host=self.config['host'],
                port=int(self.config['port']),
                database=self.config['database'],
                user=self.config['user'],
                password=self.config['password']
            )
        except Error as e:
            self.logger.error(f"Database connection error: {str(e)}")
            raise

    def add_new_columns(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # 新增或修改所需欄位
            alter_queries = [
                "ALTER TABLE ptt_2 ADD COLUMN IF NOT EXISTS sentiment VARCHAR(20)",
                "ALTER TABLE ptt_2 ADD COLUMN IF NOT EXISTS sentiment_score INT",
                "ALTER TABLE ptt_2 ADD COLUMN IF NOT EXISTS topic VARCHAR(500)"
            ]

            for query in alter_queries:
                try:
                    cursor.execute(query)
                except Error as e:
                    if e.errno != 1060:  # 如果錯誤不是「欄位已存在」，則拋出異常
                        raise

            conn.commit()
            self.logger.info("Table columns verified and updated if necessary")

        except Error as e:
            self.logger.error(f"Error modifying columns: {str(e)}")
            raise
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def get_unprocessed_records(self, limit=None) -> List[Dict]:
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT id, keyword, article_title, content_text 
                FROM ptt_2 
                WHERE sentiment IS NULL
            """
            
            if limit:
                query += " LIMIT %s"
                cursor.execute(query, (limit,))
            else:
                cursor.execute(query)
                
            return cursor.fetchall()
            
        except Error as e:
            self.logger.error(f"Error fetching records: {str(e)}")
            raise
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def update_record(self, id: int, sentiment: str, score: int, topic: str):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            update_query = """
                UPDATE ptt_2 
                SET sentiment = %s,
                    sentiment_score = %s,
                    topic = %s
                WHERE id = %s
            """
            
            cursor.execute(update_query, (sentiment, score, topic, id))
            conn.commit()
            
        except Error as e:
            self.logger.error(f"Error updating record {id}: {str(e)}")
            raise
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
                
    def batch_update_records(self, updates: List[Tuple[str, int, str, int]]):
        """批量更新記錄"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            update_query = """
                UPDATE ptt_2 
                SET sentiment = %s,
                    sentiment_score = %s,
                    topic = %s
                WHERE id = %s
            """
            
            # 確保參數順序與查詢相符
            formatted_updates = [(sentiment, score, topic, id) for id, sentiment, score, topic in updates]
            
            cursor.executemany(update_query, formatted_updates)
            conn.commit()
            
            updated_rows = cursor.rowcount
            self.logger.info(f"成功更新 {updated_rows} 筆資料")
            
            return updated_rows
            
        except Error as e:
            self.logger.error(f"Error batch updating records: {str(e)}")
            raise
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()