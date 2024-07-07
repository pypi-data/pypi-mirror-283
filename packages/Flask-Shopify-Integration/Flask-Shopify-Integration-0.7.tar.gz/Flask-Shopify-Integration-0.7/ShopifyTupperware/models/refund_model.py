from marshmallow import Schema, fields
from ShopifyTupperware.models import lineitem_model, price_model, transaction_model

class RefundLineItemSchema(Schema):
    id = fields.Integer()
    quantity = fields.Integer()
    line_item_id= fields.Integer()
    location_id = fields.Integer()
    restock_type = fields.String()
    subtotal = fields.Float()
    total_tax = fields.Float()
    subtotal_set = fields.Nested(price_model.PriceSetSchema)
    total_tax_set = fields.Nested(price_model.PriceSetSchema)
    line_item = fields.Nested(lineitem_model.LineItemSchema)

class RefundSchema(Schema):
    id = fields.Integer()
    order_id = fields.Integer()
    created_at = fields.String()
    note = fields.String()
    user_id = fields.Integer()
    processed_at = fields.String()
    restock = fields.Boolean()
    refund_line_items = fields.List(fields.Nested(RefundLineItemSchema))
    transactions = fields.List(fields.Nested(transaction_model.TransactionSchema))
    order_adjustments = fields.List(fields.String)