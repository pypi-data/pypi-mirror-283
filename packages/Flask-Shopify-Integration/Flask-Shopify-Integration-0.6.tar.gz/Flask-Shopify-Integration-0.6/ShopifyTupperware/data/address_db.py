from ShopifyTupperware.data import db

_db = db.db

class AddressDb(_db.Model):

    __tablename__ = "address"
    __table_args__ = {'implicit_returning':False}

    key = _db.Column(_db.BigInteger, primary_key=True)
    id = _db.Column(_db.BigInteger)
    customer_id = _db.Column(_db.BigInteger)
    customer_key = _db.Column(_db.BigInteger, _db.ForeignKey('customer.key'), nullable=True)
    address1 = _db.Column(_db.String)
    address2 = _db.Column(_db.String)
    city = _db.Column(_db.String)
    company = _db.Column(_db.String)
    country = _db.Column(_db.String)
    first_name = _db.Column(_db.String)
    last_name = _db.Column(_db.String)
    phone = _db.Column(_db.String)
    province = _db.Column(_db.String)
    zip = _db.Column(_db.String)
    name = _db.Column(_db.String)
    province_code = _db.Column(_db.String)
    country_code = _db.Column(_db.String)
    latitude = _db.Column(_db.String)
    longitude = _db.Column(_db.String)
    default = _db.Column(_db.Boolean)

    orders = _db.relationship('OrderDb', backref='address', lazy=True)

    @staticmethod
    def create_or_update(address):
        _db.session.add(address)
        _db.session.commit()
        return address