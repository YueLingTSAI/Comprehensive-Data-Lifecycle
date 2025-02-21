import mysql.connector
from mysql.connector import Error
import configparser
import logging
from typing import Dict, Any, List


class DatabaseHandler:
    def __init__(self, config_path: str):
        self.config = self._read_config(config_path)
        self.logger = logging.getLogger(__name__)

    def _read_config(self, config_path: str) -> Dict[str, Any]:
        config = configparser.ConfigParser()
        config.read(config_path)
        return dict(config["database"])

    def get_connection(self):
        try:
            return mysql.connector.connect(
                host=self.config["host"],
                port=int(self.config["port"]),
                database=self.config["database"],
                user=self.config["user"],
                password=self.config["password"],
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
                "ALTER TABLE dcard_2 MODIFY COLUMN sentiment VARCHAR(20)",
                "ALTER TABLE dcard_2 MODIFY COLUMN sentiment_score INT",
                "ALTER TABLE dcard_2 MODIFY COLUMN topic VARCHAR(100)",
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
                SELECT id, cafe, title, content 
                FROM dcard_2 
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
                UPDATE dcard_2 
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
