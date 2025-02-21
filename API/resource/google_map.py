from flask_apispec import MethodResource, marshal_with, doc, use_kwargs
import util
from . import google_map_route_model
from model import Google_map1, Google_map2, Google_map3, Google_map4

####### API Action #########


class GoogleMaps(MethodResource):
    @doc(description="獲取 Google Map 評論資料，可依品牌、地區和評分進行篩選", tags=["Google_map"])
    @use_kwargs(google_map_route_model.GoogleMapFilterRequest, location=('query'))
    @marshal_with(google_map_route_model.GoogleMapResponse, code=200)
    def get(self, **kwargs):
        # 獲取查詢參數
        brand = kwargs.get('brand')
        region = kwargs.get('region')
        rating = kwargs.get('rating')
        
        # 建立基礎查詢
        query = Google_map1.query.filter_by(brand=brand)
        
        # 添加可選篩選條件
        if region:
            query = query.filter_by(region=region)
        if rating is not None:
            query = query.filter_by(rating=rating)
            
        # 執行查詢
        results = query.all()
        
        if not results:
            return util.failure({"message": "無符合條件的資料"})
            
        # 格式化結果
        data = []
        for item in results:
            data.append({
                "id": item.id,
                "brand": item.brand,
                "store_name": item.store_name,
                "rating": item.rating,
                "content": item.content,
                "content_time": item.content_time,
                "region": item.region
            })
            
        return util.success(data)

class GoogleMapRatingCount(MethodResource):
    @doc(description="獲取 Google Map 評分統計資料，可依品牌、地區和評分進行篩選", tags=["Google_map"])
    @use_kwargs(google_map_route_model.GoogleMapFilterRequest, location=('query'))
    @marshal_with(google_map_route_model.GoogleMapResponse, code=200)
    def get(self, **kwargs):
        # 獲取查詢參數
        brand = kwargs.get('brand')
        region = kwargs.get('region')
        rating = kwargs.get('rating')
        
        # 建立基礎查詢
        query = Google_map2.query.filter_by(brand=brand)
        
        # 添加可選篩選條件
        if region:
            query = query.filter_by(region=region)
        if rating is not None:
            query = query.filter_by(rating=rating)
            
        # 執行查詢
        results = query.all()
        
        if not results:
            return util.failure({"message": "無符合條件的資料"})
            
        # 格式化結果
        data = []
        for item in results:
            data.append({
                "region": item.region,
                "brand": item.brand,
                "rating": item.rating,
                "count": item.count
            })
            
        return util.success(data)

class GoogleMapStatistics(MethodResource):
    @doc(description="獲取 Google Map 統計摘要資料，可依品牌和地區進行篩選", tags=["Google_map"])
    @use_kwargs(google_map_route_model.GoogleMapStatsFilterRequest, location=('query'))
    @marshal_with(google_map_route_model.GoogleMapResponse, code=200)
    def get(self, **kwargs):
        # 獲取查詢參數
        brand = kwargs.get('brand')
        region = kwargs.get('region')
        
        # 建立基礎查詢
        query = Google_map3.query.filter_by(brand=brand)
        
        # 添加可選篩選條件
        if region:
            query = query.filter_by(region=region)
            
        # 執行查詢
        results = query.all()
        
        if not results:
            return util.failure({"message": "無符合條件的資料"})
            
        # 格式化結果
        data = []
        for item in results:
            data.append({
                "region": item.region,
                "brand": item.brand,
                "rating_count": item.rating_count,
                "rating_mean": item.rating_mean,
                "rating_min": item.rating_min,  # 注意拼寫錯誤在原始模型中
                "rating_max": item.rating_max
            })
            
        return util.success(data)

class GoogleMapStoreRegion(MethodResource):
    @doc(description="獲取 Google Map 店鋪地區資料，可依品牌和地區進行篩選", tags=["Google_map"])
    @use_kwargs(google_map_route_model.GoogleMapStatsFilterRequest, location=('query'))
    @marshal_with(google_map_route_model.GoogleMapResponse, code=200)
    def get(self, **kwargs):
        # 獲取查詢參數
        brand = kwargs.get('brand')
        region = kwargs.get('region')
        
        # 建立基礎查詢
        query = Google_map4.query.filter_by(brand=brand)
        
        # 添加可選篩選條件
        if region:
            query = query.filter_by(region=region)
            
        # 執行查詢
        results = query.all()
        
        if not results:
            return util.failure({"message": "無符合條件的資料"})
            
        # 格式化結果
        data = []
        for item in results:
            data.append({
                "shop": item.shop,
                "region": item.region,
                "brand": item.brand
            })
            
        return util.success(data)