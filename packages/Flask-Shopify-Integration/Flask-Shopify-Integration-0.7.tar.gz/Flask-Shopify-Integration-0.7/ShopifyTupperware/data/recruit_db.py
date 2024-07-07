from ShopifyTupperware.data import db

_db = db.db

class RecruitDb(_db.Model):
    __tablename__ = "recruit"
    __table_args__ = {'implicit_returning':False}

    key = _db.Column(_db.BigInteger, primary_key=True)
    name = _db.Column(_db.String)
    sex = _db.Column(_db.String)
    email = _db.Column(_db.String)
    phonenumber = _db.Column(_db.String)
    place_birth = _db.Column(_db.String)
    date_birth = _db.Column(_db.String)
    address= _db.Column(_db.String)
    province= _db.Column(_db.String)
    city= _db.Column(_db.String)
    postal= _db.Column(_db.String)
    ship_address= _db.Column(_db.String)
    ship_province= _db.Column(_db.String)
    ship_city= _db.Column(_db.String)
    ship_postal= _db.Column(_db.String)
    identity_no =_db.Column(_db.String)
    check_sign= _db.Column(_db.String)
    sign_img= _db.Column(_db.String)
    ref_url= _db.Column(_db.String)
    identity_img = _db.Column(_db.String)
    created_at = _db.Column(_db.String)
    updated_at = _db.Column(_db.String)


    @staticmethod
    def create_or_update(model):
        _db.session.add(model)
        _db.session.commit()
        return model


