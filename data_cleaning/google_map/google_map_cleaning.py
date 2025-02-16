import pandas as pd
import re
from g_c_DB import DatabaseConfig

# 定義地區分類
region_mapping = {
    '北部': ['臺北市', '台北市', '新北市', '基隆市', '新竹市', '桃園市', '新竹縣', '宜蘭縣'],
    '中部': ['臺中市', '台中市', '苗栗縣', '彰化縣', '南投縣', '雲林縣'],
    '南部': ['高雄市', '臺南市', '台南市', '嘉義市', '嘉義縣', '屏東縣', '澎湖縣'],
    '東部': ['花蓮縣', '台東縣', '臺東縣'],
    '外島': ['金門縣', '連江縣']
}

def get_region(address):
    """根據地址判斷所屬地區"""
    for region, counties in region_mapping.items():
        if any(county in address for county in counties):
            return region
    return '其他'

def create_store_region_mapping(stores_csv1_path, stores_csv2_path, db_config):
    """處理兩個店家 CSV 檔案，建立店家-地區對照表"""
    print("正在處理店家資料...")
    
    # 讀取兩個 CSV 檔案
    df1 = pd.read_csv(stores_csv1_path)
    df2 = pd.read_csv(stores_csv2_path)
    
    # 合併資料框
    df_stores = pd.concat([df1, df2], ignore_index=True)
    
    # 移除重複的店家
    df_stores = df_stores.drop_duplicates(subset=['shop'])
    
    # 新增地區欄位
    df_stores['region'] = df_stores['address'].apply(get_region)
    
    # 建立店家-地區對照字典
    store_region_dict = dict(zip(df_stores['shop'], df_stores['region']))
    
    # 將結果寫入資料庫
    db_config.write_df_to_table(
        df_stores[['shop', 'region']], 
        'store_region_mapping'
    )
    
    print(f"共處理了 {len(df_stores)} 家店舖")
    print("地區分布：")
    print(df_stores.groupby('region')['shop'].count())
    
    return store_region_dict

def is_too_old(time_str):
    """判斷是否為6年以前的資料"""
    if not isinstance(time_str, str):
        return False
    
    year_match = re.search(r'(\d+)\s*年前', time_str)
    if year_match:
        years = int(year_match.group(1))
        return years >= 6
    return False

def process_sql_data(store_region_dict, sql_data, db_config):
    """處理 SQL 資料"""
    print("\n正在處理評論資料...")
    
    # 過濾掉6年以前的資料
    original_count = len(sql_data)
    sql_data = sql_data[~sql_data['content_time'].apply(is_too_old)].copy()
    filtered_count = len(sql_data)
    print(f"原始資料量：{original_count} 筆")
    print(f"過濾後資料量：{filtered_count} 筆")
    print(f"移除 {original_count - filtered_count} 筆舊資料")
    
    # 新增地區欄位
    sql_data['region'] = sql_data['store_name'].map(store_region_dict)
    
    # 依照地區和評分進行分組
    region_rating = sql_data.groupby(['region', 'rating'])['id'].count().reset_index(name='count')
    
    # 計算各區域統計資料
    region_stats = sql_data.groupby('region').agg({
        'rating': ['count', 'mean', 'min', 'max']
    }).round(2)
    
    # 將結果寫入資料庫
    db_config.write_df_to_table(sql_data, 'processed_reviews_recent')
    db_config.write_df_to_table(region_rating, 'region_rating_distribution_recent')
    db_config.write_df_to_table(region_stats, 'region_statistics_recent')
    
    print("\n評分分布：")
    print(region_rating)
    print("\n地區統計：")
    print(region_stats)
    
    return sql_data, region_rating, region_stats

def main():
    try:
        # 初始化資料庫設定
        db_config = DatabaseConfig()
        
        # 1. 處理店家資料，建立地區對照表
        store_region_dict = create_store_region_mapping(
            'Louisa.csv',     # 第一個店家資料檔案
            'Cama.csv',       # 第二個店家資料檔案
            db_config
        )
        
        # 2. 從資料庫讀取評論資料
        sql_data = db_config.read_table_to_df('google_map', schema='SOPHIA')
        
        if sql_data is not None:
            # 3. 處理資料並寫入資料庫
            processed_data, rating_dist, stats = process_sql_data(
                store_region_dict, 
                sql_data,
                db_config
            )
            print("\n資料處理完成！")
        else:
            print("無法處理資料")
        
    except Exception as e:
        print(f"錯誤：{e}")

if __name__ == "__main__":
    main()