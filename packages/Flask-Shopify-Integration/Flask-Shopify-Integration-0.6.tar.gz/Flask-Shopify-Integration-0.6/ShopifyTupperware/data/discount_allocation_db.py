from ShopifyTupperware.data import db

_db = db.db

class DiscountAllocationDb(_db.Model):

    __tablename__ = "discount_allocation"
    __table_args__ = {'implicit_returning':False}

    key = _db.Column(_db.BigInteger, primary_key=True)
    line_item_key = _db.Column(_db.BigInteger, _db.ForeignKey('lineitem.key'), nullable=True)
    amount = _db.Column(_db.Float)
    discount_application_index = _db.Column(_db.Integer)


