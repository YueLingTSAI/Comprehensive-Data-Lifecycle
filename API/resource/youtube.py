from flask_apispec import MethodResource, marshal_with, doc, use_kwargs
import util
from . import youtube_route_model
from model import Youtube_cama, Youtube_louisa

####### API Action #########


class Youtube_camas(MethodResource):
    @doc(description="獲取Youtube上的cama資料", tags=["Youtube"])
    @use_kwargs(youtube_route_model.YoutubeFilterRequest, location=('query'))
    @marshal_with(youtube_route_model.YoutubeResponse, code=200)
    def get(self, **kwargs):
        # 獲取查詢參數
        topic = kwargs.get("topic")
        sentiment = kwargs.get('sentiment')
        
        # 建立基礎查詢
        query = Youtube_cama.query.filter_by(topic=topic)

        if sentiment:
            query = query.filter_by(sentiment=sentiment)
            
        # 執行查詢
        results = query.all()
        
        if not results:
            return util.failure({"message": "無符合條件的資料"})
            
        # 格式化結果
        data = []
        for item in results:
            data.append({
                "id": item.id,
                "content": item.content,
                "created_at": item.created_at,
                "sentiment_score": item.sentiment_score,
                "video_id": item.video_id
            })
            
        return util.success(data)
    
class Youtube_louisas(MethodResource):
    @doc(description="獲取Youtube上的louisa資料", tags=["Youtube"])
    @use_kwargs(youtube_route_model.YoutubeFilterRequest, location=('query'))
    @marshal_with(youtube_route_model.YoutubeResponse, code=200)
    def get(self, **kwargs):
        # 獲取查詢參數
        topic = kwargs.get("topic")
        sentiment = kwargs.get('sentiment')
        
        # 建立基礎查詢
        query = Youtube_cama.query.filter_by(topic=topic)

        if sentiment:
            query = query.filter_by(sentiment=sentiment)
            
        # 執行查詢
        results = query.all()
        
        if not results:
            return util.failure({"message": "無符合條件的資料"})
            
        # 格式化結果
        data = []
        for item in results:
            data.append({
                "id": item.id,
                "content": item.content,
                "created_at": item.created_at,
                "sentiment_score": item.sentiment_score,
                "video_id": item.video_id
            })
            
        return util.success(data)