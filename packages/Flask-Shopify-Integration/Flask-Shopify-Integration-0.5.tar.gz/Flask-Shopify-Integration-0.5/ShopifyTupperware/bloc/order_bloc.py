from ShopifyTupperware.data.order_db import OrderDb
from ShopifyTupperware.bloc.discount_bloc import DiscountBloc
from ShopifyTupperware.bloc.transaction_bloc import TransactionBloc
from ShopifyTupperware.bloc.customer_bloc import CustomerBloc
from ShopifyTupperware.bloc.address_bloc import AddressBloc
from ShopifyTupperware.bloc.fulfillment_bloc import FulfillmentBloc
from ShopifyTupperware.bloc.line_item_bloc import LineItemBloc
from ShopifyTupperware.models.customer_model import CustomerSchema
from ShopifyTupperware.bloc.shipping_bloc import ShippingBloc
from ShopifyTupperware import helper


class OrderBloc:

    @staticmethod
    def save_order(order):
        #initial order
        new_order = OrderDb()
        for key, value in order.items():
            if hasattr(new_order, key) & (helper.is_dictionary(order[key]) != True):
                setattr(new_order, key, value)
        #add customer
        if order['customer'] is not None:
            customer = order['customer']
            new_customer = CustomerBloc.add(new_order, customer)

            #add address
            if order['shipping_address'] is not None:
                address = order['shipping_address']
                AddressBloc.add_shipping_address(new_order, new_customer, address)

        #add fulfillments
        if 'fulfillments' in order:
            if (order['fulfillments'] is not None) and (len(order['fulfillments']) > 0):
                fulfillments = order['fulfillments']
                FulfillmentBloc.add(new_order, fulfillments)

        #add line-items
        if 'line_items' in order:
            if (order['line_items'] is not None) and (len(order['line_items']) > 0):
                line_items = order['line_items']
                LineItemBloc.add(new_order, line_items)

        #add transactions
        if 'transactions' in order:
            if (order['transactions'] is not None) and (len(order['transactions']) > 0):
                transactions = order['transactions']
                TransactionBloc.add_transactions(new_order, transactions)

        #add discount applications
        if 'discount_applications' in order:
            if (order['discount_applications'] is not None) and (len(order['discount_applications']) > 0):
                discount_applications = order['discount_applications'] 
                DiscountBloc.add_discount_applications(new_order, discount_applications)

        #add discount codes
        if 'discount_codes' in order:
            if (order['discount_codes'] is not None) and (len(order['discount_codes']) > 0):
                discount_codes = order['discount_codes']
                DiscountBloc.add_discount_codes(new_order, discount_codes)
        #add shipping lines item
        if 'shipping_lines' in order:
            if(order['shipping_lines'] is not None) and (len(order['shipping_lines']) > 0):
                ShippingBloc.add_shipping_lines(new_order, order['shipping_lines'])

        new_order = OrderDb.save_or_update(new_order)
        return new_order

    @staticmethod
    def order_exist(id):
        return OrderDb.order_id_exists(id) #OrderDb.query.filter(OrderDb.id == id).first()

    @staticmethod
    def update_order_locationid(key, location_id):
        return OrderDb.update_order_location_id(key, location_id)