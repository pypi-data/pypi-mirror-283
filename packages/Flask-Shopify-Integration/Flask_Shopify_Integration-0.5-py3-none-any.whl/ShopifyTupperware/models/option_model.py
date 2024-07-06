from marshmallow import Schema, fields

class OptionModel:
    pass

class OptionSchema(Schema):
    id = fields.Integer()
    product_id = fields.Integer()
    name = fields.String()
    position = fields.Integer()
    values = fields.List(fields.String)

class PropertySchema(Schema):
    name = fields.String()
    value = fields.String()

class ClientDetailSchema(Schema):
    browser_ip = fields.String()
    accept_language = fields.String()
    user_agent = fields.String()
    browser_width = fields.String()
    browser_height = fields.String()