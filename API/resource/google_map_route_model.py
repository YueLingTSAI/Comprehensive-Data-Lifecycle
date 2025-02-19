from marshmallow import Schema, fields

# 一般篩選條件 (包含評分)
class GoogleMapFilterRequest(Schema):
    brand = fields.Str(required=True, enum=["Cama", "Louisa"], description="品牌名稱")
    region = fields.Str(required=False, enum=["北部", "中部", "南部", "東部", "外島"], description="地區")
    rating = fields.Str(required=False, enum=["1", "2", "3", "4", "5"], description="評分")

# 沒有評分的篩選條件 (用於統計和店鋪)
class GoogleMapStatsFilterRequest(Schema):
    brand = fields.Str(required=True, enum=["Cama", "Louisa"], description="品牌名稱")
    region = fields.Str(required=False, enum=["北部", "中部", "南部", "東部", "外島"], description="地區")

# 一般回應模型
class GoogleMapResponse(Schema):
    message = fields.Str(example="success")
    datetime = fields.Str(example="1970-01-01T00:00:00.000000")
    data = fields.List(fields.Dict())