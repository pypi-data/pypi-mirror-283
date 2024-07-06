from ShopifyTupperware.repositories.repository import Repository
from shopify import Transaction

class TransactionRepository(Repository):

    def get_transactions(self, orderId):
        try:
            trans = Transaction()
            trans = trans.find(order_id = orderId)
            return trans
        except:
            return None



