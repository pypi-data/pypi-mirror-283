from ShopifyTupperware.data.recruit_db import RecruitDb
from ShopifyTupperware import app
import datetime
import base64
import io
import os
from PIL import Image

class RecruitBloc:

    @staticmethod
    def save_image(file, filename):
        try:
            starter = file.find(',')
            image_data = file[starter+1:]
            image_data = bytes(image_data, encoding="ascii")
            file = Image.open(io.BytesIO(base64.b64decode(image_data)))
            file.save(os.path.join(app.config['BASE_DIR'], app.config['UPLOAD_FOLDER'], filename))
            return 1
        except Exception as ex:
            return -1




    @staticmethod
    def add_recruit(model):
        try:
            db = RecruitDb()
            db.name = model['q41_namaLengkap']
            db.identity_no = model['q28_noKtp28']
            db.sex = model['q39_jenisKelamin']
            db.email = model['q3_email3']
            db.phonenumber = model['q42_nomorTelepon']
            db.place_birth = model['q45_tempatLahir']
            db.date_birth = (model['q46_tanggalLahir']['day'] + "-" +
                             model['q46_tanggalLahir']['month'] + "-" +
                             model['q46_tanggalLahir']['year'])
            db.address = (model['q4_alamatKtp']['addr_line1']+ " "+
                          model['q4_alamatKtp']['addr_line2']+ " "+
                          model['q4_alamatKtp']['city'] #+ " "+
                          #model['q4_alamatKtp']['state']+ " "+
                          #model['q4_alamatKtp']['postal']#+ " "+
                          #model['q4_alamatKtp']['country']
                          )
            db.province= model['q38_propinsi']
            db.city= model['q4_alamatKtp']['city']
            db.postal= model['q35_kodePos']
            db.ship_address= (model['q36_alamatPengiriman36']['addr_line1']+ " "+
                              model['q36_alamatPengiriman36']['addr_line2']+ " "+
                              model['q36_alamatPengiriman36']['city'] #+ " "+
                              #model['q36_alamatPengiriman36']['state']+ " "+
                              #model['q36_alamatPengiriman36']['postal']#+ " "+
                              #model['q36_alamatPengiriman36']['country']
                              )
            db.ship_province= model['q40_propinsi40']
            db.ship_city= model['q36_alamatPengiriman36']['city']
            db.ship_postal= model['q37_kodePos37']

            db.check_sign = 'ACCEPTED'
            filename=model['q28_noKtp28'] + datetime.datetime.now().strftime('%Y%m%d%H%M%S') +'.png'
            RecruitBloc.save_image(model['q26_tandaTangan26'], filename)
            db.sign_img = app.config['UPLOAD_FOLDER'] + filename
            db.ref_url = model['q30_typeA30']
            db.identity_img = model['fotoKtpsim']
            db.created_at= datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
            RecruitDb.create_or_update(db)
            return 1
        except Exception as ex:
            return -1
