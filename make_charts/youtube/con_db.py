import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import pandas as pd
from wordcloud import WordCloud
from yt_con_db import DatabaseConfig

# 設定中文字體（Windows）
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 或 ['SimSun']
plt.rcParams['axes.unicode_minus'] = False  # 確保負號正常顯示
font_path = "C:/Windows/Fonts/msjh.ttc"  # Microsoft JhengHei
prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = prop.get_name()

# 創建資料庫連線設定
db = DatabaseConfig()

df_cama = db.read_table_to_df("youtube_comments_cama")  # 假設表名是 youtube_comments
df_louisa = db.read_table_to_df("youtube_comments_louisa")  # 假設表名是 youtube_reviews

# 確認資料是否讀取成功
print(f"Cama 資料筆數: {len(df_cama)}")
print(f"Louisa 資料筆數: {len(df_louisa)}")

# 如果資料為空則直接結束
if df_cama.empty and df_louisa.empty:
    print("❌ 無法繪圖：資料表為空")
    exit()

# 合併兩個資料表
df = pd.concat([df_cama, df_louisa], ignore_index=True)

# 1️⃣ 品牌話題趨勢
plt.figure(figsize=(14, 7))
brand_topic_counts = df.groupby(['brand', 'topic']).size().unstack().fillna(0)
brand_topic_counts.plot(kind='bar', edgecolor='black')
plt.title("品牌話題趨勢", fontsize=14)
plt.xlabel("品牌", fontsize=12)
plt.ylabel("評論數量", fontsize=12)
plt.legend(title="話題", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# 2️⃣ 品牌情緒分析
plt.figure(figsize=(14, 7))
brand_sentiment_counts = df.groupby(['brand', 'sentiment']).size().unstack().fillna(0)
brand_sentiment_counts.plot(kind='bar', stacked=True, edgecolor='black')
plt.title("品牌情緒分析", fontsize=14)
plt.xlabel("品牌", fontsize=12)
plt.ylabel("評論數量", fontsize=12)
plt.legend(title="情緒", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# 3️⃣ 競品話題情緒比較
plt.figure(figsize=(14, 7))
brand_topic_sentiment_counts = df.groupby(['brand', 'topic', 'sentiment']).size().unstack().fillna(0)
brand_topic_sentiment_counts.plot(kind='bar', stacked=True, edgecolor='black')
plt.title("競品話題情緒比較", fontsize=14)
plt.xlabel("品牌與話題", fontsize=12)
plt.ylabel("評論數量", fontsize=12)
plt.legend(title="情緒", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=30, ha="right")  # 讓 X 軸標籤向右傾斜
plt.tight_layout()

# 4️⃣ 關鍵字詞雲
# 讀取評論文本
plt.figure(figsize=(10, 5))
text = " ".join(df['content'].dropna())
wordcloud = WordCloud(font_path="C:/Windows/Fonts/msjh.ttc", width=1600, height=800, background_color='white', colormap='viridis').generate(text)
# 顯示詞雲
plt.figure(figsize=(14, 7))  # 增加 Matplotlib 畫布大小
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("關鍵字詞雲", fontsize=18)
plt.tight_layout()

# 5️⃣ 時間趨勢圖
plt.figure(figsize=(14, 7))
df['created_at'] = pd.to_datetime(df['created_at'])
df['date'] = df['created_at'].dt.date
comment_trend = df.groupby('date').size()
comment_trend.plot(marker='o')
plt.title("評論數量時間趨勢", fontsize=14)
plt.xlabel("日期", fontsize=12)
plt.ylabel("評論數量", fontsize=12)
plt.grid()
plt.xticks(rotation=30, ha="right")  # 讓 X 軸標籤向右傾斜
plt.tight_layout()

# 只在最後執行一次 plt.show()
plt.show()

if __name__ == "__main__":
    db_config = DatabaseConfig()