from scrapy import signals
from scrapy.exceptions import NotConfigured

from django.core.mail import send_mail

from django.utils import timezone
from datetime import timedelta

from scripts.webstore import Publish

class AvailabilitySpider(object):
    
    def __init__(self):
        self.hide_products = Hide()

    @classmethod
    def from_crawler(cls, crawler):
        # instantiate the extension object
        ext = cls()

        # connect the extension object to signals
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)

        # return the extension object
        return ext
        
    def spider_opened(self, spider):
        spider.log("opened spider %s" % spider.name)

    def spider_closed(self, spider):
        """
        Publishes all new products to amazon webstore. 
        Hides all old products from amazon webstore.
        Sends email to administrator summarizing the new and old products. 
        """
        spider.log("Starting spider_closed operations for %s" % spider.name)        
        
        publish_products = Publish(spider.parsed_products)
        publish_products.run()
        
        email_body = ("Products hidden from your webstore: " + str(len(self.hide_products.hidden)) + "\n" + 
            "Products newly published to your webstore: " + str(len(spider.parsed_products)))
        
        send_mail("Amazon Webstore Update", email_body,
            "Robert Ervin <robert.ervin16@gmail.com>", ["robert@sparkwant.com"])

       
