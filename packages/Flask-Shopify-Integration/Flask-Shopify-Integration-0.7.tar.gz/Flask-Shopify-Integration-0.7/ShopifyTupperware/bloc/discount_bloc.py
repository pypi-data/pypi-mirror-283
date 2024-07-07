from ShopifyTupperware.data.discount_app_db import DiscountAppDb
from ShopifyTupperware.data.discount_code_db import DiscountCodeDb
from ShopifyTupperware import helper

class DiscountBloc:

    @staticmethod
    def add_discount_applications(new_order, discounts):
        for discount in discounts:
            new_discount = DiscountAppDb()
            for key, value in discount.items():
                if hasattr(new_discount, key) & (helper.is_dictionary(discount[key]) != True):
                    setattr(new_discount, key, value)
            new_order.discount_applications.append(new_discount)
        return new_order


    @staticmethod
    def add_discount_codes(new_order, discounts):
        for discount in discounts:
            new_discount = DiscountCodeDb()
            for key, value in discount.items():
                if hasattr(new_discount, key) & (helper.is_dictionary(discount[key]) != True):
                    setattr(new_discount, key, value)
            new_order.discount_codes.append(new_discount)
        return new_order
