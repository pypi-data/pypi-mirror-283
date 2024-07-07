from ShopifyTupperware.data import db

_db = db.db

class FulfillmentDb(_db.Model):

     __tablename__ = "fulfillment"
     __table_args__ = {'implicit_returning':False}
     
     key = _db.Column(_db.BigInteger, primary_key=True)
     id = _db.Column(_db.BigInteger)
     order_key = _db.Column(_db.BigInteger, _db.ForeignKey('order.key'), nullable=False)
     order_id = _db.Column(_db.BigInteger)
     location_id = _db.Column(_db.BigInteger)
     name = _db.Column(_db.String)
     notify_customer = _db.Column(_db.Boolean)
     service = _db.Column(_db.String)
     shipment_status = _db.Column(_db.String)
     status = _db.Column(_db.String)
     tracking_company = _db.Column(_db.String)
     tracking_number = _db.Column(_db.String)
     tracking_url = _db.Column(_db.String)
     updated_at = _db.Column(_db.String)
     variant_inventory_management = _db.Column(_db.String)


     @staticmethod
     def create_or_update(fulfillment):
        _db.session.add(fulfillment)
        _db.session.commit()
        return fulfillment


