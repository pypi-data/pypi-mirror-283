from ShopifyTupperware.data import db

_db = db.db

class WarantyAttachDb(_db.Model):
    __tablename__ = "waranty_attach"
    __table_args__ = {'implicit_returning':False}

    key = _db.Column(_db.BigInteger, primary_key=True)
    waranty_key =  _db.Column(_db.BigInteger, _db.ForeignKey('waranty.key'), nullable=False)
    image_url = _db.Column(_db.String)


class WarantyDb(_db.Model):
    __tablename__ = "waranty"
    __table_args__ = {'implicit_returning':False}

    key = _db.Column(_db.BigInteger, primary_key=True)
    name = _db.Column(_db.String)
    email = _db.Column(_db.String)
    phonenumber = _db.Column(_db.String)
    address= _db.Column(_db.String)
    product_series= _db.Column(_db.String)
    productname= _db.Column(_db.String)
    cookware_part = _db.Column(_db.String)
    product_melamine = _db.Column(_db.String)
    bagian_melamine = _db.Column(_db.String)
    product_difuser= _db.Column(_db.String)
    difuser_part= _db.Column(_db.String)
    alasan_klaim45 = _db.Column(_db.String)
    alasan_klaim = _db.Column(_db.String)
    alasan_klaim_difuser = _db.Column(_db.String)
    serialnumber= _db.Column(_db.String)
    ref_url= _db.Column(_db.String)
    status = _db.Column(_db.Integer)
    created_at = _db.Column(_db.String)
    updated_at = _db.Column(_db.String)
    attachments = _db.relationship('WarantyAttachDb', backref='waranty', lazy=True)

    @staticmethod
    def create_or_update(model):
        _db.session.add(model)
        _db.session.commit()
        return model


