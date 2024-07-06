from ShopifyTupperware.data import db
from ShopifyTupperware.data.order_db import OrderDb
from ShopifyTupperware.data.address_db import AddressDb

_db = db.db

class Customer2Db(_db.Model):
    
     __tablename__ = "customer2"
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
     status = _db.Column(_db.Integer)

     @staticmethod
     def create_or_update(customer):
         _db.session.add(customer)
         _db.session.commit()
         return customer

     @staticmethod
     def exists(firstname, lastname, email):
        customer = _db.session.query(Customer2Db).with_hint(Customer2Db, 'WITH (NOLOCK)').filter((Customer2Db.first_name.equal(firstname)) & (Customer2Db.last_name.equal(lastname)) & (Customer2Db.email.equal(email))).first()
        #Customer2Db.query.filter((Customer2Db.first_name.equal(firstname)) & (Customer2Db.last_name.equal(lastname)) & (Customer2Db.email.equal(email))).first()
        if not customer:
            return None
        return customer

     @staticmethod
     def exist(id):
        customer = _db.session.query(Customer2Db).with_hint(Customer2Db, 'WITH (NOLOCK)').filter(Customer2Db.id == id).first()
        if not customer:
            return None
        return customer

     @staticmethod
     def check_exist(email):
        customer = _db.session.query(Customer2Db).with_hint(Customer2Db, 'WITH (NOLOCK)').filter(Customer2Db.email == email).first()
        if not customer:
            return None
        return customer

     @staticmethod
     def delete_customer(id):
         _db.session.query(Customer2Db).with_hint(Customer2Db, 'WITH (NOLOCK)').filter(Customer2Db.id == id).delete()
         _db.session.commit()
         return id

     @staticmethod
     def update_status(key):
        _db.session.query(Customer2Db).filter(Customer2Db.key == key).update({"status": 1}, synchronize_session='fetch')
        _db.session.commit()
        return key

     @staticmethod
     def update_customer(key, id, address_id, addr_name, kodepos):
        conn = db.engine.raw_connection()
        cursor = conn.cursor()
        try:
             cursor.execute('exec trxUpdateCustomerId ?,?,?,?,?', [key, id, address_id, addr_name, kodepos])
             cursor.fetchone()
             cursor.close()
             conn.commit()
        except Exception as ex :
            print(ex)
        finally:
            conn.close()
        return key

     @staticmethod
     def sync_customer_tags(id):
        conn = db.engine.raw_connection()
        cursor = conn.cursor()
        try:
             cursor.execute('exec trxSyncCustomerTags ?', [id])
             cursor.fetchone()
             cursor.close()
             conn.commit()
        except Exception as ex :
            print(ex)
        finally:
            conn.close()
        return id

