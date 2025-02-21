from marshmallow import Schema, fields


# 一般篩選條件
class YoutubeFilterRequest(Schema):
    topic = fields.Str(required=False, enum=["品質", "服務", "價格", "環境", "其他"], description="主題")
    sentiment = fields.Str(required=False, enum=["強烈正面", "正面", "中性", "負面", "強烈負面"], description="回饋")


# 一般回應模型
class YoutubeResponse(Schema):
    message = fields.Str(example="success")
    datetime = fields.Str(example="1970-01-01T00:00:00.000000")
    data = fields.List(fields.Dict())