import pandas as pd
import re

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

def create_store_region_mapping(stores_csv1_path, stores_csv2_path):
    """處理兩個店家 CSV 檔案，建立店家-地區對照表"""
    print("正在處理店家資料...")
    
    # 讀取兩個 CSV 檔案
    df1 = pd.read_csv(stores_csv1_path)
    df2 = pd.read_csv(stores_csv2_path)
    
    # 合併資料框
    df_stores = pd.concat([df1, df2], ignore_index=True)
    
    # 移除重複的店家（如果有的話）
    df_stores = df_stores.drop_duplicates(subset=['shop'])
    
    # 新增地區欄位
    df_stores['region'] = df_stores['address'].apply(get_region)
    
    # 建立店家-地區對照字典
    store_region_dict = dict(zip(df_stores['shop'], df_stores['region']))
    
    # 儲存對照表
    df_stores[['shop', 'region']].to_csv('store_region_mapping.csv', encoding='utf-8-sig', index=False)
    
    print(f"共處理了 {len(df_stores)} 家店舖")
    print("地區分布：")
    print(df_stores.groupby('region')['shop'].count())
    
    return store_region_dict

def parse_sql_file(sql_file_path):
    """解析 SQL 檔案中的資料"""
    print("正在讀取 SQL 檔案...")
    
    try:
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
            
        # 使用正則表達式找出 INSERT 語句中的值
        pattern = r"\((\d+,'[^']*','[^']*',\d+,'[^']*','[^']*','[^']*')\)"
        matches = re.findall(pattern, sql_content)
        
        # 解析匹配到的資料
        data_list = []
        for match in matches:
            # 分割每一列的值
            values = match.split(',')
            
            # 清理資料（移除引號等）
            id_val = int(values[0])
            brand = values[1].strip("'")
            store_name = values[2].strip("'")
            rating = int(values[3])
            content = values[4].strip("'")
            content_time = values[5].strip("'")
            crawling_time = values[6].strip("'")
            
            data_list.append({
                'id': id_val,
                'brand': brand,
                'store_name': store_name,
                'rating': rating,
                'content': content,
                'content_time': content_time,
                'crawling_time': crawling_time
            })
        
        # 轉換為 DataFrame
        df = pd.DataFrame(data_list)
        print(f"成功讀取 {len(df)} 筆評論資料")
        return df
        
    except Exception as e:
        print(f"讀取 SQL 檔案時發生錯誤：{e}")
        return None

def process_sql_data(store_region_dict, sql_data):
    """處理 SQL 資料"""
    print("\n正在處理評論資料...")
    
    # 新增地區欄位
    sql_data['region'] = sql_data['store_name'].map(store_region_dict)
    
    # 依照地區和評分進行分組
    region_rating = sql_data.groupby(['region', 'rating'])['id'].count().reset_index(name='count')
    
    # 計算各區域統計資料
    region_stats = sql_data.groupby('region').agg({
        'rating': ['count', 'mean', 'min', 'max']
    }).round(2)
    
    # 儲存結果
    sql_data.to_csv('processed_reviews.csv', encoding='utf-8-sig', index=False)
    region_rating.to_csv('region_rating_distribution.csv', encoding='utf-8-sig', index=False)
    region_stats.to_csv('region_statistics.csv', encoding='utf-8-sig')
    
    print("\n評分分布：")
    print(region_rating)
    print("\n地區統計：")
    print(region_stats)
    
    return sql_data, region_rating, region_stats

def main():
    try:
        # 1. 處理店家資料，建立地區對照表
        store_region_dict = create_store_region_mapping(
            'Louisa.csv',     # 第一個店家資料檔案
            'Cama.csv'        # 第二個店家資料檔案
        )
        
        # 2. 讀取 SQL 檔案
        sql_data = parse_sql_file('data.sql')
        
        if sql_data is not None:
            # 3. 處理 SQL 資料
            processed_data, rating_dist, stats = process_sql_data(store_region_dict, sql_data)
            print("\n資料處理完成！")
        else:
            print("無法處理 SQL 資料")
        
    except FileNotFoundError as e:
        print(f"錯誤：找不到檔案 - {e}")
    except Exception as e:
        print(f"錯誤：{e}")

if __name__ == "__main__":
    main()