from ShopifyTupperware.data.customer_db import CustomerDb
from ShopifyTupperware.data.customer2_db import Customer2Db
from ShopifyTupperware.data.gift_db import GiftDb
from ShopifyTupperware import helper
#import time

class CustomerBloc:

    @staticmethod
    def check_customer_by_email(email):
        return Customer2Db.check_exist(email)

    @staticmethod
    def add(new_order, customer):
        new_customer = CustomerDb()
        for key, value in customer.items():
            if hasattr(new_customer, key) & (helper.is_dictionary(customer[key]) != True):
                setattr(new_customer, key, value)
            
        new_customer = CustomerDb.create_or_update(new_customer)
        new_order.customer_id = new_customer.id
        new_order.customer_key = new_customer.key
        return new_customer

    @staticmethod
    def create(model):
        if Customer2Db.exist(model['id']) is not None:
            return None
        if Customer2Db.check_exist(model['email']) is not None:
            return None
        customer = Customer2Db()
        for key, value in model.items():
            if hasattr(customer, key) & (helper.is_dictionary(model[key]) != True):
                setattr(customer, key, value)
                pass
            pass
        customer.status = 1
        Customer2Db.create_or_update(customer)
        #time.sleep(1)
        return Customer2Db.sync_customer_tags(model['id'])

    @staticmethod
    def update_status(key):
        return Customer2Db.update_status(key)

    @staticmethod
    def delete_customer(model):
        if not model:
            return None
        if 'id' not in model or model['id'] is None:
            return None
        return Customer2Db.delete_customer(model['id'])


    @staticmethod
    def update_customer_id(key, model):
        if not model:
            return None
        if 'id' not in model or model['id'] is None:
            return None
        id = model['id']
        address_ids = []
        if 'addresses' in model and model['addresses'] is not None:
            addresses = model['addresses']
            for addr in addresses:
                temp_dict= {
                    'id': (addr['id'] if 'id' in addr and addr['id'] is not None else 0), 
                    'nama': (addr['name'] if 'name' in addr and addr['name'] is not None else ''), 
                    'kodepos': (addr['zip'] if 'zip' in addr and addr['zip'] is not None else '')
                }
                address_ids.append(temp_dict)
        if len(address_ids) > 0 :
            for addr_id in address_ids:
                Customer2Db.update_customer(key, id, addr_id['id'], addr_id['nama'], addr_id['kodepos'])
        else:
            Customer2Db.update_customer(key, id, 0, None, None)
        return 0

    @staticmethod
    def update_customer_gift(key, model):
        if not model:
            return None
        id = model['id']
        customer_id = model['customer_id']
        return GiftDb.update_gift(key, id, customer_id)

