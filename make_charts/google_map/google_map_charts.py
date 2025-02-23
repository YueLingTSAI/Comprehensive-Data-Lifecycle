import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

# 讀取所有資料
df = pd.read_csv("processed_reviews.csv")
region_rating = pd.read_csv("region_rating_distribution.csv")
region_stats = pd.read_csv("region_statistics.csv", skiprows=1)  # 跳過第一行，因為它包含欄位說明
store_mapping = pd.read_csv("store_region_mapping.csv")

# 篩選出 Cama 和 Louisa 的資料
df_filtered = df[df['brand'].str.lower().isin(['cama', 'louisa'])]

# 1️⃣ 品牌評分分布
plt.figure(figsize=(14, 7))
sns.boxplot(data=df_filtered, x='brand', y='rating')
plt.title("Cama vs Louisa 評分分布", fontsize=14)
plt.xlabel("品牌", fontsize=12)
plt.ylabel("評分", fontsize=12)
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig('圖表1_品牌評分分布.png')
plt.close()

# 2️⃣ 地區評分分析（加入品牌區分）
plt.figure(figsize=(14, 7))

# 計算每個地區每個品牌的平均評分
brand_region_stats = df_filtered.groupby(['region', 'brand'])['rating'].agg(['mean', 'count']).reset_index()

# 使用 seaborn 的 grouped barplot
sns.barplot(data=brand_region_stats, x='region', y='mean', hue='brand')

plt.title("各地區品牌平均評分", fontsize=14)
plt.xlabel("地區", fontsize=12)
plt.ylabel("平均評分", fontsize=12)
plt.xticks(rotation=30)
plt.legend(title="品牌")
plt.tight_layout()
plt.savefig('圖表2_地區平均評分.png')
plt.close()

# 3️⃣ 品牌門市區域分布（使用 store_region_mapping.csv）
plt.figure(figsize=(14, 7))
# 移除合併步驟，直接使用原始數據的 region 欄位
df_with_region = df_filtered  # df_filtered 已經包含了 region 欄位

# 計算每個品牌在各地區的門市數量
store_region_dist = df_with_region.groupby(['brand', 'region'])['store_name'].nunique().unstack().fillna(0)

# 繪製堆疊條形圖
store_region_dist.plot(kind='bar', stacked=True)
plt.title("品牌門市區域分布", fontsize=14)
plt.xlabel("品牌", fontsize=12)
plt.ylabel("門市數量", fontsize=12)
plt.legend(title="地區", bbox_to_anchor=(1.05, 1))
plt.tight_layout()
plt.savefig('圖表3_品牌門市區域分布.png')
plt.close()

# 4️⃣ 各地區評分分布熱力圖
plt.figure(figsize=(14, 7))
region_brand_ratings = df_with_region.groupby(['region', 'brand'])['rating'].agg(['mean', 'count']).reset_index()
region_brand_pivot = region_brand_ratings.pivot(index='region', columns='brand', values='mean')

sns.heatmap(region_brand_pivot, annot=True, fmt='.2f', cmap='RdYlBu', center=4)
plt.title("各地區品牌評分熱力圖", fontsize=14)
plt.tight_layout()
plt.savefig('圖表4_地區品牌評分熱力圖.png')
plt.close()

# 5️⃣ 時間趨勢分析（修改版本）
def convert_to_days(time_str):
    if isinstance(time_str, str):
        try:
            number = int(''.join(filter(str.isdigit, time_str)))
            if '年前' in time_str:
                return number * 365
            elif '個月前' in time_str:
                return number * 30
            elif '週前' in time_str:
                return number * 7
            elif '天前' in time_str:
                return number
            elif '小時前' in time_str:
                return 1  # 將小時轉換為1天
        except (ValueError, IndexError):
            return None
    return None

# 計算評論時間並創建時間趨勢圖
plt.figure(figsize=(14, 7))

# 處理時間數據
df_filtered['days_ago'] = df_filtered['content_time'].apply(convert_to_days)
df_clean = df_filtered.dropna(subset=['days_ago'])

# 確保 days_ago 是數值型別
df_clean['days_ago'] = pd.to_numeric(df_clean['days_ago'])

# 針對每個品牌分別處理
for brand in df_clean['brand'].unique():
    brand_data = df_clean[df_clean['brand'] == brand]
    
    # 先按天數分組計算平均評分
    daily_ratings = brand_data.groupby('days_ago')['rating'].mean()
    
    # 排序索引以確保正確的時間順序
    daily_ratings = daily_ratings.sort_index()
    
    # 使用rolling mean來平滑趨勢線（縮小窗口大小以保留更多細節）
    smoothed_ratings = daily_ratings.rolling(window=7, min_periods=1).mean()
    
    # 繪製趨勢線
    plt.plot(smoothed_ratings.index, smoothed_ratings.values, label=brand, linewidth=2)

plt.title("評分時間趨勢（7天移動平均）", fontsize=14)
plt.xlabel("發布時間（天以前）", fontsize=12)
plt.ylabel("平均評分", fontsize=12)
plt.legend()
plt.grid(True, alpha=0.3)
plt.gca().invert_xaxis()  # 反轉 x 軸使得最近的數據在右側
plt.tight_layout()
plt.savefig('圖表5_時間趨勢分析.png')
plt.close()
