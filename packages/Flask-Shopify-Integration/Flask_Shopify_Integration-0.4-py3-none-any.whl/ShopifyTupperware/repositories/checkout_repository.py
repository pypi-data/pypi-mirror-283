from ShopifyTupperware.repositories.repository import Repository
from shopify import Checkout

class CheckoutRepository(Repository):

    def create_checkout(self, data):
        checkout = Checkout(data)
        checkout.save()
        return checkout

    def get_checkout(self, token):
        checkout = Checkout()
        return checkout.find(token=token)



