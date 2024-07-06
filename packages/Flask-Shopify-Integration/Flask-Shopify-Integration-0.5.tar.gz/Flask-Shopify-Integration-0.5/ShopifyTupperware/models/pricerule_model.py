from marshmallow import Schema, fields

class PriceRuleSchema(Schema):
    allocation_method= fields.String()
    #created_at= fields.String()
    #updated_at= fields.String()
    customer_selection= fields.String()
    ends_at= fields.String()
    entitled_collection_ids= fields.List(fields.Integer())##
    #entitled_product_ids= fields.List(fields.Integer())##
    #entitled_variant_ids= fields.List(fields.Integer())##
    id= fields.Integer()
    once_per_customer= fields.Boolean()
    prerequisite_customer_ids= fields.List(fields.Float())##
    #customer_segment_prerequisite_ids= fields.List(fields.Integer())##
    starts_at= fields.String()
    target_selection= fields.String()
    target_type= fields.String()
    title= fields.String()
    usage_limit= fields.Integer()
    #prerequisite_product_ids= fields.List(fields.Integer())##
    #prerequisite_variant_ids= fields.List(fields.Integer())##
    #prerequisite_collection_ids= fields.List(fields.Integer())##
    value= fields.Integer()
    value_type= fields.String()
    allocation_limit= fields.Integer()
    
    #prerequisite_quantity_range: Optional[PrerequisiteQuantityRange]
    #prerequisite_shipping_price_range: Optional[PrerequisiteShippingPriceRange]
    #prerequisite_subtotal_range: Optional[PrerequisiteSubtotalRange]
    #prerequisite_to_entitlement_purchase: Optional[PrerequisiteToEntitlementPurchase]
    #prerequisite_to_entitlement_quantity_ratio: Optional[PrerequisiteToEntitlementQuantityRatio]