from scrapy import signals
from scrapy.exceptions import NotConfigured

from django.core.mail import send_mail

from django.utils import timezone
from datetime import timedelta

class AvailabilitySpider(object):
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
        Do whatever you want when the spider is closed
        """
        spider.log('closing spider %s' % spider.name)
        execfile('./close_connection.sh')

       
