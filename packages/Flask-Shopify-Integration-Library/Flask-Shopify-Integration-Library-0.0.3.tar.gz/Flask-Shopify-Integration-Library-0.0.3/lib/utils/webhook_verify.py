import base64
import hashlib
import hmac


def verify_webhook(data, headers, key):
    try:
        hmac_header  = headers.get('X-Shopify-Hmac-SHA256')
        store = headers.get('X-Shopify-Shop-Domain')
        shared_key = key.encode()
        data_bytes = data
        digest = hmac.new(shared_key, msg=data_bytes, digestmod= hashlib.sha256).digest()
        computed_hmac = base64.b64encode(digest).decode()
        return hmac.compare_digest(str(computed_hmac).encode(), str(hmac_header).encode())
    except:
        return None
    
