from flask_apispec import MethodResource, marshal_with, doc
import util
from . import youtube_cama_route_model
from model import Youtube_cama

####### API Action #########


class Youtube_camas(MethodResource):
    # Get single by id
    @doc(description="Get Single Users info.", tags=["Youtube"])
    @marshal_with(youtube_cama_route_model.Youtube_camaSingleGetResponse, code=200)
    def get(self, id):
        youtube_cama = Youtube_cama.query.filter_by(id=id).first()
        if youtube_cama is None:  # 錯誤處理
            return util.failure({"message": "Youtube_cama not found"})

        youtube_cama_info = {
            "id": youtube_cama.id,
            "video_id": youtube_cama.video_id,
            "content": youtube_cama.content,
            "author": youtube_cama.author,
            "like_count": youtube_cama.like_count,
            "created_at": youtube_cama.created_at,
        }
        return util.success(youtube_cama_info)