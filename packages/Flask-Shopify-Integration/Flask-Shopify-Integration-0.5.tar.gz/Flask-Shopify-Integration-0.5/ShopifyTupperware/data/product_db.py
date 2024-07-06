from ShopifyTupperware.data import db
from ShopifyTupperware.data.variant_db import VariantDb
from datetime import datetime

_db = db.db

class ProductDb(_db.Model):

    __tablename__ = "product"
    __table_args__ = {'implicit_returning':False}

    key = _db.Column(_db.BigInteger, primary_key=True)
    id = _db.Column(_db.BigInteger)
    title = _db.Column(_db.String)
    body_html = _db.Column(_db.String)
    vendor = _db.Column(_db.String)
    product_type = _db.Column(_db.String)
    published = _db.Column(_db.Boolean)
    published_at = _db.Column(_db.DateTime) 
    status = _db.Column(_db.Integer)
    is_sync = _db.Column(_db.Boolean)
    variants = _db.relationship('VariantDb', backref='product', lazy=True)
    images = _db.relationship('ImageDb', backref='product', lazy=True)


    @staticmethod
    def create_or_update(product):
        _db.session.add(product)
        _db.session.commit()
        return product

    @staticmethod
    def update_id(key, id):
        _db.session.query(ProductDb).filter(ProductDb.key == key).update({"id": id, "is_sync": True}, synchronize_session='fetch')
        _db.session.commit()
        return id

    @staticmethod
    def update_published(id, model):
        try:
            published_date = None
            if model['published_at'] is not None:
                dt_time = str(model['published_at']).split(sep='+')[0]
                published_date = datetime.strptime(dt_time, '%Y-%m-%dT%H:%M:%S')
                pass
            is_published = published_date is not None
            _db.session.query(ProductDb).filter(ProductDb.id == id).update({
                "title":model['title'],
                "body_html":model['body_html'],
                "vendor":model['vendor'],
                "product_type":model['product_type'],
                "published_at": published_date, 
                "published" : is_published
                }, synchronize_session='fetch')
            _db.session.commit()
            return 0
        except Exception as ex:
          return None



    connection = None
    cursor = None
    def __init__(self):
        self.connection =  db.engine.raw_connection()
        self.cursor = self.connection.cursor()

    def delete_product(self, id):
        try:
             self.cursor.execute('exec productDeletedById ?', id)
             self.cursor.close()
             self.connection.commit()
        except:
            return None
        finally:
            self.connection.close()
    
    def get_products(self):
        try:
            self.cursor.execute('exec getProducts')
            results = self.cursor.fetchall()
            return results
        except:
            return None
        finally:
            self.cursor.close()
            self.connection.close()