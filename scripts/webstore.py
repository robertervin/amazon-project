from products.models import Product

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
        return
    