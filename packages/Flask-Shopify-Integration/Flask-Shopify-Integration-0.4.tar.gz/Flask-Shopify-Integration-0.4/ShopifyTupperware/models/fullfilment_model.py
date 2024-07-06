from marshmallow import Schema, fields
from ShopifyTupperware.models import receipt_model, lineitem_model

class FullfilmentSchema(Schema):
    id = fields.Integer()
    order_id = fields.Integer()
    status = fields.String()
    created_at = fields.String()
    service = fields.String()
    updated_at = fields.String()
    tracking_company = fields.String()
    shipment_status = fields.String()
    location_id = fields.Integer()
    tracking_number = fields.String()
    tracking_numbers = fields.List(fields.String)
    tracking_url = fields.String()
    tracking_urls = fields.List(fields.String)
    receipt = fields.Nested(receipt_model.ReceiptSchema)
    name = fields.String()
    notify_customer = fields.Boolean()
    line_items = fields.List(fields.Nested(lineitem_model.LineItemSchema))

    
class LineItemFulfillmentOrderDetailSchema(Schema):
    id = fields.Integer()
    quantity = fields.Integer()

class LineItemFulfillmentOrderSchema(Schema):
    fulfillment_order_id = fields.Integer()
    fulfillment_order_line_items = fields.List(fields.Nested(LineItemFulfillmentOrderDetailSchema))

    
class TrackingInfoSchema(Schema):
    company = fields.String()
    number = fields.String()
    url = fields.String()


class OriginAddressSchema(Schema):
    address1 = fields.String()
    address2 = fields.String()
    city = fields.String()
    country_code = fields.String()
    province_code = fields.String()
    zip = fields.String()

class FulfillmentV2Schema(Schema):
    line_items_by_fulfillment_order = fields.List(fields.Nested(LineItemFulfillmentOrderSchema))
    message = fields.String()
    notify_customer = fields.Boolean()
    tracking_info = fields.Nested(TrackingInfoSchema)
    origin_address = fields.Nested(OriginAddressSchema)



class FulfillmentOrderLineItemSchema(Schema):
    id= fields.Integer()
    shop_id= fields.Integer()
    fulfillment_order_id= fields.Integer()
    quantity= fields.Integer()
    line_item_id= fields.Integer()
    inventory_item_id= fields.Integer()
    fulfillable_quantity= fields.Integer()
    variant_id= fields.Integer()

class FulfillmentOrderDestinationSchema(Schema):
    id= fields.Integer()
    address1= fields.String()
    address2= fields.String()
    city= fields.String()
    company= fields.String()
    country= fields.String()
    email= fields.String()
    first_name= fields.String()
    last_name= fields.String()
    phone= fields.String()
    province= fields.String()
    zip= fields.String()

class FulfillmentHoldSchema(Schema):
    reason = fields.String()
    reason_notes = fields.String()

class DeliveryMethodSchema(Schema):
    id= fields.Integer()
    method_type= fields.String()
    min_delivery_date_time= fields.String()
    max_delivery_date_time= fields.String()

class AssignedLocationSchema(Schema):
    address1= fields.String()
    address2= fields.String()
    city= fields.String()
    country_code= fields.String()
    location_id = fields.Integer()
    name = fields.String()
    phone = fields.String()
    province = fields.String()
    zip= fields.String()

class FulfillmentOrderSchema(Schema):
    id = fields.Integer()
    shop_id = fields.Integer()
    order_id = fields.Integer()
    assigned_location_id = fields.Integer()
    request_status = fields.String()
    status = fields.String()
    supported_actions = fields.List(fields.String)
    destination = fields.Nested(FulfillmentOrderDestinationSchema)
    line_items = fields.List(fields.Nested(FulfillmentOrderLineItemSchema))
    fulfill_at = fields.String()
    fulfill_by = fields.String()
    international_duties = fields.String()
    fulfillment_holds = fields.List(fields.Nested(FulfillmentHoldSchema))
    delivery_method = fields.Nested(DeliveryMethodSchema)
    created_at = fields.String()
    updated_at = fields.String()
    assigned_location: fields.Nested(AssignedLocationSchema)

class FulfillmentOrderRootSchema(Schema):
    fulfillment_orders = fields.List(fields.Nested(FulfillmentOrderSchema))