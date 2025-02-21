from marshmallow import Schema, fields


# 一般篩選條件
class PttFilterRequest(Schema):
    # 定義搜尋欄位
    keyword = fields.Str(required=False, description="搜尋關鍵字")

# 一般回應模型
class PttResponse(Schema):
    message = fields.Str(example="success")
    datetime = fields.Str(example="1970-01-01T00:00:00.000000")
    data = fields.List(fields.Dict())