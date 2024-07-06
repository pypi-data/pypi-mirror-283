from ShopifyTupperware.data import db

_db = db.db

class VariantDb(_db.Model):
    __tablename__ = "variant"
    __table_args__ = {'implicit_returning':False}

    key = _db.Column(_db.BigInteger, primary_key=True)
    id = _db.Column(_db.BigInteger)
    product_key =  _db.Column(_db.BigInteger, _db.ForeignKey('product.key'), nullable=False)
    product_id = _db.Column(_db.BigInteger)
    inventory_item_id = _db.Column(_db.BigInteger)
    sku = _db.Column(_db.String)
    price = _db.Column(_db.Float)
    taxable = _db.Column(_db.Boolean)
    inventory_quantity = _db.Column(_db.Integer)
    old_inventory_quantity = _db.Column(_db.Integer)
    inventory_management = _db.Column(_db.String)

    @staticmethod
    def update_inventory_item_id(product_key, product_id, inventory_item_id, id):
        _db.session.query(VariantDb).filter(VariantDb.product_key == product_key).update({"product_id":product_id, "inventory_item_id": inventory_item_id, "id": id}, synchronize_session='fetch')
        _db.session.commit()
        return 0
