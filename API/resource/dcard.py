from flask_apispec import MethodResource, marshal_with, doc
import util
from . import dcard_route_model
from model import Dcard

####### API Action #########


class Dcards(MethodResource):
    # Get single by id
    @doc(description="Get Single Users info.", tags=["Dcard"])
    @marshal_with(dcard_route_model.DcardSingleGetResponse, code=200)
    def get(self, id):
        dcard = Dcard.query.filter_by(id=id).first()
        if dcard is None:  # 錯誤處理
            return util.failure({"message": "Dcard not found"})
        
        dcard_info = {
            "id": dcard.id,
            "cafe": dcard.cafe,
            "title": dcard.title,
            "link": dcard.link,
            "content": dcard.content,
            "source": dcard.source,
            "search_date": dcard.search_date,
        }
        return util.success(dcard_info)