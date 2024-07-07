from ShopifyTupperware.data import db

_db = db.db

class OrderDb(_db.Model):
        __tablename__ = "order"
        __table_args__ = {'implicit_returning':False}

        key = _db.Column(_db.BigInteger, primary_key=True)
        id = _db.Column(_db.BigInteger)


        customer_key = _db.Column(_db.BigInteger, _db.ForeignKey('customer.key'), nullable=True)
        customer_id = _db.Column(_db.BigInteger)
       
        address_key = _db.Column(_db.BigInteger, _db.ForeignKey('address.key'), nullable=True)
        address_id = _db.Column(_db.BigInteger)
        
        app_id = _db.Column(_db.BigInteger)
        location_id = _db.Column(_db.BigInteger)

        name = _db.Column(_db.String)
        note = _db.Column(_db.String)
        gateway = _db.Column(_db.String)
        number = _db.Column(_db.Integer)
        order_number = _db.Column(_db.BigInteger)
        #add new item here
        checkout_id =  _db.Column(_db.BigInteger)
        financial_status = _db.Column(_db.String)
        fulfillment_status = _db.Column(_db.String)
        email = _db.Column(_db.String)
        phone = _db.Column(_db.String)
        subtotal_price = _db.Column(_db.Float)
        tags = _db.Column(_db.String)
        token = _db.Column(_db.String)
        total_discounts = _db.Column(_db.Float)
        total_line_items_price = _db.Column(_db.Float)
        total_price = _db.Column(_db.Float)
        total_tax = _db.Column(_db.Float)
        total_weight = _db.Column(_db.Float)
        updated_at = _db.Column(_db.String)
        processed_at = _db.Column(_db.String)
        created_at = _db.Column(_db.String)
        closed_at = _db.Column(_db.String)
        order_status_url = _db.Column(_db.String)

        fulfillments = _db.relationship('FulfillmentDb', backref='order', lazy=True)
        line_items = _db.relationship('LineItemDb', backref='order', lazy=True)
        discount_applications =  _db.relationship('DiscountAppDb', backref='order', lazy=True)
        discount_codes =  _db.relationship('DiscountCodeDb', backref='order', lazy=True)
        shipping_lines =  _db.relationship('ShippingLineDb', backref='order', lazy=True)

        @staticmethod
        def save_or_update(order):
            _db.session.add(order)
            _db.session.commit()
            return order

        @staticmethod
        def update_checkoutid(orderid, checkout_id):
             _db.session.query(OrderDb).filter(OrderDb.id == orderid).update({"checkout_id": checkout_id}, synchronize_session='fetch')
             _db.session.commit()
             return orderid

        @staticmethod
        def update_locationid(key, location_id):
             _db.session.query(OrderDb).filter(OrderDb.key == key).update({"location_id": location_id}, synchronize_session='fetch')
             _db.session.commit()
             return key

        @staticmethod
        def order_id_exists(order_id):
            current_order_id = _db.session.query(OrderDb.id).with_hint(OrderDb, 'WITH (NOLOCK)').filter(OrderDb.id == order_id).first()
            return current_order_id #_db.session.query(OrderDb.id).with_hint(OrderDb, 'WITH (NOLOCK)').filter(OrderDb.id == orderid).first()

        @staticmethod
        def update_order_location_id(key, location_id):
            conn = db.engine.raw_connection()
            cursor = conn.cursor()
            try:
                 cursor.execute('exec updateOrderLocation ?,?', [key, location_id])
                 cursor.fetchone()
                 cursor.close()
                 conn.commit()
            except Exception as ex :
                print(ex)
            finally:
                conn.close()
            return key



