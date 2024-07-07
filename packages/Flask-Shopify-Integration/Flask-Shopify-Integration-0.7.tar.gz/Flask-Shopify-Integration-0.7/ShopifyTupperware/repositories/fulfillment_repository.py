from ShopifyTupperware.repositories.repository import Repository
from shopify import Fulfillment
from shopify.resources.fulfillment import FulfillmentV2

class FulfillmentRepository(Repository):

    def save_fulfillment(self, data):
        try:
            fulfillment = Fulfillment()
            fulfillment.create(data)
            return fulfillment
        except Exception as ex:
            raise ex

    def save_fulfillment_v2(self, data):
        try:
            fulfillment = FulfillmentV2()
            response = fulfillment.create(data)
            return response
        except Exception as ex:
            raise ex
        

    def save_fulfillment_by_order(self, orderId, data):
        try:
            fulfillment = Fulfillment()
            fulfillment = fulfillment.find(order_id= orderId)
            if not fulfillment:
                return None
            fulfillment.create(data)
            return fulfillment
        except:
            return None
        

    def open(self, id, orderId):
        try:
            fulfillment = Fulfillment()
            fulfillment = fulfillment.find(id_= id, order_id=orderId)
            fulfillment.open()
            return fulfillment
        except:
            return None

    def completed(self, id, order_id):
        try:
            fulfillment = Fulfillment()
            fulfillment = fulfillment.find(id_= id, order_id= order_id)
            fulfillment.complete()
        except Exception as ex:
            return None

