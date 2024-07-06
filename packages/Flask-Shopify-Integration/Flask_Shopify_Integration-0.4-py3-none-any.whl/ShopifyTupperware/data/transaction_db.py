from ShopifyTupperware.data import db

_db = db.db

class TransactionDb(_db.Model):

    __tablename__ = "transaction"
    __table_args__ = {'implicit_returning':False}

    key = _db.Column(_db.BigInteger, primary_key=True)
    id = _db.Column(_db.BigInteger)
    order_key =  _db.Column(_db.BigInteger, _db.ForeignKey('order.key'), nullable=False)
    order_id = _db.Column(_db.BigInteger)
    location_id = _db.Column(_db.BigInteger)
    user_id = _db.Column(_db.BigInteger)
    parent_id = _db.Column(_db.BigInteger)
    device_id =  _db.Column(_db.String)
    kind =  _db.Column(_db.String)
    gateway =  _db.Column(_db.String)
    status =  _db.Column(_db.String)
    message =  _db.Column(_db.String)
    created_at =  _db.Column(_db.String)
    test = _db.Column(_db.Boolean)
    authorization =  _db.Column(_db.String)
    processed_at =  _db.Column(_db.String)
    error_code =  _db.Column(_db.String)
    source_name =  _db.Column(_db.String)
    amount = _db.Column(_db.Float)
    currency =  _db.Column(_db.String)


