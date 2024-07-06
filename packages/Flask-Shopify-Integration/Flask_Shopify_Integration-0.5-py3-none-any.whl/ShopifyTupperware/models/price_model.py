from marshmallow import Schema, fields

class PriceSchema(Schema):
    currency_code = fields.String()
    amount = fields.Float()

class PresentmentPriceSchema(Schema):
    price = fields.Nested(PriceSchema)
    compare_at_price = fields.String()

class PriceSetSchema(Schema):
    shop_money = fields.Nested(PriceSchema)
    presentment_money = fields.Nested(PriceSchema)

class DiscountPriceSchema(Schema):
    code = fields.String()
    amount = fields.String()
    type = fields.String()

class DiscountApplicationPriceSchema(Schema):
    type = fields.String()
    value = fields.String()
    value_type = fields.String()
    allocation_method = fields.String()
    target_selection = fields.String()
    target_type = fields.String()
    code = fields.String()
    title= fields.String()
