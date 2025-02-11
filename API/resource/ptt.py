from flask_apispec import MethodResource, marshal_with, doc
import util
from . import ptt_route_model
from model import Ptt

####### API Action #########


class Ptts(MethodResource):
    # Get single by id
    @doc(description="Get Single Users info.", tags=["Ptt"])
    @marshal_with(ptt_route_model.PttSingleGetResponse, code=200)
    def get(self, id):
        ptt = Ptt.query.filter_by(id=id).first()
        if ptt is None:  # 錯誤處理
            return util.failure({"message": "Ptt not found"})

        ptt_info = {
            "id": ptt.id,
            "keyword": ptt.keyword,
            "article_title": ptt.article_title,
            "content_text": ptt.content_text,
            "content_type": ptt.content_type,
            "post_time": ptt.post_time,
            "crawl_time": ptt.crawl_time,
            "article_url": ptt.article_url,
            "comment_author": ptt.comment_author,
        }
        return util.success(ptt_info)