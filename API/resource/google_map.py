from flask_apispec import MethodResource, marshal_with, doc
import util
from . import google_map_route_model
from model import Google_map

####### API Action #########


class Google_maps(MethodResource):
    # Get single by id
    @doc(description="Get Single Users info.", tags=["Google_map"])
    @marshal_with(google_map_route_model.Google_mapSingleGetResponse, code=200)
    def get(self, id):
        google_map = Google_map.query.filter_by(id=id).first()
        if google_map is None:  # 錯誤處理
            return util.failure({"message": "Google_map not found"})

        google_map_info = {
            "id": google_map.id,
            "brand": google_map.brand,
            "store_name": google_map.store_name,
            "rating":google_map.rating,
            "content": google_map.content,
        }
        return util.success(google_map_info)