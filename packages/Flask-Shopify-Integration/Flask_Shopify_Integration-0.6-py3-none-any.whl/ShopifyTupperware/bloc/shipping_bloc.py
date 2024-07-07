from ShopifyTupperware.data.shipping_line_db  import ShippingLineDb
from ShopifyTupperware import helper

class ShippingBloc:

    @staticmethod
    def add_shipping_lines(order, shipping_lines):
        for model in shipping_lines:
            db = ShippingLineDb()
            for key, value in model.items():
                if hasattr(db, key) & (helper.is_dictionary(model[key]) != True):
                    setattr(db, key, value)
            order.shipping_lines.append(db)
        return order


