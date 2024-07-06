from marshmallow import Schema, fields

class LocationSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    address1 = fields.String()
    address2 = fields.String()
    city = fields.String()
    zip = fields.String()
    province = fields.String()
    country = fields.String()
    phone = fields.String()
    created_at = fields.String()
    updated_at = fields.String()
    country_code = fields.String()
    country_name = fields.String()
    province_code = fields.String()
    legacy = fields.Boolean()
    active = fields.Boolean()