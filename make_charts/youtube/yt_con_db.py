import mysql.connector
import pandas as pd

class DatabaseConfig:
    def __init__(self):
        self.host = '請填入你的資料庫主機IP' 
        self.port = 預設端口
        self.database = '請填入你的資料庫名稱'
        self.username = '請填入你的資料庫帳號'
        self.password = '請填入你的資料庫密碼'

    def get_connection(self):
        """ 建立資料庫連線 """
        return mysql.connector.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.username,
            password=self.password
        )

    def read_table_to_df(self, table_name):
        """ 讀取資料表並返回 DataFrame """
        conn = None
        try:
            conn = self.get_connection()
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql(query, conn)
            return df
        except Exception as e:
            print(f"❌ 無法讀取資料表 {table_name}: {e}")
            return pd.DataFrame()  # 回傳空的 DataFrame
        finally:
            if conn:
                conn.close()  # 確保連線關閉
