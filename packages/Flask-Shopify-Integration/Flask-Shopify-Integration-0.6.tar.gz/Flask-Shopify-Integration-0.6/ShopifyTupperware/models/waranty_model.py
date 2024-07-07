import json
from marshmallow import Schema, fields, post_dump, pre_dump, ValidationError


class WarantyFormData(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        return "".join(str(d) for d in value)

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            obj= json.loads(value)
            return obj
        except ValueError as error:
            raise ValidationError("Form Data Error.") from error

class WarantyAttachment(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ""
        return "".join(str(d) for d in value)

    def _deserialize(self, value, attr, data, **kwargs):
        try:
            obj= json.loads(value)
            return obj
        except ValueError as error:
            raise ValidationError("Attachment Error.") from error



class WarantyFormSchema(Schema):
    productid= fields.String()
    address= fields.String()
    alasanclaim= fields.String()

class WarantyAttachSchema(Schema):
    file_1= fields.String(attribute="file-1")


#class WarantySchemaData(Schema):
#    shop_id= fields.String()
#    form_id= fields.String()
#    name= fields.String()
#    email= fields.String()
#    subject= fields.String()
#    message= fields.String()
#    form_data= WarantyFormData(data_key="form_data")
#    attachments= WarantyAttachment(data_key="attachments")
#    created_at= fields.String()
#    updated_at= fields.String()
#    status= fields.Integer()

class WarantySchemaData(Schema):
    shop_id= fields.String()
    form_id= fields.String()
    name= fields.String()
    email= fields.String()
    subject= fields.String()
    message= fields.String()
    form_data= fields.Nested(WarantyFormSchema)
    attachments= fields.Nested(WarantyAttachSchema)
    created_at= fields.String()
    updated_at= fields.String()
    status= fields.Integer()

class WarantySchema(Schema):
    data= fields.Nested(WarantySchemaData)

#class WarantySchema(Schema):
#    data= fields.Nested(WarantySchemaData)



class Q32Name(Schema):
    first = fields.String()
    last = fields.String()

class Q12Alamat(Schema):
    addr_line1 = fields.String()
    addr_line2 = fields.String()
    city = fields.String()
    state = fields.String()
    postal = fields.String()
    country = fields.String()

class TempUpload(Schema):
    q43_input43 = fields.List(fields.String())


class ClaimWarantySchema(Schema):
    q32_nama = fields.Nested(Q32Name)
    q31_email_cust = fields.String(attribute="q31_email-cust")
    q25_telepon = fields.String()
    q12_alamat= fields.Nested(Q12Alamat)
    q38_productSeries = fields.String()
    q39_productName = fields.String()
    q47_cookwarePart = fields.String()
    q40_productMelamine = fields.String()
    q49_bagianMelamine = fields.String()
    q45_alasanKlaim45 = fields.String()
    q48_alasanKlaim = fields.String()
    q44_typeA44 = fields.String()
    q36_typeA = fields.String()
    event_id = fields.String()
    temp_upload = fields.Nested(TempUpload)
    file_server = fields.String()
    input43 = fields.List(fields.String())




    ##NEW MAPPING SCHEMA

class LimitedCustomerFullName(Schema):
        first= fields.String()
        last= fields.String()

class LimitedCustomerAddress(Schema):
        addr_line1= fields.String()
        addr_line2= fields.String()
        city= fields.String()
        state= fields.String()
        postal= fields.String()
        country= fields.String()

class LimitedWarantySchema(Schema):
        q6_namaLengkap6= fields.Nested(LimitedCustomerFullName)
        q7_emailAktif7= fields.String()
        q8_nomorHp= fields.String()
        q9_alamatsesuai= fields.Nested(LimitedCustomerAddress)
        q10_productSeries= fields.String()
        q5_cookwareSeries5= fields.String()
        q11_melamineSeries= fields.String()
        q21_diffuserSeries= fields.String()
        q12_alasanClaim= fields.String() #cookware
        q13_alasanClaim13= fields.String() #melamine
        q22_alasanClaim22= fields.String() #diffuser
        q15_serialNumber= fields.String()
        input16= fields.List(fields.String())
        input17= fields.List(fields.String())
#class LimitedWarantySchema(Schema):
#        q6_namaLengkap= fields.Nested(LimitedCustomerFullName)
#        q7_email= fields.String()
#        q8_telepon= fields.String()
#        q9_address= fields.Nested(LimitedCustomerAddress)
#        q10_productSeries= fields.String()
#        q5_cookwareSeries5= fields.String()
#        q11_melamineSeries= fields.String()
#        q12_alasanClaim= fields.String()
#        q13_alasanClaim13= fields.String()
#        q15_serialNumber= fields.String()
#        input16= fields.List(fields.String())
#        input17= fields.List(fields.String())







