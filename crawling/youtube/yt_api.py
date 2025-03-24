from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import time
import re
import csv
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
from dateutil.parser import parse

# 從環境變數中讀取多個 API Key
API_KEYS = os.getenv("YOUTUBE_API_KEYS", "").split(",")
API_KEYS = [key.strip() for key in API_KEYS if key.strip()]
current_key_index = 0

# 設定 CSV 檔案名稱
CSV_FILE = "youtube_comments.csv"

def get_next_api_key():
    """自動切換到下一個 API Key"""
    global current_key_index
    if not API_KEYS:
        raise ValueError("未找到 API Key，請確認 YOUTUBE_API_KEYS 環境變數是否正確設置")
    
    api_key = API_KEYS[current_key_index]
    current_key_index = (current_key_index + 1) % len(API_KEYS)
    return api_key

def init_db():
    """確保資料庫 `SOPHIA` 存在，並確保 `youtube_louisa` 和 `youtube_cama` 資料表存在"""
    engine = create_engine("mysql+pymysql://你的資料庫帳號:你的資料庫密碼@你的資料庫IP:3306/你的資料庫名稱", pool_pre_ping=True)
    connection = engine.connect()

    # ✅ 使用 `text()` 來確保 SQLAlchemy 可執行 SQL
    connection.execute(text("CREATE DATABASE IF NOT EXISTS SOPHIA;"))
    connection.commit()
    connection.close()

    # **重新連接至 SOPHIA 資料庫**
    engine = create_engine("mysql+pymysql://你的資料庫帳號:你的資料庫密碼@你的資料庫IP:3306/你的資料庫名稱", pool_pre_ping=True)
    Base = declarative_base()

    class Louisa(Base):
        __tablename__ = "youtube_louisa"
        id = Column(Integer, primary_key=True, autoincrement=True)
        video_id = Column(String(50), index=True, nullable=False)
        content = Column(Text, nullable=False)
        author = Column(String(255))
        like_count = Column(Integer)
        created_at = Column(DateTime, default=datetime.now(timezone.utc))

    class Cama(Base):
        __tablename__ = "youtube_cama"
        id = Column(Integer, primary_key=True, autoincrement=True)
        video_id = Column(String(50), index=True, nullable=False)
        content = Column(Text, nullable=False)
        author = Column(String(255))
        like_count = Column(Integer)
        created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # **確保資料表存在**
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    return Session, Cama, Louisa

Session, Cama, Louisa = init_db()

def retry_request(request_function, retries=3, delay=5):
    """帶有重試機制的 API 請求"""
    for attempt in range(retries):
        try:
            return request_function()
        except HttpError as e:
            if "quotaExceeded" in str(e):
                print("API 配額已用完，切換 API Key 後重試...")
                os.environ['YOUTUBE_API_KEY'] = get_next_api_key()
            else:
                print(f"發生錯誤: {e}")
            if attempt < retries - 1:
                print(f"重試第 {attempt + 1} 次...")
                time.sleep(delay)
            else:
                raise

def save_to_csv(video_id, comment):
    """將留言儲存到 CSV 檔案"""
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # 如果檔案不存在，寫入標題
        if not file_exists:
            writer.writerow(["video_id", "content", "author", "like_count", "created_at"])
        writer.writerow([video_id, comment["content"], comment["author"], comment["like_count"], comment["created_at"]])

def youtube_scraper(query):
    API_KEY = get_next_api_key()
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    session = Session()
    table = Cama if 'cama' in query.lower() else Louisa

    # 取得已存入的影片 ID，避免重複爬取
    existing_video_ids = {row.video_id for row in session.query(table.video_id).distinct()}

    def fetch_videos():
        return youtube.search().list(
            q=query,
            part='id,snippet',
            type='video',
            maxResults=10
        ).execute().get('items', [])

    videos = retry_request(fetch_videos)

    for video in videos:
        video_id = video['id']['videoId']
        if video_id in existing_video_ids:
            continue  # 跳過已存影片

        comments = get_all_comments(youtube, video_id)

        for comment in comments:
            if session.query(table).filter_by(video_id=video_id, content=comment['content']).first():
                continue  # 跳過已存留言

            try:
                comment_obj = table(video_id=video_id, **comment)
                session.add(comment_obj)
                session.commit()
                save_to_csv(video_id, comment)  # ✅ 存入 CSV
            except IntegrityError:
                session.rollback()

    session.close()

def get_all_comments(youtube, video_id, max_comments=100):
    comments = []
    retries = 0
    max_retries = 3

    while retries < max_retries and len(comments) < max_comments:
        try:
            request = youtube.commentThreads().list(part="snippet", videoId=video_id, maxResults=100)
            while request and len(comments) < max_comments:
                response = request.execute()
                for item in response.get('items', []):
                    comment_data = item['snippet']['topLevelComment']['snippet']
                    comment_text = comment_data['textOriginal'].strip()

                    # ✅ 只存入至少含有一個中文字的留言
                    if not re.search(r'[\u4e00-\u9fff]', comment_text):
                        continue

                    comments.append({
                        'content': comment_text[:2000],  # 限制最多 2000 字
                        'author': comment_data['authorDisplayName'],
                        'like_count': comment_data['likeCount'],
                        'created_at': parse(comment_data['publishedAt'])
                    })
                    if len(comments) >= max_comments:
                        break
                request = youtube.commentThreads().list_next(request, response)
            return comments[:max_comments]
        except HttpError:
            retries += 1
            time.sleep(2)
    return comments[:max_comments]

def main():
    keywords = ["路易莎咖啡 評價", "cama café 評價", "路易莎 咖啡 CP值", "cama 咖啡 CP值", "路易莎 咖啡 最熱銷", "cama 咖啡 最熱銷","路易莎 咖啡 促銷活動", "cama 咖啡 促銷活動", "路易莎 vs cama 咖啡口味比較", "路易莎 vs cama 行銷策略比較"]
    
    for keyword in keywords:
        youtube_scraper(keyword)
        time.sleep(10)  # 避免 API 過載

if __name__ == "__main__":
    main()
