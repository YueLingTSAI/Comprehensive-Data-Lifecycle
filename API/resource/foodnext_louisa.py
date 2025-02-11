from flask_apispec import MethodResource, marshal_with, doc
import util
from . import foodnext_louisa_route_model
from model import Foodnext_louisa

####### API Action #########


class Foodnext_louisas(MethodResource):
    # Get single by id
    @doc(description="Get Single Users info.", tags=["Foodnext"])
    @marshal_with(foodnext_louisa_route_model.Foodnext_louisaSingleGetResponse, code=200)
    def get(self, id):
        foodnext_louisa = Foodnext_louisa.query.filter_by(id=id).first()
        if foodnext_louisa is None:  # 錯誤處理
            return util.failure({"message": "Foodnext_louisa not found"})

        foodnext_louisa_info = {
            "id": foodnext_louisa.id,
            "title": foodnext_louisa.title,
            "url": foodnext_louisa.url,
            "date": foodnext_louisa.date,
            "content":foodnext_louisa.content
        }
        return util.success(foodnext_louisa_info)