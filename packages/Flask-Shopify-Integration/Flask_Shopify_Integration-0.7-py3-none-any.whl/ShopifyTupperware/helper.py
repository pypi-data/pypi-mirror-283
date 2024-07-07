import hmac
import hashlib
import base64
from config import shopify_shared_secret, shopify_store

def is_dictionary(obj):
    return (isinstance(obj, dict)) | (isinstance(obj, list))


def verify_webhook(data, headers):
    try:
        hmac_header  = headers.get('X-Shopify-Hmac-SHA256')
        store = headers.get('X-Shopify-Shop-Domain')
        shared_key = shopify_shared_secret.encode()
        data_bytes = data
        digest = hmac.new(shared_key, msg=data_bytes, digestmod= hashlib.sha256).digest()
        computed_hmac = base64.b64encode(digest).decode()
        return hmac.compare_digest(str(computed_hmac).encode(), str(hmac_header).encode())
    except:
        return None
   