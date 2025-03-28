from sqlalchemy import create_engine, Column, Integer, String, DateTime, text, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from typing import List, Dict, Tuple

def init_db():
    # 直接連接到 指定 資料庫
    engine = create_engine(
        "mysql+pymysql://你的資料庫帳號:你的資料庫密碼@你的資料庫IP:3306/你的資料庫名稱"
    )
    Base = declarative_base()

    class Dcard(Base):
        __tablename__ = "dcard"
        id = Column(Integer, primary_key=True)
        cafe = Column(String(50))
        title = Column(String(255))
        link = Column(String(512), unique=True)
        content = Column(String(2000))
        source = Column(String(50))
        search_date = Column(DateTime)
        # 以下欄位由其他程序處理，在爬蟲時可為 NULL
        sentiment = Column(String(20), nullable=True)
        sentiment_score = Column(Float, nullable=True)
        sentiment_explanation = Column(Text, nullable=True)

    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return engine, Base, Session, session, Dcard

engine, Base, Session, session, Dcard = init_db()

def save_to_db(reviews: List[Dict]) -> Tuple[int, int]:
    """
    將評論保存到資料庫，並返回成功和重複的數量
    Args:
        reviews: 評論列表
    Returns:
        Tuple[int, int]: (成功新增數量, 重複連結數量)
    """
    # 如果沒有資料，直接返回 0, 0
    if not reviews:
        print("\n===== 資料庫存儲統計 =====")
        print("成功新增: 0 筆")
        print("重複連結: 0 筆")
        print("總處理筆數: 0 筆")
        return 0, 0

    success_count = 0
    duplicate_count = 0

    for review in reviews:
        try:
            review_obj = Dcard(**review)
            session.add(review_obj)
            session.commit()
            success_count += 1
            print(f"成功新增: {review['title']}")
        except IntegrityError:
            session.rollback()
            duplicate_count += 1
            print(f"重複連結，跳過: {review['link']}")

    print(f"\n===== 資料庫存儲統計 =====")
    print(f"成功新增: {success_count} 筆")
    print(f"重複連結: {duplicate_count} 筆")
    print(f"總處理筆數: {success_count + duplicate_count} 筆")

    return success_count, duplicate_count
