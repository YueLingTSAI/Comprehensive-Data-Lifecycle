# 分析檔案

## store_region_mapping.csv：店家地區對照表
```
shop,region
澎湖馬公門市,南部
金門金城門市,外島
台北信義門市,北部
...
```

## processed_reviews.csv：處理後的評論資料
```
id,brand,store_name,rating,content,content_time,crawling_time,region
1,Louisa,澎湖馬公門市,5,店員親切...,4 天前,2025-02-14 03:02:17,南部
2,Louisa,澎湖馬公門市,5,,1 週前,2025-02-14 03:02:17,南部
...
```

## region_rating_distribution.csv：各地區評分分布
```
region,rating,count
北部,1,50     # 代表北部有 50 筆 1 星評價
北部,2,100    # 代表北部有 100 筆 2 星評價
北部,3,200    # 代表北部有 200 筆 3 星評價
北部,4,300    # 代表北部有 300 筆 4 星評價
北部,5,400    # 代表北部有 400 筆 5 星評價
中部,1,30     # 代表中部有 30 筆 1 星評價
...           # 以此類推
```

## region_statistics.csv：地區統計資料
```
region,rating_count,rating_mean,rating_min,rating_max
北部,1050,4.2,1,5    # 代表北部總共有1050筆評價，平均4.2星，最低1星，最高5星
中部,800,4.1,1,5     # 代表中部總共有800筆評價，平均4.1星，最低1星，最高5星
南部,600,4.3,1,5     # 代表南部總共有600筆評價，平均4.3星，最低1星，最高5星
...
```