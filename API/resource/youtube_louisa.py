from flask_apispec import MethodResource, marshal_with, doc
import util
from . import youtube_louisa_route_model
from model import Youtube_louisa

####### API Action #########


class Youtube_louisas(MethodResource):
    # Get single by id
    @doc(description="Get Single Users info.", tags=["Youtube"])
    @marshal_with(youtube_louisa_route_model.Youtube_louisaSingleGetResponse, code=200)
    def get(self, id):
        youtube_louisa = Youtube_louisa.query.filter_by(id=id).first()
        if youtube_louisa is None:  # 錯誤處理
            return util.failure({"message": "Youtube_louisa not found"})

        youtube_louisa_info = {
            "id": youtube_louisa.id,
            "video_id": youtube_louisa.video_id,
            "content": youtube_louisa.content,
            "author": youtube_louisa.author,
            "like_count": youtube_louisa.like_count,
            "created_at": youtube_louisa.created_at,
        }
        return util.success(youtube_louisa_info)
