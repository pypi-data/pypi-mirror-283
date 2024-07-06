from ShopifyTupperware.data import db
from ShopifyTupperware.data.order_db import OrderDb
from ShopifyTupperware.data.address_db import AddressDb

_db = db.db

class CustomerDb(_db.Model):
    
     __tablename__ = "customer"
     __table_args__ = {'implicit_returning':False}

     key = _db.Column(_db.BigInteger, primary_key=True)
     id = _db.Column(_db.BigInteger)
     email = _db.Column(_db.String)
     accepts_marketing = _db.Column(_db.Boolean)
     created_at = _db.Column(_db.String)
     updated_at = _db.Column(_db.String)
     first_name = _db.Column(_db.String)
     last_name = _db.Column(_db.String)
     orders_count = _db.Column(_db.Integer)
     state = _db.Column(_db.String)
     total_spent = _db.Column(_db.Float)
     last_order_id = _db.Column(_db.BigInteger)
     note = _db.Column(_db.String)
     verified_email = _db.Column(_db.Boolean)
     phone = _db.Column(_db.String)
     tags = _db.Column(_db.String)
     last_order_name = _db.Column(_db.String)
     currency = _db.Column(_db.String)

     orders = _db.relationship('OrderDb', backref='customer', lazy=True)
     addresses = _db.relationship('AddressDb', backref='customer', lazy=True)


     @staticmethod
     def create_or_update(customer):
         _db.session.add(customer)
         _db.session.commit()
         return customer

     @staticmethod
     def exists(firstname, lastname, email):
        customer = _db.session.query(CustomerDb).with_hint(CustomerDb, 'WITH (NOLOCK)').filter((CustomerDb.first_name.equal(firstname)) & (CustomerDb.last_name.equal(lastname)) & (CustomerDb.email.equal(email))).first()
        if not customer:
            return None
        return customer

     @staticmethod
     def exist(id):
        customer = CustomerDb.query.get(id)
        return customer


