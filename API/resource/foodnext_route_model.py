from marshmallow import Schema, fields


# 一般篩選條件
class FoodnextFilterRequest(Schema):
    classified = fields.Str(required=False, enum=["產品相關類", "品牌發展類", "市場趨勢類", "品牌類", "未分類"], description="文章分類")


# 一般回應模型
class FoodnextResponse(Schema):
    message = fields.Str(example="success")
    datetime = fields.Str(example="1970-01-01T00:00:00.000000")
    data = fields.List(fields.Dict())