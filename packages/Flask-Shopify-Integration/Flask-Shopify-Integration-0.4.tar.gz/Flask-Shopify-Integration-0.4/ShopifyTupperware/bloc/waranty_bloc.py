from ShopifyTupperware.data.waranty_db import WarantyDb, WarantyAttachDb
import datetime

class WarantyBloc:

    @staticmethod
    def add_limited_waranty(model):
        try:
            db = WarantyDb()
            db.name = model['q6_namaLengkap6']['first'] + " " + model['q6_namaLengkap6']['last']
            db.email = model['q7_emailAktif7']
            db.phonenumber = model['q8_nomorHp']
            db.address = (model['q9_alamatsesuai']['addr_line1'] + " "+
                        #model['q9_alamatsesuai']['addr_line2'] + " "+
                        model['q9_alamatsesuai']['city'] + " "+
                        model['q9_alamatsesuai']['state']+ " - "+
                        model['q9_alamatsesuai']['postal']+ " " #+
                        #model['q9_alamatsesuai']['country']
                        )
            db.product_series=model['q10_productSeries']

            if 'q5_cookwareSeries5' in model and str(model['q5_cookwareSeries5']) != "" and  model['q5_cookwareSeries5'] is not None:
                db.productname = str(model['q5_cookwareSeries5']).split(sep='\r\n')[0]
                db.cookware_part= str(model['q5_cookwareSeries5']).split(sep='\r\n')[1]

            if 'q21_diffuserSeries' in model and str(model['q21_diffuserSeries']) != "" and model['q21_diffuserSeries'] is not None:
                db.product_difuser = model['q21_diffuserSeries']

            if 'q11_melamineSeries' in model and str(model['q11_melamineSeries']) != "" and model['q11_melamineSeries'] is not None:
                db.product_melamine = str(model['q11_melamineSeries']).split(sep='\r\n')[0]
                db.bagian_melamine= str(model['q11_melamineSeries']).split(sep='\r\n')[1]

            if 'q12_alasanClaim' in model and model['q12_alasanClaim'] is not None:
                db.alasan_klaim45 = model['q12_alasanClaim']#cookware

            if 'q13_alasanClaim13' in model and model['q13_alasanClaim13'] is not None:
                db.alasan_klaim = model['q13_alasanClaim13']#melamine

            if 'q22_alasanClaim22' in model and model['q22_alasanClaim22'] is not None:
                db.alasan_klaim_difuser = model['q22_alasanClaim22']#difuser

            db.serialnumber= model['q15_serialNumber']
            db.ref_url=''
            db.status= 0
            db.created_at= datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
            for img in model['input16']:
                d_db = WarantyAttachDb()
                d_db.image_url = img
                db.attachments.append(d_db)
            for img in model['input17']:
                d_db = WarantyAttachDb()
                d_db.image_url = img
                db.attachments.append(d_db)
            WarantyDb.create_or_update(db)
            return 1
        except Exception as ex:
            return -1

            



    @staticmethod
    def add_waranty(model):
        try:
            db = WarantyDb()
            db.name = model['q32_nama']['first'] + " " + model['q32_nama']['last']
            db.email = model['q31_email_cust']
            db.phonenumber = model['q25_telepon']
            db.address = (model['q12_alamat']['addr_line1'] + " "+
                          model['q12_alamat']['addr_line2'] + " "+
                          model['q12_alamat']['city'] + " "+
                          model['q12_alamat']['state']+ " - "+
                          model['q12_alamat']['postal']+ " "+
                          model['q12_alamat']['country']
                          )
            db.product_series = model['q38_productSeries']
            db.productname = model['q39_productName']
            db.cookware_part = model['q47_cookwarePart']
            db.product_melamine = model['q40_productMelamine']
            db.bagian_melamine = model['q49_bagianMelamine']
            db.alasan_klaim45 = model['q45_alasanKlaim45']
            db.alasan_klaim = model['q48_alasanKlaim']
            db.serialnumber = model['q44_typeA44']
            db.ref_url = model['q36_typeA']
            db.status= 0
            db.created_at= datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
            for img in model['input43']:
                d_db = WarantyAttachDb()
                d_db.image_url = img
                db.attachments.append(d_db)
            WarantyDb.create_or_update(db)
            return 1
        except Exception as ex:
            return -1
        