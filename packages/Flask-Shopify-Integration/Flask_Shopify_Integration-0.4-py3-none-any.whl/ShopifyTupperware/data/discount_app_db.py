from ShopifyTupperware.data import db

_db = db.db

class DiscountAppDb(_db.Model):

    __tablename__ = "discount_application"
    __table_args__ = {'implicit_returning':False}

    key = _db.Column(_db.BigInteger, primary_key=True)
    order_key = _db.Column(_db.BigInteger, _db.ForeignKey('order.key'), nullable=True)

    type = _db.Column(_db.String)
    value = _db.Column(_db.String)
    value_type = _db.Column(_db.String)
    allocation_method = _db.Column(_db.String)
    target_selection = _db.Column(_db.String)
    target_type = _db.Column(_db.String)
    code = _db.Column(_db.String)
    title = _db.Column(_db.String)
