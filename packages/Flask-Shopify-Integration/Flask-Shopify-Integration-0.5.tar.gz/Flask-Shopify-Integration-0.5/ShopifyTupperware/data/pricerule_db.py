from ShopifyTupperware.data import db
import datetime
_db = db.db

class PriceRuleDb(_db.Model):
    __tablename__ = "price_rule"
    __table_args__ = {'implicit_returning':False}

    key = _db.Column(_db.BigInteger, primary_key=True)
    id = _db.Column(_db.BigInteger)
    #allocation_method= _db.Column(_db.String)
    #customer_selection= _db.Column(_db.String)
    #entitled_collection_ids= _db.Column(_db.String)
    #entitled_product_ids= _db.Column(_db.String)
    #entitled_variant_ids= _db.Column(_db.String)
    once_per_customer= _db.Column(_db.Boolean)
    #prerequisite_customer_ids= _db.Column(_db.String)
    #customer_segment_prerequisite_ids= _db.Column(_db.String)
    #target_selection= _db.Column(_db.String)
    #target_type= _db.Column(_db.String)
    title= _db.Column(_db.String)
    usage_limit= _db.Column(_db.Integer)
    #prerequisite_product_ids= _db.Column(_db.String)
    #prerequisite_variant_ids= _db.Column(_db.String)
    #prerequisite_collection_ids= _db.Column(_db.String)
    value= _db.Column(_db.Integer)
    value_type= _db.Column(_db.String)
    discount_code= _db.Column(_db.String)
    allocation_limit= _db.Column(_db.Integer)
    starts_at= _db.Column(_db.DateTime, default=datetime.datetime.utcnow)
    ends_at= _db.Column(_db.DateTime)
    created_at= _db.Column(_db.DateTime, default=datetime.datetime.utcnow)
    updated_at= _db.Column(_db.DateTime, default=datetime.datetime.utcnow)
    status= _db.Column(_db.Integer)
    actived=  _db.Column(_db.Boolean)

    @staticmethod
    def update_id(key, id):
        _db.session.query(PriceRuleDb).filter(PriceRuleDb.key == key).update({"id": id}, synchronize_session='fetch')
        _db.session.commit()
        return id

    @staticmethod
    def find_by_id(id):
        data = _db.session.query(PriceRuleDb).with_hint(PriceRuleDb, 'WITH (NOLOCK)').filter(PriceRuleDb.id == int(id)).first()
        return data
    
    @staticmethod
    def find_by_code(code):
        data = _db.session.query(PriceRuleDb).with_hint(PriceRuleDb, 'WITH (NOLOCK)').filter(PriceRuleDb.discount_code == code).first()
        return data
    
    @staticmethod
    def update_usage_limit(code):
        _db.session.query(PriceRuleDb).filter(PriceRuleDb.title == code).update({"status": 4, "once_per_customer": True, "updated_at": datetime.datetime.utcnow() }, synchronize_session='fetch')
        _db.session.commit()
        return code

    @staticmethod
    def deactivated_discount(key):
        _db.session.query(PriceRuleDb).filter(PriceRuleDb.key == key).update({"actived": False, "updated_at": datetime.datetime.utcnow() }, synchronize_session='fetch')
        _db.session.commit()
        return key

    @staticmethod
    def update_current_discount(id, title):
        _db.session.query(PriceRuleDb).filter(PriceRuleDb.id == int(id)).update({"title": title, "status": 9, "actived": True, "updated_at": datetime.datetime.utcnow() }, synchronize_session='fetch')
        _db.session.commit()
        return id

    @staticmethod
    def add(discount):
        _db.session.add(discount)
        _db.session.commit()
        return discount

