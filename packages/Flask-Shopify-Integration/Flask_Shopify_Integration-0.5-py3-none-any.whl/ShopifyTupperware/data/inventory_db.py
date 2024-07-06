from ShopifyTupperware.data import db

_db = db.db

class InventoryLevelDb(_db.Model):

    __tablename__ = "inventory_level"
    __table_args__ = {'implicit_returning':False}

    id = _db.Column(_db.BigInteger, primary_key=True)
    inventory_item_id = _db.Column(_db.BigInteger, nullable=False)
    location_id = _db.Column(_db.BigInteger, nullable=False)
    available = _db.Column(_db.Integer)
    status = _db.Column(_db.Integer)
    is_sync = _db.Column(_db.Boolean)

    @staticmethod
    def add_or_update(data):
        _db.session.add(data)
        _db.session.commit()
        return data

class InventoryItemDb(_db.Model):
    __tablename__ = "inventory_item"

    id = _db.Column(_db.BigInteger, primary_key=True)

class LocationDb(_db.Model):
    __tablename__ = "location"
    __table_args__ = {'implicit_returning':False}
    
    key = _db.Column(_db.BigInteger, primary_key=True)
    id = _db.Column(_db.BigInteger)
    actived = _db.Column(_db.Boolean)
    is_default = _db.Column(_db.Boolean)
    name = _db.Column(_db.String)
    address1 = _db.Column(_db.String)
    address2 = _db.Column(_db.String)
    city = _db.Column(_db.String)
    country = _db.Column(_db.String)
    country_code = _db.Column(_db.String)
    legacy = _db.Column(_db.Boolean)
    phone = _db.Column(_db.String)
    province = _db.Column(_db.String)
    province_code = _db.Column(_db.String)
    zip = _db.Column(_db.String)
    is_sync =  _db.Column(_db.Boolean)

    @staticmethod
    def create_location(location):
        _db.session.add(location)
        _db.session.commit()
        return location

    @staticmethod
    def update_location(key, id):
        _db.session.query(LocationDb).filter(LocationDb.key == key).update({"id": id, "is_sync": True}, synchronize_session='fetch')
        _db.session.commit()
        return id

    @staticmethod
    def update_location_by_id(id, name, address1):
        _db.session.query(LocationDb).filter(LocationDb.id == id).update({"name": name, "address1": address1}, synchronize_session='fetch')
        _db.session.commit()
        return id

    @staticmethod
    def location_exists(id):
        return _db.session.query(LocationDb).filter(LocationDb.id == id).with_hint(LocationDb, 'WITH (NOLOCK)').first()





