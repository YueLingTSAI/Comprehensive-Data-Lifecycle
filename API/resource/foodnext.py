from flask_apispec import MethodResource, marshal_with, doc, use_kwargs
import util
from . import foodnext_route_model
from model import Foodnext_cama, Foodnext_louisa

####### API Action #########


class Foodnext_camas(MethodResource):
    @doc(description="獲取 Foodnext 資料並進行篩選", tags=["Foodnext"])
    @use_kwargs(foodnext_route_model.FoodnextFilterRequest, location=('query'))
    @marshal_with(foodnext_route_model.FoodnextResponse, code=200)
    def get(self, **kwargs):
        # 獲取查詢參數
        classified = kwargs.get('classified')
        
        # 建立基礎查詢
        query = Foodnext_cama.query.filter_by(classified=classified)
            
        # 執行查詢
        results = query.all()
        
        if not results:
            return util.failure({"message": "無符合條件的資料"})
            
        # 格式化結果
        data = []
        for item in results:
            data.append({
                "id": item.id,
                "title": item.title,
                "url": item.url,
                "content": item.content
            })
            
        return util.success(data)

class Foodnext_louisas(MethodResource):
    @doc(description="獲取 Foodnext 資料並進行篩選", tags=["Foodnext"])
    @use_kwargs(foodnext_route_model.FoodnextFilterRequest, location=('query'))
    @marshal_with(foodnext_route_model.FoodnextResponse, code=200)
    def get(self, **kwargs):
        # 獲取查詢參數
        classified = kwargs.get('classified')
        
        # 建立基礎查詢
        query = Foodnext_louisa.query.filter_by(classified=classified)
            
        # 執行查詢
        results = query.all()
        
        if not results:
            return util.failure({"message": "無符合條件的資料"})
            
        # 格式化結果
        data = []
        for item in results:
            data.append({
                "id": item.id,
                "title": item.title,
                "url": item.url,
                "content": item.content
            })
            
        return util.success(data)