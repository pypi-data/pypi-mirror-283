from ShopifyTupperware.data import db

_db = db.db

class ShippingLineDb(_db.Model):
    
    __tablename__ = "shipping_line"
    __table_args__ = {'implicit_returning':False}

    key = _db.Column(_db.BigInteger, primary_key=True)
    id = _db.Column(_db.BigInteger)
    order_key = _db.Column(_db.BigInteger, _db.ForeignKey('order.key'), nullable=True)

    title = _db.Column(_db.String)
    price = _db.Column(_db.Float)
    code = _db.Column(_db.String)
    source = _db.Column(_db.String)
    discounted_price= _db.Column(_db.Float)
