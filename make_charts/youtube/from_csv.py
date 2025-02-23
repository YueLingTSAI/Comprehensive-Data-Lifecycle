import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 讀取資料
df_cama = pd.read_csv("data/youtube_comments_cama.csv")
df_louisa = pd.read_csv("data/youtube_comments_louisa.csv")
df_combined = pd.read_csv("data/youtube_comments_combined.csv")

# 確保資料不為空
if df_combined.empty or df_cama.empty or df_louisa.empty:
    print("❌ 無法繪圖：部分資料表為空")
    exit()  

# 1️⃣ 品牌評論數量週期性分析
# 轉換時間格式
df_cama['created_at'] = pd.to_datetime(df_cama['created_at'], errors='coerce')
df_louisa['created_at'] = pd.to_datetime(df_louisa['created_at'], errors='coerce')

# 新增時間變數
df_cama['month'] = df_cama['created_at'].dt.month
df_louisa['month'] = df_louisa['created_at'].dt.month
df_cama['weekday'] = df_cama['created_at'].dt.dayofweek
df_louisa['weekday'] = df_louisa['created_at'].dt.dayofweek
df_cama['hour'] = df_cama['created_at'].dt.hour
df_louisa['hour'] = df_louisa['created_at'].dt.hour

# 設定 x 軸標籤
month_labels = ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"]
weekday_labels = ["一", "二", "三", "四", "五", "六", "日"]
hour_labels = [f"{h}:00" for h in range(0, 24, 2)]

# 計算評論數量
all_months = range(1, 13)
cama_monthly = df_cama['month'].value_counts().reindex(all_months, fill_value=0).sort_index()
louisa_monthly = df_louisa['month'].value_counts().reindex(all_months, fill_value=0).sort_index()

all_days = range(7)
cama_weekly = df_cama['weekday'].value_counts().reindex(all_days, fill_value=0).sort_index()
louisa_weekly = df_louisa['weekday'].value_counts().reindex(all_days, fill_value=0).sort_index()

all_hours = range(0, 24)
cama_hourly = df_cama['hour'].value_counts().reindex(all_hours, fill_value=0).sort_index()
louisa_hourly = df_louisa['hour'].value_counts().reindex(all_hours, fill_value=0).sort_index()

# 設定顏色
cama_color = "#1f77b4"
louisa_color = "#17becf"

# 繪製評論數量週期性分析圖
fig, axes = plt.subplots(1, 3, figsize=(16, 6))

# 月份分析
axes[0].bar(cama_monthly.index, cama_monthly, color=cama_color, label="Cama")
axes[0].bar(louisa_monthly.index, louisa_monthly, color=louisa_color, bottom=cama_monthly, label="Louisa")
axes[0].set_title("評論數量週期性分析（月份）", fontsize=14)
axes[0].set_xlabel("月份", fontsize=12)
axes[0].set_ylabel("評論數量", fontsize=12)
axes[0].set_xticks(range(1, 13))
axes[0].set_xticklabels(month_labels, rotation=45)
axes[0].legend(title="品牌")

# 星期分析
axes[1].bar(cama_weekly.index, cama_weekly, color=cama_color, label="Cama")
axes[1].bar(louisa_weekly.index, louisa_weekly, color=louisa_color, bottom=cama_weekly, label="Louisa")
axes[1].set_title("評論數量週期性分析（星期）", fontsize=14)
axes[1].set_xlabel("星期", fontsize=12)
axes[1].set_ylabel("評論數量", fontsize=12)
axes[1].set_xticks(range(7))
axes[1].set_xticklabels(weekday_labels)
axes[1].legend(title="品牌")

# 時段分析
axes[2].bar(cama_hourly.index, cama_hourly, color=cama_color, label="Cama")
axes[2].bar(louisa_hourly.index, louisa_hourly, color=louisa_color, bottom=cama_hourly, label="Louisa")
axes[2].set_title("評論數量週期性分析（時段）", fontsize=14)
axes[2].set_xlabel("時段", fontsize=12)
axes[2].set_ylabel("評論數量", fontsize=12)
axes[2].set_xticks(range(0, 24, 2))
axes[2].set_xticklabels(hour_labels, rotation=45)
axes[2].legend(title="品牌")

plt.tight_layout()
plt.show()

# 自訂義情緒排序
sentiment_order = ['強烈正面', '正面', '中性', '負面', '強烈負面']
df_combined['sentiment'] = pd.Categorical(df_combined['sentiment'], categories=sentiment_order, ordered=True)

# 設定配色
colors = sns.color_palette("tab10", n_colors=10)
topic_colors = sns.color_palette("husl", n_colors=len(df_combined['topic'].unique()))

# 2️⃣ 各主題情緒分布熱力圖
brand_topic_sentiment = df_combined.pivot_table(index='topic', columns=['brand', 'sentiment'], aggfunc='size', fill_value=0)
fig, axes = plt.subplots(1, 2, figsize=(16, 8), sharey=True)
fig.suptitle('各主題情緒分布熱力圖', fontsize=18, fontweight='bold')

sns.heatmap(brand_topic_sentiment['Cama'], cmap='Reds', annot=True, fmt='d', linewidths=1, linecolor='black', ax=axes[0])
axes[0].set_title('Cama', fontsize=16)
axes[0].set_xlabel('情緒類別', fontsize=14)
axes[0].set_ylabel('主題', fontsize=14)

sns.heatmap(brand_topic_sentiment['Louisa'], cmap='Blues', annot=True, fmt='d', linewidths=1, linecolor='black', ax=axes[1])
axes[1].set_title('Louisa', fontsize=16)
axes[1].set_xlabel('情緒類別', fontsize=14)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

# 3️⃣ 品牌情緒極性佔比（圓餅圖）
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle("Cama vs Louisa 情緒分析比較", fontsize=18, fontweight='bold')
for i, (df, brand) in enumerate(zip([df_cama, df_louisa], ['Cama', 'Louisa'])):
    sentiment_counts = df['sentiment'].value_counts().sort_index()
    axes[i].pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', colors=sns.color_palette("Set2"), startangle=140)
    axes[i].set_title(f"{brand}", fontsize=16)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

# 4️⃣ 品牌話題趨勢
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
