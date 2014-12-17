from categories.models import Category
from query_titles.models import Title
from query_values.models import Value
import HTMLParser
from lxml import etree
from bs4 import BeautifulSoup
import requests
import re
import sys
from lxml.html.soupparser import convert_tree

start = 6
end = 9

"""
Grabs all title: value sets by navigating to the webpage of each node with a depth in the range of start - end
and scraping the query div for information. 
"""


for category in Category.objects.filter(depth__in=range(start, end)).exclude(node_id=0):
    print str(category.node_id)
    url = 'http://www.amazon.com/b/ref=sv_fp_0?ie=UTF8&node=' + str(category.node_id)
    print url
    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
    try:
        response = s.get(url)
    except:
        print "Request Timed Out"
        continue
    tree = etree.HTML(response.text.encode('ascii','replace'))
    #if not ##TODO: query table in html:
        #return
    query_id_list = tree.xpath('//div[@id="refinements"]/ul[contains(@id, ref_)]/@id')
    for query_id in query_id_list:
        query = "//div[@id='refinements']/ul[@id=" + "'" + str(query_id) + "'" + "]"
        title = tree.xpath("//h2[following-sibling::ul[@id=" + "'" + str(query_id) + "'" + "]]/text()")
        try:
            title = title[len(title)-1]
        except:
            print "No Title"
            continue
        if Title.objects.filter(name=title, category=category).count() > 0:
            print "Title already created"
            continue
        query_title_obj = Title.objects.create(name=title, category=category)
        url = tree.xpath("//ul[@id=" + "'" + str(query_id) + "'" + "]/li/a/@href")
        if title == 'Avg. Customer Review':
            values_stars =  tree.xpath("//ul[@id=" + "'" + str(query_id) + "'" + "]/li/a/img/@alt")
            values_count =  [value for index, value in enumerate(tree.xpath("//ul[@id=" + "'" + str(query_id) + "'" + "]/li/a/span/text()")) if index%2!=0]
            values = zip(values_stars, values_count)
        else:
            values =  tree.xpath("//ul[@id=" + "'" + str(query_id) + "'" + "]/li/a/span/text()")
            it = iter(values)
            values = zip(it, it)
        #No count
        try:
            ([re.findall(r'\?\((\d+)', v[1].encode('ascii','replace')) for i, v in enumerate(values) if i%2!=0][0])
        except:
            # final_vals = []
            # print values
            # final_vals.extend([list(v) for v in values])
            # print "FINAL VALS"
            # raw_input(final_vals)
            continue
        
        for i, value in enumerate(values):
            try:
                Value.objects.create(name=value[0], count=int(re.sub('[^0-9]+', '', value[1].encode('ascii','replace'))), url='http://www.amazon.com/' + url[i], query_title=query_title_obj)
            except:
                if query_title_obj.id:
                    query_title_obj.delete()
                continue