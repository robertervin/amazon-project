from products.models import Product
import dicttoxml

import traceback

from mws import mws

class Hide(object):
    def __init__(self):
        self.hidden = Product.objects.filter(published=True)
        
    def run(self):
        """
        Sends API requests to the amazon webstore and sets all published products to hidden
        """
        return
        
        
class Publish(object):
    def __init__(self, products):
        self.products = products
    
    def run(self):
        """
        Sends API requests to the amazon webstore and publishes all new products
        """
        product_dict = []
        for ASIN in self.products:
            product_dict.append({
                "Product": {
                    "StandardProductID": {
                        "Type": "ASIN",
                        "Value": ASIN
                    }
                }
            })
        xml = dicttoxml.dicttoxml(product_dict)

        ## INSERT CONFIG SETTINGS HERE ##
        
        req = mws.Feeds(
            access_key=aws_access_key_id, 
            secret_key=secret_key, 
            account_id=seller_id, 
            region="US"
            )
        try:
            req.submit_feed(
                feed=xml, 
                feed_type=feed_type
                )
        except:
            traceback.print_exc()