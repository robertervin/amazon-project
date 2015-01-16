# -*- coding: utf-8 -*-
import os
import sys
from os.path import dirname
# Scrapy settings for amazon_scraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'amazon_scraper'

SPIDER_MODULES = ['amazon_scraper.spiders']
NEWSPIDER_MODULE = 'amazon_scraper.spiders'

EXTENSIONS = {
    'amazon_scraper.extensions.custom.AvailabilitySpider': 0,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36 (+http://sparkwant.com)"

CONCURRENT_REQUESTS = 5

DOWNLOAD_TIMEOUT = 720

COOKIES_ENABLED = False

# Setting up django's settings module name.
os.environ['DJANGO_SETTINGS_MODULE'] = 'amazon_api.settings'
import django
django.setup()
