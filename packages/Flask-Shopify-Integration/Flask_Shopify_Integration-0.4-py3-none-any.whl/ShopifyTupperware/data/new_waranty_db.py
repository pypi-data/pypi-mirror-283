from ShopifyTupperware.data import db

_db = db.db

class NewWarantyAttachDb(_db.Model):
    __tablename__ = "new_waranty_attach"
    __table_args__ = {'implicit_returning':False}

    key = _db.Column(_db.BigInteger, primary_key=True)
    waranty_key =  _db.Column(_db.BigInteger, _db.ForeignKey('new_waranty.key'), nullable=False)
    image_url = _db.Column(_db.String)

class NewWarantyDb(_db.Model):
    __tablename__ = "new_waranty"
    __table_args__ = {'implicit_returning':False}
    key= _db.Column(_db.BigInteger, primary_key=True)
    name= _db.Column(_db.String)
    sex= _db.Column(_db.String)
    email= _db.Column(_db.String)
    phone= _db.Column(_db.String)
    address= _db.Column(_db.String)
    provinsi= _db.Column(_db.String)
    city= _db.Column(_db.String)
    kecamatan= _db.Column(_db.String)
    desa= _db.Column(_db.String)
    kodepos= _db.Column(_db.String)
    product_series= _db.Column(_db.String)
    product_name= _db.Column(_db.String)
    product_part= _db.Column(_db.String)
    serial_no= _db.Column(_db.String)
    created_at= _db.Column(_db.String)
    created_by= _db.Column(_db.String)
    attachments = _db.relationship('NewWarantyAttachDb', backref='new_waranty', lazy=True)

    @staticmethod
    def validation(model):
        connection = db.engine.raw_connection()
        cursor = connection.cursor()
        try:
             cursor.execute('exec warantyValidation ?,?,?', [model.noKtp, model.email, model.phone])
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