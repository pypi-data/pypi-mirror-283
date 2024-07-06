from ShopifyTupperware.data import db

_db = db.db

class DiscountCodeDb(_db.Model):

    __tablename__ = "discount_code"
    __table_args__ = {'implicit_returning':False}

    key = _db.Column(_db.BigInteger, primary_key=True)
    order_key = _db.Column(_db.BigInteger, _db.ForeignKey('order.key'), nullable=True)
    
    code = _db.Column(_db.String)
    amount = _db.Column(_db.String)
    type = _db.Column(_db.String)