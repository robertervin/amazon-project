from products.models import Product
import dicttoxml

import traceback

from mws import mws
from amazon_api.settings import SECRET_KEY, AWS_ACCESS_KEY_ID, MWS_AUTH_TOKEN, SELLER_ID

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
        xml =  (
                '<?xml version="1.0" encoding="UTF-8"?>'
                '<AmazonEnvelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="amzn-envelope.xsd">'
                '<Header>'
                    '<DocumentVersion>1.02</DocumentVersion>'
                    '<MerchantIdentifier>M_BESTDEALS_17316086</MerchantIdentifier>'
                '</Header>'
                '<MessageType>Product</MessageType>'
                '<PurgeAndReplace>false</PurgeAndReplace>'
                '<Message>'
                    '<MessageID>1</MessageID>'
                    '<OperationType>Update</OperationType>'
                )
        for product in self.products:
            xml += ('<Product>'
                        '<SKU>' + str(product.id) + '</SKU>'
                        '<StandardProductID>'
                            '<Type>ASIN</Type>'
                            '<Value>' + str(product.ASIN) + '</Value>'
                        '</StandardProductID>'
                    '</Product>'
                    '<ProductTaxCode>A_GEN_NOTAX</ProductTaxCode>'
                    '<DescriptionData>'
                        '<Title>Example Product Title</Title>'
                        '<Brand>Example Product Brand</Brand>'
                        '<Description>This is an example product description.</Description>'
                        '<MSRP currency="USD">25.19</MSRP>'
                        '<Manufacturer>Example Product Manufacturer</Manufacturer>'
                        '<ItemType>example-item-type</ItemType>'
                    '</DescriptionData>'
                )
        # xml += xml1
        xml += '</Message></AmazonEnvelope>'

        feed_content = xml
        raw_input(xml)
        feed_type = "_POST_PRODUCT_DATA_"
        
        req = mws.Feeds(
            access_key=AWS_ACCESS_KEY_ID,
            secret_key=SECRET_KEY,
            account_id=SELLER_ID,
            region="US"
            )
        try:
            res = req.submit_feed(
                feed=xml,
                feed_type=feed_type
                )
            return res.__dict__
        except:
            traceback.print_exc()