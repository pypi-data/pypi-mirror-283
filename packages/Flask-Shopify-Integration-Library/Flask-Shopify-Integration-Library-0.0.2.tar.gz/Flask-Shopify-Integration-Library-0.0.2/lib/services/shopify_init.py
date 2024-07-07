from shopify import ShopifyResource, Session

class ShopifyBaseService:

    def __init__(self, host, version, token):
        session = Session(host, version=version, token=token)
        ShopifyResource.activate_session(session)
