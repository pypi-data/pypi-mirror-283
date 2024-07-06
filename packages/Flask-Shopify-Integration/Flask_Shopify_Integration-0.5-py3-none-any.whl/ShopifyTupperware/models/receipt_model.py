from marshmallow import Schema, fields

class ReceiptSchema(Schema):
    testcase = fields.Boolean()
    authorization = fields.String()