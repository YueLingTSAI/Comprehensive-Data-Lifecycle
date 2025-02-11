from flask_apispec import MethodResource, marshal_with, doc
import util
from . import foodnext_cama_route_model
from model import Foodnext_cama

####### API Action #########


class Foodnext_camas(MethodResource):
    # Get single by id
    @doc(description="Get Single Users info.", tags=["Foodnext"])
    @marshal_with(foodnext_cama_route_model.Foodnext_camaSingleGetResponse, code=200)
    def get(self, id):
        foodnext_cama = Foodnext_cama.query.filter_by(id=id).first()
        if foodnext_cama is None:  # 錯誤處理
            return util.failure({"message": "Foodnext_cama not found"})

        foodnext_cama_info = {
            "id": foodnext_cama.id,
            "title": foodnext_cama.title,
            "url": foodnext_cama.url,
            "date": foodnext_cama.date,
            "content": foodnext_cama.content,
        }
        return util.success(foodnext_cama_info)