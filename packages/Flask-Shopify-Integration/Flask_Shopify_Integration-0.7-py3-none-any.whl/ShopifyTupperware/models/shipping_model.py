from marshmallow import Schema, fields
from ShopifyTupperware.models import price_model

class ShippingSchema(Schema):
    id  = fields.Integer()
    title  = fields.String()
    price  = fields.String()
    code  = fields.String()
    source  = fields.String()
    phone  = fields.String()
    requested_fulfillment_service_id  = fields.String()
    delivery_category  = fields.String()
    carrier_identifier  = fields.String()
    discounted_price  = fields.String()
    price_set  = fields.Nested(price_model.PriceSetSchema)
    discounted_price_set  = fields.Nested(price_model.PriceSetSchema)