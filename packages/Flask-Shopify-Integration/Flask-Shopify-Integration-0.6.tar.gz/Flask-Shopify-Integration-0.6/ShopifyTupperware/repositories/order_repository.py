from ShopifyTupperware.repositories.repository import Repository
from shopify import Order, Transaction, Fulfillment
import math
import urllib.parse


class OrderRepository(Repository):

    def get_order_page(self, after_date, before_date):
        try:
            limit = 50
            orders = list()
            order = Order.find(limit= limit, financial_status= "paid", updated_at_min= after_date, updated_at_max= before_date)
            orders.extend(order)
            while order.next_page_url is not None:
                url_parts = urllib.parse.urlparse(order.next_page_url)
                query_parts = urllib.parse.parse_qs(url_parts.query)
                page_info = query_parts['page_info'][0]
                order = Order.find(limit= limit, page_info= page_info)
                orders.extend(order)
            return orders
        except Exception as ex:
            raise ex

    def get_order_paid(self):
        try:
            order = Order.find(status ="any", financial_status= "paid")
            return order
        except:
            return None


    def get_orders(self):
        try:
            order = Order()
            order = order.find()
            return order
        except:
            return None
       

    def get_order(self, id):
        try:
            order = Order()
            order = order.find(id_ = id)
            return order
        except:
            return None

    def update_order(self, data):
        try:
            order = Order(data)
            order.save()
            return order
        except:
            return None

    def paid_order(self, data):
        try:
            trx = Transaction()
            trx = trx.find(order_id= data['order_id'])
            if not trx:
                return None
            transaction_id = trx[0].id
            transaction = Transaction.create(data)
            return transaction
        except:
            return None
        

    def shipped_order(self, data):
        try:
            #if ('location_id' not in data) or ('order_id' not in data):
            #    return None
            fulfillment = Fulfillment.create(data)
            return fulfillment
        except:
            return None

    def completed_order(self, id, order_id):
        try:
            fulfillment = Fulfillment()
            fulfillment = fulfillment.find(id_= id, order_id= order_id)
            fulfillment.complete()
            return fulfillment
        except Exception as ex:
            return None
        


    def cancel_order(self, id):
        try:
            order = Order()
            order = order.find(id_= id)
            order.cancel()
            return order
        except:
            return None

    def get_transaction_by_orderid(self, id):
        try:
            trans = Transaction()
            trans = trans.find(order_id= id)
            if not trans:
                return None
            return trans
        except Exception as ex:
            return None
        

