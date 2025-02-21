from marshmallow import Schema, fields, validate

# 一般篩選條件
class DcardFilterRequest(Schema):
    cafe = fields.Str(required=True, enum=["CAMA", "路易莎"], description="品牌名稱")
    post_date = fields.Str(
    required=False, 
    description="日期 (格式：YYYY-MM)",
    validate=validate.Regexp(r'^\d{4}-\d{2}$', error="日期格式必須為 YYYY-MM")
)

# 一般回應模
class DcardResponse(Schema):
    message = fields.Str(example="success")
    datetime = fields.Str(example="1970-01-01T00:00:00.000000")
    data = fields.List(fields.Dict())