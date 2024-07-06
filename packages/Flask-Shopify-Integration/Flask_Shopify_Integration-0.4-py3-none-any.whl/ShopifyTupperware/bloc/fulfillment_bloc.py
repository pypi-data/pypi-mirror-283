from ShopifyTupperware.data.fulfillment_db import FulfillmentDb
from ShopifyTupperware import helper
class FulfillmentBloc:

    @staticmethod
    def add(new_order, fulfillments):
        for fulfillment in fulfillments:
            new_fulfillment = FulfillmentDb()
            for key, value in fulfillment.items():
                if hasattr(new_fulfillment, key) & (helper.is_dictionary(fulfillment[key]) != True):
                    setattr(new_fulfillment, key, value)
            new_fulfillment.order_id = new_order.id
            new_order.fulfillments.append(new_fulfillment)
        return new_order
