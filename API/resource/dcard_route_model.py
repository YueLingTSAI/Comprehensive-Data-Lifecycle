from marshmallow import Schema, fields


class DcardSingleGetResponse(Schema):
    message = fields.Str(example="success")
    datatime = fields.Str(example="1970-01-01T00:00:00.000000")
    data = fields.Dict()
