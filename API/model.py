from sqlalchemy import Column, Integer
from sqlalchemy.dialects.mysql import VARCHAR, TEXT, DATETIME, ENUM
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Dcard(db.Model):
    __tablename__ = 'dcard'  # 確保這裡的名稱與你現有的資料表名稱完全一致
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cafe = Column(VARCHAR(50), nullable=True)
    title = Column(VARCHAR(255), nullable=True)
    link = Column(VARCHAR(512), nullable=True)
    content = Column(VARCHAR(2000), nullable=True)
    source = Column(VARCHAR(50), nullable=True)
    search_date = Column(DATETIME, nullable=True)

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }

class Foodnext_cama(db.Model):
    __tablename__ = 'foodnext_cama'  # 確保這裡的名稱與你現有的資料表名稱完全一致
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(255), nullable=True)
    url = Column(VARCHAR(255), nullable=True)
    date = Column(VARCHAR(255), nullable=True)
    content = Column(TEXT, nullable=True)

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }

class Foodnext_louisa(db.Model):
    __tablename__ = 'foodnext_louisa'  # 確保這裡的名稱與你現有的資料表名稱完全一致
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(255), nullable=True)
    url = Column(VARCHAR(255), nullable=True)
    date = Column(VARCHAR(255), nullable=True)
    content = Column(TEXT, nullable=True)

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }

class Google_map(db.Model):
    __tablename__ = 'google_map'  # 確保這裡的名稱與你現有的資料表名稱完全一致
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    brand = Column(VARCHAR(10), nullable=True)
    store_name = Column(VARCHAR(30), nullable=True)
    rating = Column(Integer, nullable=True)
    content = Column(TEXT, nullable=True)

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }

class Ptt(db.Model):
    __tablename__ = 'ptt'  # 確保這裡的名稱與你現有的資料表名稱完全一致
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    keyword = Column(VARCHAR(255), nullable=True)
    article_title = Column(TEXT, nullable=True)
    content_text = Column(TEXT, nullable=True)
    content_type = Column(ENUM('article','comment'), nullable=True)
    post_time = Column(DATETIME, nullable=True)
    crawl_time = Column(DATETIME, nullable=True)
    article_url = Column(VARCHAR(255), nullable=True)
    comment_author = Column(VARCHAR(255), nullable=True)

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }

class Youtube_cama(db.Model):
    __tablename__ = 'youtube_cama'  # 確保這裡的名稱與你現有的資料表名稱完全一致
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(VARCHAR(50), nullable=True)
    content = Column(TEXT, nullable=True)
    author = Column(VARCHAR(255), nullable=True)
    like_count = Column(Integer, nullable=True)
    created_at = Column(DATETIME, nullable=True)
    
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }

class Youtube_louisa(db.Model):
    __tablename__ = 'youtube_louisa'  # 確保這裡的名稱與你現有的資料表名稱完全一致
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(VARCHAR(50), nullable=True)
    content = Column(TEXT, nullable=True)
    author = Column(VARCHAR(255), nullable=True)
    like_count = Column(Integer, nullable=True)
    created_at = Column(DATETIME, nullable=True)
    
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }