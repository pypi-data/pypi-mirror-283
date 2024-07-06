from marshmallow import Schema, fields, post_load


class CollectionImageModel(Schema):
    src: fields.String()

class CollectionModel(Schema):
    id = fields.Integer()
    body_html = fields.String()
    handle = fields.String()
    image = fields.String(attribute='image.src')#fields.Nested(CollectionImageModel)
    handle = fields.String()
    published = fields.Boolean()
    published_at = fields.String()
    published_scope = fields.String()
    sort_order = fields.String()
    title = fields.String()
    updated_at = fields.String()


