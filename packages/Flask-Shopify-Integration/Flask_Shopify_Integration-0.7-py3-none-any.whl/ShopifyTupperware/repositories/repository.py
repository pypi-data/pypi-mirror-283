from shopify import ShopifyResource, Session
from config import shopify_host, shopify_version, shopify_pwd

class Repository:
    def __init__(self):
        session = Session(shopify_host, version=shopify_version, token=shopify_pwd)
        ShopifyResource.activate_session(session)