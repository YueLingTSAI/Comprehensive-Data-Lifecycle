import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

class DatabaseConfig:
    def __init__(self):
        # MariaDB 連接設定
        self.host = os.getenv("DB_HOST")
        self.port = 3306
        self.database = os.getenv("DB_NAME")
        self.username = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
    
    def get_connection(self):
        """建立資料庫連接"""
        return mysql.connector.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.username,
            password=self.password
        )

    def get_engine(self):
        """建立 SQLAlchemy engine"""
        conn_str = (
            f"mysql+mysqlconnector://{self.username}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
        )
        return create_engine(conn_str)

    def read_table_to_df(self, table_name, schema=None):
        """從資料庫讀取資料表到DataFrame"""
        engine = self.get_engine()
        if schema:
            query = f"SELECT * FROM {schema}.{table_name}"
        else:
            query = f"SELECT * FROM {table_name}"
        return pd.read_sql(query, engine)

    def write_df_to_table(self, df, table_name, schema='CLEAN_SOPHIA', if_exists='replace'):
        """將DataFrame寫入資料庫"""
        # 在 MariaDB 中，schema 就是 database
        # 確保 schema 存在
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # 創建 schema（如果不存在）
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {schema}")
            conn.commit()
            
            # 切換到指定的 schema
            cursor.execute(f"USE {schema}")
            conn.commit()
            
            # 使用 SQLAlchemy 寫入資料
            engine = create_engine(
                f"mysql+mysqlconnector://{self.username}:{self.password}"
                f"@{self.host}:{self.port}/{schema}"
            )
            
            df.to_sql(
                name=table_name,
                con=engine,
                if_exists=if_exists,
                index=False
            )
            print(f"資料已成功寫入 {schema}.{table_name}")
            
        except Exception as e:
            print(f"寫入資料時發生錯誤：{e}")
            raise
        finally:
            cursor.close()
            conn.close()

    def execute_query(self, query):
        """執行SQL查詢"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
        finally:
            cursor.close()
            conn.close()