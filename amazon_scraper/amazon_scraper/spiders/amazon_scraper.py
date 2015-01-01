import scrapy
from categories.models import Category
from products.models import Product
# from reviews.models import Review
# import amazonproduct
import lxml
from django.utils import timezone
import HTMLParser
import traceback
import re
import requests
import sys

from amazon.api import AmazonAPI

from amazonproduct import API
api = API(locale='us')

# def grab_reviews(tree, product_obj):
#     raw_input(tree.xpath('//div[@class="crIframeReviewList"]')[0])
#     raw_input(lxml.objectify.dump(tree.xpath('//div[@class="crIframeReviewList"]/table/tr/td')[0]))
#     reviews_divs = tree.xpath('//table[@class="crIframeReviewList"]/tbody/tr/td/div')
#     raw_input(reviews_divs)
#     for review_div in reviews_divs:
#         review_data = []
#         review_data['content'] = review_div.xpath('.//div[@class="reviewText"]/text()').extract()[0]
#         review_data['rating'] = review_div.xpath('.//span[contains(@class, "swSprite")/@title]').extract()[0]
#         # review_data['product'] = product_obj
#         raw_input(review_data)
#         try:
#             helpful_count = re.findall('(\d+) of (\d+) people found the following review helpful', review_div.extract()) 
#             low_helpful_count = helpful_count[0]
#             high_helpful_count = helpful_count[1]
#             review_data['total_found_helpful'] = int(high_helpful_count)
#             review_data['percent_found_helpful'] = round(100-(float(low_helpful_count)/float(high_helpful_count)*100))
#         except:
#             print traceback.print_exc()
#             pass
#         raw_input(review_data)
        
#     return 

class AmazonSpider(scrapy.Spider):
    name = "amazon.com"
    allowed_domains = ["amazon.com"]
    start_urls = [
        "http://www.amazon.com/s/ref=browse_6pack_canon?node=172282,!493964,502394,281052,330405011&search-alias=photo&field-lbr_brands_browse-bin=Canon&bbn=330405011&pf_rd_p=1805817422&pf_rd_s=merchandised-search-5&pf_rd_t=101&pf_rd_i=330405011&pf_rd_m=ATVPDKIKX0DER&pf_rd_r=037VPY81K06WWP0VHQVT"
    ]

    def __init__(self, *args, **kwargs):
        super(AmazonSpider, self).__init__(*args, **kwargs)
        self.parsed_products = []

    def parse(self, response):
        """
        Parses HTML to grab necessary product information. 
        Uses a mixture of regex and dictionary parsing to grab the information.
        """

        try:
            products_grid = response.xpath('//*[contains(@id, "result_")]').extract()
            products_grid = [re.search('(B00\w+)', p) for p in products_grid]
            if not products_grid:
                return
            
            products_grid = [products_grid[p].group(0) for p in range(0, len(products_grid))]
            
            for asin in products_grid:
                print asin
                try:
                    # result = api.item_lookup(asin, ResponseGroup='Large')
                    product_data = {}
                    product_data['ASIN'] = asin
                    # product_data['title'] = result.Items.Item.ItemAttributes.Title
                    # r = HTMLParser.HTMLParser()
                    # product_data['title'] = r.unescape(product_data['title'])
                    # product_data['product_url'] = result.Items.Item.DetailPageURL
                    # try:
                    #     product_data['upc'] = result.Items.Item.ItemAttributes.UPC
                    # except:
                    #     pass
                    # product_data['price'] = result.Items.Item.ItemAttributes.ListPrice.Amount
                    # product_data['image'] = result.Items.Item.LargeImage.URL
                    # Gets url for reviews iframe
                    # reviews_url = (result.Items.Item.CustomerReviews.IFrameURL)
                    # product_data['reviews_url'] = reviews_url
                    # response = requests.get(str(reviews_url))
                    # tree = lxml.etree.HTML(response.text)
                    # has_reviews = False
                    # try:
                    #     avg_rating = float(tree.xpath('//span[@class="crAvgStars"]/span/a/img/@title')[0][:3])
                    #     num_reviews = int(re.sub('[^0-9]+', '', tree.xpath('//span[@class="crAvgStars"]/a/text()')[0]))
                    #     product_data['avg_rating'] = avg_rating
                    #     product_data['num_reviews'] = num_reviews
                    #     has_reviews = True
                    # except: #no reviews
                    #     print 'No Reviews'
                    #     pass
                    # raw_input(product_data)
                    product_obj = Product.objects.create(**product_data)
                    self.parsed_products.append(asin)
                    # product_obj = 0
                    # raw_input(has_reviews)
                    # if has_reviews:
                    #     grab_reviews(tree, product_obj)
                except:
                    traceback.print_exc()
                    continue
        except:
            print "Failed: " + response.url
            traceback.print_exc()
            return