from marshmallow import Schema, fields

class FullName(Schema):
    first= fields.String()
    last= fields.String()

class HandphoneNo(Schema):
    area= fields.String()
    phone= fields.String()

class FullAddress(Schema):
    addr_line1= fields.String()
    addr_line2= fields.String()
    city= fields.String()
    state= fields.String()
    postal= fields.String()
    country= fields.String()

class TgLahir(Schema):
    day = fields.String()
    month = fields.String()
    year = fields.String()


class RecruitSchema(Schema):
    q41_namaLengkap= fields.String()
    q39_jenisKelamin= fields.String()
    q28_noKtp28= fields.String()
    q3_email3= fields.String()
    q42_nomorTelepon=fields.String()
    q45_tempatLahir=fields.String()
    q46_tanggalLahir=fields.Nested(TgLahir)
    q4_alamatKtp= fields.Nested(FullAddress)
    q38_propinsi= fields.String()
    q35_kodePos= fields.String()
    q36_alamatPengiriman36= fields.Nested(FullAddress)
    q40_propinsi40= fields.String()
    q37_kodePos37= fields.String()
    q24_typeA24= fields.String()
    q26_typeA= fields.String()
    q26_tandaTangan26= fields.String()
    q30_typeA30= fields.String()
    fotoKtpsim= fields.String()

#class RecruitSchema(Schema):
#    q2_fullName2= fields.Nested(FullName)
#    q28_noKtp28= fields.String()
#    q39_jenisKelamin= fields.String()
#    q3_email3= fields.String()
#    q27_nomorHandphone=fields.Nested(HandphoneNo)
#    q4_alamatKtp= fields.Nested(FullAddress)
#    q38_propinsi= fields.String()
#    q35_kodePos= fields.String()
#    q36_alamatPengiriman36= fields.Nested(FullAddress)
#    q40_propinsi40= fields.String()
#    q37_kodePos37= fields.String()
#    q24_typeA24= fields.String()
#    q26_typeA= fields.String()
#    q30_typeA30= fields.String()
#    fotoKtpsim= fields.String()


