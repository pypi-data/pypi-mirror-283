from marshmallow import Schema, fields

class PaymentDetailSchema(Schema):
    credit_card_bin = fields.String()
    avs_result_code = fields.String()
    cvv_result_code = fields.String()
    credit_card_number = fields.String()
    credit_card_company = fields.String()