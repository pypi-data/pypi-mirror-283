from ShopifyTupperware.data import db

_db = db.db

class LineItemDb(_db.Model):
    __tablename__ = "lineitem"
    __table_args__ = {'implicit_returning':False}

    key = _db.Column(_db.BigInteger, primary_key=True)
    id = _db.Column(_db.BigInteger)


    order_key = _db.Column(_db.BigInteger, _db.ForeignKey('order.key'), nullable=True)
    order_id = _db.Column(_db.BigInteger)
       
    product_key = _db.Column(_db.BigInteger, _db.ForeignKey('product.key'), nullable=True)
    product_id = _db.Column(_db.BigInteger)
        
    variant_key = _db.Column(_db.BigInteger, _db.ForeignKey('variant.key'), nullable=True)
    variant_id = _db.Column(_db.BigInteger)

    sku = _db.Column(_db.String)
    price = _db.Column(_db.Float)
    quantity = _db.Column(_db.Integer)
    requires_shipping = _db.Column(_db.Boolean)
    title = _db.Column(_db.String)
    variant_title = _db.Column(_db.String)
    vendor = _db.Column(_db.String)
    name = _db.Column(_db.String)
    fulfillable_quantity = _db.Column(_db.Integer)
    fulfillment_service = _db.Column(_db.String)
    fulfillment_status = _db.Column(_db.String)
    total_discount = _db.Column(_db.Float)


    discount_allocations =  _db.relationship('DiscountAllocationDb', backref='lineitem', lazy=True)