from marshmallow import Schema, fields

class CheckoutSchema(Schema):
    applied_discount = fields.Nested(AppliedDiscountSchema)
    billing_address = fields.Nested(CheckoutAddressSchema)
    buyer_accepts_marketing = fields.Boolean()
    created_at = fields.String()
    currency = fields.String()
    customer_id = fields.Integer()
    discount_code = fields.String()
    email = fields.String()
    gift_cards = fields.Nested(GiftCardSchema)
    line_items = fields.List(fields.Nested(CheckoutLineItemSchema))
    order = fields.Nested(CheckoutOrderSchema)
    payment_due = fields.Decimal()
    payment_url = fields.String()
    phone = fields.String()
    presentment_currency = fields.String()
    requires_shipping = fields.Boolean()
    reservation_time = fields.String()
    reservation_time_left = fields.Integer()
    shipping_address = fields.Nested(CheckoutAddressSchema)
    shipping_line = fields.Nested(CheckoutShippingLineSchema)
    shipping_rate = fields.Nested(CheckoutShippingRateSchema)
    source_name = fields.String()
    subtotal_price = fields.Decimal()
    tax_lines = fields.Nested(CheckoutTaxLineSchema)
    taxes_included = fields.Boolean()
    token = fields.String()
    total_price = fields.Decimal()
    total_tax = fields.Decimal()
    updated_at = fields.String()
    user_id = fields.Integer()
    web_url = fields.String()


class AppliedDiscountSchema(Schema):
    amount = fields.Decimal()
    title = fields.String()
    description = fields.String()
    value = fields.Decimal()
    value_type = fields.String()
    non_applicable_reason = fields.String()
    applicable = fields.Boolean()

class CheckoutAddressSchema(Schema):
    address1= fields.String()
    address2= fields.String()
    city = fields.String()
    company = fields.String()
    country = fields.String()
    first_name = fields.String()
    id = fields.String()
    last_name = fields.String()
    phone = fields.String()
    province = fields.String()
    zip = fields.String()
    province_code = fields.String()
    country_code = fields.String()

class GiftCardSchema(Schema):
    amount_used = fields.Decimal()
    balance = fields.Decimal()
    id = fields.Integer()
    last_characters = fields.String()

class CheckoutLineItemSchema(Schema):
    compare_at_price = fields.Decimal()
    fulfillment_service = fields.String()
    grams = fields.Float()
    id = fields.Integer()
    line_price = fields.Decimal()
    price = fields.Decimal()
    product_id = fields.Integer()
    quantity = fields.Integer()
    requires_shipping = fields.Boolean()
    sku = fields.String()
    taxable = fields.Boolean()
    title = fields.String()
    variant_id = fields.Integer()
    variant_title = fields.String()
    vendor = fields.String()

class CheckoutOrderSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    status_url = fields.String()

class CheckoutShippingLineSchema(Schema):
    handle = fields.String()
    price = fields.Decimal()
    title = fields.String()

class CheckoutShippingRateSchema(Schema):
    id = fields.String()
    price = fields.Decimal()
    title = fields.String()


class CheckoutTaxLineSchema(Schema):
    price = fields.Decimal()
    rate = fields.Float()
    title = fields.String()