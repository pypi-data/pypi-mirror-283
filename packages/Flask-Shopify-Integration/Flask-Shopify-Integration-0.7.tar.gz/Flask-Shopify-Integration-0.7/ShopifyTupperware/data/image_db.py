from ShopifyTupperware.data import db

_db = db.db

class ImageDb(_db.Model):

    __tablename__ = "product_image"
    __table_args__ = {'implicit_returning':False}

    key = _db.Column(_db.BigInteger, primary_key=True)
    id = _db.Column(_db.BigInteger)
    product_key =  _db.Column(_db.BigInteger, _db.ForeignKey('product.key'), nullable=True)
    product_id = _db.Column(_db.BigInteger)
    alt = _db.Column(_db.String)
    width = _db.Column(_db.Integer)
    height = _db.Column(_db.Integer)
    src = _db.Column(_db.String)
    processing = _db.Column(_db.Boolean)
    #created_at = _db.Column(_db.String)
    #updated_at = _db.Column(_db.String)

    @staticmethod
    def update_product_image_id(key, id, product_id):
        _db.session.query(ImageDb).filter(ImageDb.key == key).update({"id":id, "product_id":product_id, "processing": False}, synchronize_session='fetch')
        _db.session.commit()
        return 0

    @staticmethod
    def update_image_id(key, id, product_id):
        _db.session.query(ImageDb).filter(ImageDb.key == key).update({"id":id, "product_id":product_id, "processing": False}, synchronize_session='fetch')
        _db.session.commit()
        return 0

    @staticmethod
    def create_or_update(images):
        try:
            for image in images:
                _db.session.add(image)
            _db.session.commit()
            return 1
        except Exception as ex:
            _db.session.rollback()
            print(ex.args)
            return None
