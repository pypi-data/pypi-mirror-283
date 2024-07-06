from marshmallow import Schema, fields
from ShopifyTupperware.models import price_model, option_model


class TaxLineSchema(Schema):
    title = fields.String()
    price = fields.Float()
    rate = fields.String()
    price_set = fields.Nested(price_model.PriceSetSchema)

class DiscountAllocation(Schema):
    amount= fields.Float()
    discount_application_index= fields.Integer()



class LineItemSchema(Schema):
     id = fields.Integer()
     variant_id = fields.Integer()
     title = fields.String()
     quantity = fields.Float()
     sku = fields.String()
     variant_title = fields.String()
     vendor = fields.String()
     fulfillment_service = fields.String()
     product_id = fields.Integer()
     requires_shipping = fields.Boolean()
     taxable = fields.Boolean()
     gift_card = fields.String()
     name = fields.String()
     variant_inventory_management = fields.String()
     properties = fields.List(fields.Nested(option_model.PropertySchema))
     product_exists = fields.Boolean()
     fulfillable_quantity = fields.Integer()
     grams = fields.Integer()
     price = fields.Float()
     total_discount = fields.Float()
     fulfillment_status = fields.String()
     price_set = fields.Nested(price_model.PriceSetSchema)
     total_discount_set = fields.Nested(price_model.PriceSetSchema)
     discount_allocations = fields.List(fields.Nested(DiscountAllocation))
     tax_lines = fields.List(fields.Nested(TaxLineSchema))