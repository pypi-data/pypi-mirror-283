from ShopifyTupperware.data.address_db import AddressDb
from ShopifyTupperware import helper

class AddressBloc:

    @staticmethod
    def add_shipping_address(new_order, new_customer, address):
        new_address = AddressDb()
        for key, value in address.items():
            if hasattr(new_address, key) & (helper.is_dictionary(address[key]) != True):
                setattr(new_address, key, value)
        new_address.customer_id = new_customer.id
        new_address.customer_key = new_customer.key
        new_address = AddressDb.create_or_update(new_address)
        new_order.address_id = new_address.id
        new_order.address_key = new_address.key
        return new_address
