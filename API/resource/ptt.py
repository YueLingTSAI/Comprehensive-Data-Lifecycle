from flask_apispec import MethodResource, marshal_with, doc, use_kwargs
import util
from . import ptt_route_model
from model import Ptt

####### API Action #########


class Ptts(MethodResource):
    @doc(description="根據關鍵字搜尋 Ptt 內容", tags=["Ptt"])
    @use_kwargs(ptt_route_model.PttFilterRequest, location=('query'))
    @marshal_with(ptt_route_model.PttResponse, code=200)
    def get(self, **kwargs):
        # 獲取關鍵字參數
        keyword = kwargs.get('keyword')
        
        # 建立查詢
        query = Ptt.query
        
        # 如果提供了關鍵字，進行內容搜尋
        if keyword:
            query = query.filter(Ptt.content_text.contains(keyword))
            
        # 執行查詢
        results = query.all()
        
        if not results:
            return util.failure({"message": "無符合條件的資料"})
            
        # 格式化結果，只返回需要的欄位
        data = []
        for item in results:
            data.append({
                "id": item.id,
                "content_text": item.content_text,
                "board": item.board,
                "content_type": item.content_type
            })
            
        return util.success(data)