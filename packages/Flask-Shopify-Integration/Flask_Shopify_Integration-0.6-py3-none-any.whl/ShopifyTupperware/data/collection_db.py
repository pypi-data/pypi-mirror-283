from ShopifyTupperware.data import db

_db = db.db

class CollectionDb(_db.Model):
    __tablename__ = "collection"
    __table_args__ = {'implicit_returning':False}

    key = _db.Column(_db.Integer, primary_key=True)
    id = _db.Column(_db.BigInteger)
    body_html = _db.Column(_db.String)
    handle = _db.Column(_db.String)
    image = _db.Column(_db.String)
    published = _db.Column(_db.Boolean)
    published_at = _db.Column(_db.String)
    published_scope = _db.Column(_db.String)
    sort_order = _db.Column(_db.String)
    title = _db.Column(_db.String)
    updated_at = _db.Column(_db.String)

    @staticmethod
    def create_or_update(collection):
        _db.session.add(collection)
        _db.session.commit()
        return collection

    @staticmethod
    def update_collection(id, title, image, body_html, published, handle):
        _db.session.query(CollectionDb).with_hint(CollectionDb, 'WITH (NOLOCK)').filter(CollectionDb.id == id).update({"title": title, "image": image, "body_html": body_html, "published": published, "handle": handle}, synchronize_session='fetch')
        _db.session.commit()
        return id

    @staticmethod
    def collection_exists(id):
        return _db.session.query(CollectionDb).with_hint(CollectionDb, 'WITH (NOLOCK)').filter(CollectionDb.id == id).first()

    @staticmethod
    def get_collections():
        return _db.session.query(CollectionDb).with_hint(CollectionDb, 'WITH (NOLOCK)').all()


