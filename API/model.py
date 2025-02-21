from sqlalchemy import Column, Integer
from sqlalchemy.dialects.mysql import VARCHAR, TEXT, DATETIME, ENUM, DOUBLE, FLOAT
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Google_map1(db.Model):
    __tablename__ = 'google_map'  # 現有的資料表名稱完全一致
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    brand = Column(TEXT, nullable=True)
    store_name = Column(TEXT, nullable=True)
    rating = Column(Integer, nullable=True)
    content = Column(TEXT, nullable=True)
    content_time = Column(TEXT, nullable=True)
    crawling_time = Column(DATETIME, nullable=True)
    region = Column(TEXT, nullable=True)

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }


class Google_map2(db.Model):
    __tablename__ = 'google_map_rating_count'  # 現有的資料表名稱完全一致
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    region = Column(TEXT, nullable=True)
    brand = Column(TEXT, nullable=True)
    rating = Column(Integer, nullable=True)
    count = Column(Integer, nullable=True)

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }


class Google_map3(db.Model):
    __tablename__ = 'google_map_statistics'  # 現有的資料表名稱完全一致
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    region = Column(TEXT, nullable=True)
    brand = Column(TEXT, nullable=True)
    rating_count = Column(Integer, nullable=True)
    rating_mean = Column(DOUBLE, nullable=True)
    rating_min = Column(Integer, nullable=True)
    rating_max = Column(Integer, nullable=True)

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }


class Google_map4(db.Model):
    __tablename__ = 'google_map_store_region'  # 現有的資料表名稱完全一致
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    shop = Column(TEXT, primary_key=True, autoincrement=True)
    region = Column(TEXT, nullable=True)
    brand = Column(TEXT, nullable=True)

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }


class Foodnext_cama(db.Model):
    __tablename__ = 'foodnext_article_cama'  # 現有的資料表名稱完全一致
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(255), nullable=True)
    url = Column(VARCHAR(255), nullable=True)
    date = Column(VARCHAR(255), nullable=True)
    content = Column(TEXT, nullable=True)
    classified = Column(VARCHAR(255), nullable=True)

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }


class Foodnext_louisa(db.Model):
    __tablename__ = 'foodnext_article_louisa'  # 現有的資料表名稱完全一致

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(255), nullable=True)
    url = Column(VARCHAR(255), nullable=True)
    date = Column(VARCHAR(255), nullable=True)
    content = Column(TEXT, nullable=True)
    classified = Column(VARCHAR(255), nullable=True)

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }


class Youtube_cama(db.Model):
    __tablename__ = 'youtube_comments_cama'  # 現有的資料表名稱完全一致
    id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(TEXT, nullable=True)
    content = Column(TEXT, nullable=True)
    author = Column(TEXT, nullable=True)
    like_count = Column(Integer, nullable=True)
    created_at = Column(DATETIME, nullable=True)
    likes = Column(Integer, nullable=True)
    timestamp = Column(DATETIME, nullable=True)
    brand = Column(TEXT, nullable=True)
    sentiment = Column(TEXT, nullable=True)
    sentiment_score = Column(Integer, nullable=True)
    topic = Column(TEXT, nullable=True)
    
    
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }


class Youtube_louisa(db.Model):
    __tablename__ = 'youtube_comments_louisa'  # 現有的資料表名稱完全一致
    id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(TEXT, nullable=True)
    content = Column(TEXT, nullable=True)
    author = Column(TEXT, nullable=True)
    like_count = Column(Integer, nullable=True)
    created_at = Column(DATETIME, nullable=True)
    likes = Column(Integer, nullable=True)
    timestamp = Column(DATETIME, nullable=True)
    brand = Column(TEXT, nullable=True)
    sentiment = Column(TEXT, nullable=True)
    sentiment_score = Column(Integer, nullable=True)
    topic = Column(TEXT, nullable=True)
    
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }


class Dcard(db.Model):
    __tablename__ = 'dcard'  # 現有的資料表名稱完全一致
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cafe = Column(VARCHAR(50), nullable=True)
    title = Column(VARCHAR(255), nullable=True)
    link = Column(VARCHAR(512), nullable=True)
    content = Column(VARCHAR(2000), nullable=True)
    source = Column(VARCHAR(50), nullable=True)
    search_date = Column(DATETIME, nullable=True)
    sentiment = Column(VARCHAR(20), nullable=True)
    sentiment_score = Column(FLOAT, nullable=True)
    post_date = Column(DATETIME, nullable=True)
    board = Column(VARCHAR(20), nullable=True)
    topic = Column(VARCHAR(100), nullable=True)

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8mb4',
        'mysql_collate': 'utf8mb4_unicode_ci'
    }


class Ptt(db.Model):
    __tablename__ = 'ptt'  # 現有的資料表名稱完全一致
    
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

