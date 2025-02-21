from flask_apispec import MethodResource, marshal_with, doc, use_kwargs
import util
from . import dcard_route_model
from model import Dcard
from sqlalchemy import extract
from datetime import datetime

####### API Action #########

class Dcards(MethodResource):
    @doc(description="獲取 Dcard 資料並進行篩選", tags=["Dcard"])
    @use_kwargs(dcard_route_model.DcardFilterRequest, location=('query'))
    @marshal_with(dcard_route_model.DcardResponse, code=200)
    def get(self, **kwargs):
        # 獲取查詢參數
        cafe = kwargs.get('cafe')
        post_date = kwargs.get('post_date')
        
        # 建立基礎查詢
        query = Dcard.query
        
        if cafe:
                query = query.filter_by(cafe=cafe)
                
        if post_date:
            # 將輸入的 YYYY-MM 轉換為 datetime 物件
            date_obj = datetime.strptime(post_date, '%Y-%m')
            # 使用 extract 來比對年份和月份
            query = query.filter(
                extract('year', Dcard.post_date) == date_obj.year,
                extract('month', Dcard.post_date) == date_obj.month
            )
            
        # 執行查詢
        results = query.all()
        
        if not results:
            return util.failure({"message": "無符合條件的資料"})
            
        # 格式化結果
        data = []
        for item in results:
            data.append({
                "id": item.id,
                "board": item.board,
                "content": item.content,
                "sentiment": item.sentiment,
                "sentiment_score": item.sentiment_score
            })
            
        return util.success(data)