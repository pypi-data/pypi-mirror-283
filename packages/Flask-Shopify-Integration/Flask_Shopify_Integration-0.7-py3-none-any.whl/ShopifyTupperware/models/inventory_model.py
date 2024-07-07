from marshmallow import Schema, fields

class InventoryItemSchema(Schema):
    id= fields.Integer()
    sku= fields.String()
    created_at= fields.String()
    updated_at= fields.String()
    requires_shipping= fields.Boolean()
    cost= fields.Float()
    country_code_of_origin= fields.String()
    province_code_of_origin= fields.String()
    harmonized_system_code= fields.String()
    tracked= fields.Boolean()
    country_harmonized_system_codes= fields.List(fields.String)

class InventoryLevelSchema(Schema):
    inventory_item_id= fields.Integer()
    location_id= fields.Integer()
    available= fields.Integer()
    updated_at= fields.String()