import pandas as pd
import re
from datetime import datetime
from yt_con_db import DatabaseConfig

def analyze_comments(df):
    # 確保 DataFrame 包含所有必要欄位
    required_columns = ["id", "video_id", "content", "author", "likes", "timestamp"]
    
    for col in required_columns:
        if col not in df.columns:
            if col == "likes":
                df[col] = 0  # 如果沒有 likes，填充 0
            elif col == "timestamp":
                df[col] = datetime.now()  # 如果沒有 timestamp，填充當前時間
            else:
                df[col] = "未知"  # 其他缺失欄位填充 "未知"

    # 轉換資料類型
    df['id'] = df['id'].astype(int)
    df['likes'] = df['likes'].astype(int)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # 定義咖啡品牌關鍵字
    louisa_keywords = ['路易莎', '露易莎', 'louisa', 'Louisa']
    
    # 建立品牌標記
    def identify_brand(text):
        text_lower = text.lower()
        if any(keyword.lower() in text_lower for keyword in louisa_keywords):
            return 'Louisa'
        return None  
    
    # 過濾政治相關留言
    political_keywords = ['民主', '獨裁', '政黨', '民進黨', '國民黨', '政治', '青鳥', '選舉', '罷免']
    def filter_political_content(text):
        return not any(keyword in text for keyword in political_keywords)
    
    df = df[df['content'].apply(filter_political_content)]

    # 情感分析
    def analyze_sentiment(text):
        positive_words = {'好喝': 3, '讚': 2, '推': 2, '棒': 3, '喜歡': 3, '美味': 4, '香': 2, '值得': 3, '專業': 3, '順口': 2, '回甘': 2, '愛': 2, '很不錯': 1}
        negative_words = {'難喝': -4, '糟': -3, '爛': -3, '差': -3, '噁心': -4, '失望': -3, '貴': -2, '雷': -3, '踩雷': -4, '淡': -2, '完全不行': -3}
        
        pos_score = sum([score for word, score in positive_words.items() if word in text])
        neg_score = sum([score for word, score in negative_words.items() if word in text])
        
        sentiment_score = pos_score + neg_score
        
        if sentiment_score > 2:
            return '強烈正面', sentiment_score
        elif sentiment_score > 0:
            return '正面', sentiment_score
        elif sentiment_score < -2:
            return '強烈負面', sentiment_score
        elif sentiment_score < 0:
            return '負面', sentiment_score
        return '中性', sentiment_score
    
    # 主題分類
    def classify_topic(text):
        topics = {
            '品質': ['品質', '口感', '味道', '風味', '豆子', '咖啡', '回甘', '順口', '濃郁', '淡', '苦', '香醇', '濃縮'],
            '服務': ['服務', '態度', '店員', '人員', '店長', '熱情', '貼心', '友善', '慢', '不理人', '專業', '耐心', '熱忱'],
            '價格': ['價格', '貴', '便宜', '划算', '值得', '便利', 'CP值', '優惠', '折扣', '活動', '性價比'],
            '環境': ['環境', '空間', '座位', '店面', '裝潢', '衛生', '吵雜', '安靜', '燈光', '氣氛', '音樂', '舒適']
        }
        
        found_topics = []
        for topic, keywords in topics.items():
            if any(keyword in text for keyword in keywords):
                found_topics.append(topic)
        
        return '、'.join(found_topics) if found_topics else '其他'
    
    # 添加分析欄位
    df.loc[:, 'brand'] = df['content'].apply(identify_brand)
    df_filtered = df[df['brand'].notna()].copy()
    df_filtered[['sentiment', 'sentiment_score']] = df_filtered['content'].apply(lambda x: pd.Series(analyze_sentiment(x)))
    df_filtered['topic'] = df_filtered['content'].apply(classify_topic)
    df_filtered = df_filtered[df_filtered['content'].str.len() >= 5]

    # 結果排序
    df_filtered = df_filtered.sort_values(['brand', 'likes', 'timestamp'], ascending=[True, False, False])
    
    return df_filtered

if __name__ == "__main__":
    db_config = DatabaseConfig()
    
    # 從 SOPHIA.youtube_cama 讀取資料
    table_name = "youtube_louisa"
    df = db_config.read_table_to_df(table_name, schema="SOPHIA")  

    if not df.empty:
        result_df = analyze_comments(df)
        
        # 存入 CLEAN_SOPHIA.youtube_comments_cama
        result_df.to_csv('youtube_comments_louisa.csv', index=False, encoding='utf-8')
        db_config.write_df_to_table(result_df, "youtube_comments_louisa", schema="CLEAN_SOPHIA")
