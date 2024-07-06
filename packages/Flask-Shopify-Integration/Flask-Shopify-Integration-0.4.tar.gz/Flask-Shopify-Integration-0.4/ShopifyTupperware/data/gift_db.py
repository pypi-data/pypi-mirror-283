from ShopifyTupperware.data import db

_db = db.db

class GiftDb(_db.Model):
    __tablename__ = "gift_card"
    __table_args__ = {'implicit_returning':False}
    key = _db.Column(_db.BigInteger, primary_key=True)
    id = _db.Column(_db.BigInteger)
    api_client_id =  _db.Column(_db.Integer)
    email = _db.Column(_db.String)
    customer_id = _db.Column(_db.BigInteger)
    order_id = _db.Column(_db.BigInteger)
    line_item_id = _db.Column(_db.BigInteger)
    user_id = _db.Column(_db.BigInteger)
    balance = _db.Column(_db.String)
    currency = _db.Column(_db.String)
    initial_value = _db.Column(_db.String)
    code = _db.Column(_db.String)
    note = _db.Column(_db.String)
    disabled_at = _db.Column(_db.String)
    expires_on = _db.Column(_db.String)
    template_suffix = _db.Column(_db.String)
    last_characters = _db.Column(_db.String)
    created_at = _db.Column(_db.String)
    updated_at = _db.Column(_db.String)
    status = _db.Column(_db.Integer)

    @staticmethod
    def create_or_update(gift):
         _db.session.add(gift)
         _db.session.commit()
         return gift

    @staticmethod
    def update_gift(key, id, customer_id):
        _db.session.query(GiftDb).filter(GiftDb.key == key).update({"status": 3, "id": id, "customer_id": customer_id}, synchronize_session='fetch')
        _db.session.commit()
        return key
