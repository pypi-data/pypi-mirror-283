from marshmallow import Schema, fields


class ImageSchema(Schema):
    key = fields.Integer()
    id = fields.Integer()
    product_id = fields.Integer()
    position = fields.Integer()
    alt = fields.String()
    src = fields.String()
    width = fields.Integer()
    height = fields.Integer()
    created_at = fields.String()
    updated_at = fields.String()

class ProductImageSchema(Schema):
    key = fields.Integer()
    id = fields.Integer()
    product_id = fields.Integer()
    attachment = fields.String()
    filename = fields.String()
