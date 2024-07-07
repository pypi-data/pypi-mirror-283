from ShopifyTupperware.data.pricerule_db import PriceRuleDb

class PriceRuleBloc:

    @staticmethod
    def insert_update_discount(orderId, code, amount, disc_type):
        exist =PriceRuleDb.find_by_code(code)
        if exist is None:
            price_db = PriceRuleDb()
            price_db.title= code
            price_db.discount_code= code
            price_db.value_type= disc_type
            price_db.value= int(float(amount) * -1)
            price_db.once_per_customer= True
            price_db.status= 4
            PriceRuleDb.add(price_db)
        else:
            PriceRuleDb.update_usage_limit(code)
        return orderId

    @staticmethod
    def create_discount(id, title):
        exist = PriceRuleDb.find_by_id(id)
        if exist is None:
            price_db = PriceRuleDb()
            price_db.id= int(id)
            price_db.title= title
            price_db.once_per_customer= True
            price_db.status= 9
            PriceRuleDb.add(price_db)
        else:
            PriceRuleDb.update_current_discount(id, title)


    @staticmethod
    def deactivated_discount(key):
        PriceRuleDb.deactivated_discount(key)

    @staticmethod
    def update_discount_id(key, id):
        PriceRuleDb.update_id(key, id)

