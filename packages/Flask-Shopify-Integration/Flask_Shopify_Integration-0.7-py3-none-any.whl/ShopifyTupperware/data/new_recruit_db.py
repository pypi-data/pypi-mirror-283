from ShopifyTupperware.data import db

_db = db.db

class NewRecruitDb(_db.Model):
    __tablename__ = "new_recruit"
    __table_args__ = {'implicit_returning':False}
    key= _db.Column(_db.BigInteger, primary_key=True)
    fullname= _db.Column(_db.String)
    sex= _db.Column(_db.String)
    noKtp= _db.Column(_db.String)
    photoKtp= _db.Column(_db.String)
    email= _db.Column(_db.String)
    phone= _db.Column(_db.String)
    address= _db.Column(_db.String)
    provinsi= _db.Column(_db.String)
    city= _db.Column(_db.String)
    kecamatan= _db.Column(_db.String)
    desa= _db.Column(_db.String)
    kodepos= _db.Column(_db.String)
    address1= _db.Column(_db.String)
    provinsi1= _db.Column(_db.String)
    city1= _db.Column(_db.String)
    kecamatan1= _db.Column(_db.String)
    desa1= _db.Column(_db.String)
    kodepos1= _db.Column(_db.String)

    @staticmethod
    def validation(model):
        connection = db.engine.raw_connection()
        cursor = connection.cursor()
        try:
             cursor.execute('exec recruitValidation ?,?,?', [model.noKtp, model.email, model.phone])
             results = cursor.fetchall()
             items = [dict(zip([key[0] for key in cursor.description], row)) for row in results]
             return items
        except Exception as ex:
            raise ex
        finally:
            cursor.close()
            connection.close()



    @staticmethod
    def create_or_update(model):
        _db.session.add(model)
        _db.session.commit()
        return model