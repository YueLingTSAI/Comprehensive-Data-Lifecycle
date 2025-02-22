import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 讀取資料
df = pd.read_csv("youtube_comments_combined.csv")

# 1️⃣ 品牌話題趨勢
plt.figure(figsize=(14, 7))
brand_topic_counts = df.groupby(['brand', 'topic']).size().unstack().fillna(0)
if not brand_topic_counts.empty:
    brand_topic_counts.plot(kind='bar', edgecolor='black')
    plt.title("品牌間話題趨勢", fontsize=14)
    plt.xlabel("品牌", fontsize=12)
    plt.ylabel("評論數量", fontsize=12)
    plt.xticks(rotation=30, ha="right")
    plt.legend(title="話題", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

# 2️⃣ 品牌情緒分析
plt.figure(figsize=(14, 7))
brand_sentiment_counts = df.groupby(['brand', 'sentiment']).size().unstack().fillna(0)
if not brand_sentiment_counts.empty:
    brand_sentiment_counts.plot(kind='bar', stacked=True, edgecolor='black')
    plt.title("品牌間情緒分析", fontsize=14)
    plt.xlabel("品牌", fontsize=12)
    plt.ylabel("評論數量", fontsize=12)
    plt.xticks(rotation=30, ha="right")
    plt.legend(title="情緒", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

# 3️⃣ 競品話題情緒比較
plt.figure(figsize=(14, 7))
brand_topic_sentiment_counts = df.groupby(['brand', 'topic', 'sentiment']).size().unstack().fillna(0)
if not brand_topic_sentiment_counts.empty:
    brand_topic_sentiment_counts.plot(kind='bar', stacked=True, edgecolor='black')
    plt.title("競品話題情緒比較", fontsize=14)
    plt.xlabel("品牌與話題", fontsize=12)
    plt.ylabel("評論數量", fontsize=12)
    plt.xticks(rotation=30, ha="right")
    plt.legend(title="情緒", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

# 4️⃣ 關鍵字詞雲
plt.figure(figsize=(10, 5))
text = " ".join(df['content'].dropna())
if text:
    wordcloud = WordCloud(
        font_path="C:/Windows/Fonts/msjh.ttc",
        width=1600, height=800,
        background_color='white'
    ).generate(text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title("關鍵字詞雲", fontsize=14)
    plt.tight_layout()

# 5️⃣ 時間趨勢圖
plt.figure(figsize=(14, 7))
df['created_at'] = pd.to_datetime(df['created_at'])
df['date'] = df['created_at'].dt.date
comment_trend = df.groupby('date').size()
if not comment_trend.empty:
    comment_trend.plot(marker='o')
    plt.title("評論數量時間趨勢", fontsize=14)
    plt.xlabel("日期", fontsize=12)
    plt.ylabel("評論數量", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()

# 只在最後執行一次 plt.show()
plt.show()
