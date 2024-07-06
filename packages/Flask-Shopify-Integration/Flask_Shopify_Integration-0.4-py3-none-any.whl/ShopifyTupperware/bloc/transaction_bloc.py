from ShopifyTupperware.data import order_db, customer_db, address_db, fulfillment_db
from ShopifyTupperware import helper
from ShopifyTupperware.data.transaction_db import TransactionDb

class TransactionBloc:

    @staticmethod
    def add_transactions(new_order, transactions):
        for transaction in transactions:
            new_transaction = TransactionDb()
            for key, value in transaction.items():
                if hasattr(new_transaction, key) & (helper.is_dictionary(transaction[key]) != True):
                    setattr(new_transaction, key, value)
            new_transaction.order_id = new_order.id
            new_order.transactions.append(new_transaction)
        return new_order


