import pandas as pd
import re
from datetime import datetime

def read_sql_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"讀取檔案時發生錯誤: {str(e)}")
        return None

def analyze_comments(sql_content):
    # 使用正則表達式找出所有 INSERT 語句中的資料（允許匹配中文）
    pattern = r"\((\d+),'(.*?)','(.*?)','(.*?)',(\d+),'(.*?)'\)"
    matches = re.findall(pattern, sql_content)
    
    # 建立 DataFrame
    df = pd.DataFrame(matches, columns=['id', 'video_id', 'content', 'author', 'likes', 'timestamp'])
    
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
        return None  # Louisa 應該不會被標記為 Cama
    
    # 過濾政治相關留言
    political_keywords = ['民主', '獨裁', '政黨', '民進黨', '國民黨', '政治', '青鳥', '選舉', '罷免']
    def filter_political_content(text):
        return not any(keyword in text for keyword in political_keywords)
    
    df = df[df['content'].apply(filter_political_content)]

    # 情感分析
    def analyze_sentiment(text):
        positive_words = ['好喝', '讚', '推', '棒', '喜歡', '美味', '香', '值得', '專業']
        negative_words = ['難喝', '糟', '爛', '差', '噁心', '失望', '貴', '雷', '踩雷']
        
        pos_count = sum([1 for word in positive_words if word in text])
        neg_count = sum([1 for word in negative_words if word in text])
        
        if pos_count > neg_count:
            return '正面'
        elif neg_count > pos_count:
            return '負面'
        return '中性'
    
    # 主題分類
    def classify_topic(text):
        topics = {
            '品質': ['品質', '口感', '味道', '風味', '豆子', '咖啡'],
            '服務': ['服務', '態度', '店員', '人員', '店長'],
            '價格': ['價格', '貴', '便宜', '划算', '值得', '便利'],
            '環境': ['環境', '空間', '座位', '店面', '裝潢', '衛生']
        }
        
        found_topics = []
        for topic, keywords in topics.items():
            if any(keyword in text for keyword in keywords):
                found_topics.append(topic)
        
        return '、'.join(found_topics) if found_topics else '其他'
    
    # 添加分析欄位
    df['brand'] = df['content'].apply(identify_brand)
    df_filtered = df[df['brand'].notna()].copy()
    df_filtered['sentiment'] = df_filtered['content'].apply(analyze_sentiment)
    df_filtered['topic'] = df_filtered['content'].apply(classify_topic)
    
    # 移除過短的留言（少於5個字）
    df_filtered = df_filtered[df_filtered['content'].str.len() >= 5]
    
    # 結果排序
    df_filtered = df_filtered.sort_values(['brand', 'likes', 'timestamp'], ascending=[True, False, False])
    
    # 打印統計資訊
    print("=== 資料統計 ===")
    print(f"總評論數: {len(df)}")
    print(f"相關評論數: {len(df_filtered)}")
    print("\n品牌分布:")
    print(df_filtered['brand'].value_counts())
    print("\n情感分布:")
    print(df_filtered['sentiment'].value_counts())
    print("\n主題分布:")
    print(df_filtered['topic'].value_counts().head())
    
    # 顯示高讚數的評論範例
    print("\n=== 高讚數評論範例（前5則）===")
    sample_cols = ['brand', 'content', 'sentiment', 'topic', 'likes']
    print(df_filtered[sample_cols].nlargest(5, 'likes'))
    
    return df_filtered

# **確保 'video_id' 也存入 CSV**
result_columns = ['id', 'video_id', 'brand', 'content', 'sentiment', 'topic', 'likes', 'timestamp']

# 主程式執行
if __name__ == "__main__":
    file_path = "youtube_louisa.sql"  # SQL 檔案路徑
    sql_content = read_sql_file(file_path)
    if sql_content:
        result_df = analyze_comments(sql_content)
        # **修正這裡，確保 encoding 適合你的環境**
        result_df[result_columns].to_csv('analysis_louisa.csv', index=False, encoding='utf-8')
