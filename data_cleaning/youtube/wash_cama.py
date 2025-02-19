import pandas as pd
import re
from datetime import datetime
from collections import Counter
import itertools

def read_sql_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"讀取檔案時發生錯誤: {str(e)}")
        return None

def analyze_comments(sql_content):
    pattern = r"\((\d+),'(.*?)','(.*?)','(.*?)',(\d+),'(.*?)'\)"
    matches = re.findall(pattern, sql_content)
    
    df = pd.DataFrame(matches, columns=['id', 'video_id', 'content', 'author', 'likes', 'timestamp'])
    df['id'] = df['id'].astype(int)
    df['likes'] = df['likes'].astype(int)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    cama_keywords = ['cama', 'Cama', '咖瑪', 'CAMA']
    def identify_brand(text):
        text_lower = text.lower()
        if any(keyword.lower() in text_lower for keyword in cama_keywords):
            return 'Cama'
        return None
    
    political_keywords = ['民主', '獨裁', '政黨', '民進黨', '國民黨', '政治', '青鳥', '選舉', '罷免']
    def filter_political_content(text):
        return not any(keyword in text for keyword in political_keywords)
    
    df = df[df['content'].apply(filter_political_content)]
    
    def analyze_sentiment(text):
        positive_words = {'好喝': 3, '讚': 2, '推': 2, '棒': 3, '喜歡': 3, '美味': 4, '香': 2, '值得': 3, '專業': 3, '順口': 2, '回甘': 2, '喜歡': 1, '愛': 2, '很不錯': 1}
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
    
    def classify_topic(text):
        topics = {
            '品質': ['品質', '口感', '味道', '風味', '豆子', '咖啡', '回甘', '順口', '濃郁', '淡', '苦', '香醇', '濃縮'],
            '服務': ['服務', '態度', '店員', '人員', '店長', '熱情', '貼心', '友善', '慢', '不理人', '專業', '耐心', '熱忱'],
            '價格': ['價格', '貴', '便宜', '划算', '值得', '便利', 'CP值', '優惠', '折扣', '活動', '性價比'],
            '環境': ['環境', '空間', '座位', '店面', '裝潢', '衛生', '吵雜', '安靜', '燈光', '氣氛', '音樂', '舒適'],
            '速度': ['等太久', '超快', '出餐慢', '排隊', '等候', '快速', '拖延'],
            '包裝': ['紙杯', '吸管', '環保', '包裝', '外帶', '設計'],
            '甜點/餐點': ['可頌', '蛋糕', '司康', '餐點', '甜點', '點心', '麵包', '輕食', '小食']
        }
        
        found_topics = []
        for topic, keywords in topics.items():
            if any(keyword in text for keyword in keywords):
                found_topics.append(topic)
        
        return '、'.join(found_topics) if found_topics else '其他'
    
    df['brand'] = df['content'].apply(identify_brand)
    df_filtered = df[df['brand'].notna()].copy()
    df_filtered[['sentiment', 'sentiment_score']] = df_filtered['content'].apply(lambda x: pd.Series(analyze_sentiment(x)))
    df_filtered['topic'] = df_filtered['content'].apply(classify_topic)
    df_filtered = df_filtered[df_filtered['content'].str.len() >= 5]
    df_filtered = df_filtered.sort_values(['brand', 'likes', 'timestamp'], ascending=[True, False, False])
    
    return df_filtered

if __name__ == "__main__":
    file_path = "youtube_cama.sql"
    sql_content = read_sql_file(file_path)
    if sql_content:
        result_df = analyze_comments(sql_content)
        result_df.to_csv('analysis_cama.csv', index=False, encoding='utf-8')
