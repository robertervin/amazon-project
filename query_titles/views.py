from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from products.models import Product
from query_titles.models import Title
from query_values.models import Value
from categories.models import Category

import operator
from django.db.models import Q

# scrapers
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings

import re
from multiprocessing.pool import ThreadPool

# Scrapy Spider
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log
from amazon_scraper.amazon_scraper.spiders.amazon_scraper import AmazonSpider
from scrapy.utils.project import get_project_settings

def index(request):
    """
    Pretty much runs a Map-Reduce job on the Title-Value Sets
    
    return_objs looks like:
    [
        {T1: [V1, V2, V3]},
        {T2: [V1, V2, V3]},
        {T3: [V1, V2, V3]},
        {T4: [V1, V2, V3]},
    ]
    """
    # Limit represents the number of times the title occurs on amazon.com's query sets. Used for filtering by weight. 
    return_objs = []
    touched_titles = []
    limit = 1000
    
    def append_title(title):
        """
        Appends the title to the array along with the value set belonging to it. 
        """
        touched_titles.append(title)
        touched_values = []
        
        matched_values = Value.objects.filter(query_title__name=title).exclude(name=None).values("name")
        
        if len(matched_values) <= limit:
            print "Returned"
            return
        
        def append_value(value):
            touched_values.append(value["name"])

        # Appends the value to the value set if it's not None. 
        map(append_value, filter(lambda x: x != "None", matched_values.values()))
        
        # Sets the value set of the title if the value set is not empty.  
        if len(touched_values) > 0:
            touched_values = list(set(touched_values))
            touched_values.append(unicode("None", "utf-8"))
            print "Added Values"
            return_objs.append({
                title: reversed(touched_values)
                })

    # Loads all values for the queried titles into RAM
    titles = Title.objects.all().exclude(name=None).prefetch_related('values').values('name').distinct()
    # Makes a unique set of title strings 
    titles = list(set([title["name"] for title in titles]))
    
    # Multithreads the queried titles to grab each value set for the title.
    pool = ThreadPool()
    res = pool.map_async(append_title, titles)
    m = res.get()
    pool.close()
    
    # Returns the object to the Django Template as a dinctionary. 
    return render_to_response("list.html", dict(list_titles=return_objs), context_instance=RequestContext(request))

def scrape(request):
    """
    TODO: Filter categories which contain ALL title-value pairs
    """
    
    # Creates dictionary of title, value pairs which can be used to query the database
    new_dict = {}
    [new_dict.update({
        title: value
        }) for title, value in request._post.iteritems() if title != "csrfmiddlewaretoken" and value != "None"]
    
    # Gets the values with the matching title, value pairs
    value_lists = []
    match_count = 0
    
    count = 0
    categories = Category.objects.all()
    for t, v in new_dict.iteritems():
        # Filter by the first parameter
        if count == 0:
            categories = list(categories.filter(title__values__name=v, title__name=t))
            count = count + 1
        # If any of the other parameters don't match up, the category is invalid
        else:
            for category in categories:
                if Value.objects.filter(query_title__category=category, query_title__name=t, name=v).count() == 0:
                    categories.remove(category)
                    
    start_urls = []
    for category in categories:
        # Base URL
        base_amazon_url = "http://www.amazon.com/s/?rh=n:"
        # Base Node Id
        base_node_id = str(category.node_id)
        base_url = base_amazon_url + base_node_id
        
        node_ids = []
        p_ids = []
        for t, v in new_dict.iteritems():
            # Finds all extension nodes
            try:
                matched_value = Value.objects.get(query_title__category=category, query_title__name=t, name=v)
            except:
                continue
            
            url = matched_value.url
            
            ## Gets all node id's of matching values ##
            matched_node_ids =  re.findall("n:(\d+)", url)
            node_ids.extend(matched_node_ids)
            
            ## Gets all p_XX ids of matching values ##
            ### Returns a list of tuples like [ (36 123213), (72, KingSize) (63, 0973916) ]###
            matched_p_ids = re.findall("p_(\w+)%3(\w+)", url)
            
            if not matched_p_ids:
                matched_p_ids = re.findall("p_(\w+-\w+)%3(\w+)", url)

            p_ids.extend(matched_p_ids)
        
        # Cleans the node and p ids to remove duplicates
        node_ids = list(set(node_ids))
        p_ids = list(set(p_ids))
        
        # Creates string for node ids
        base_category_url = ",".join(["n:" + str(b) for b in node_ids])
        
        # Creates base category url
        base_query = base_url + base_category_url + ","
        
        # Creates string for node ids
        base_p_id_url = ",".join(["p_" + str(p) + ":" + str(p_id[1:]) for p, p_id in p_ids])
        
        start_url = base_query + base_p_id_url
        
        start_urls.append(start_url)

    ## UNCOMMENT THESE LINES IF YOU WANT TO DEPLOY MULTIPLE SPIDERS ##
        
    # def chunks(l, n):
    #     """ 
    #     Yield successive n-sized chunks from l.
    #     """
    #     for i in xrange(0, len(l), n):
    #         yield l[i:i+n]

    # chunked_start_urls = list(chunks(start_urls, 4))

    # def setup_crawler(_start_urls):

    # Sets up the spider with the correct settings
    spider = AmazonSpider(domain="amazon.com" )
    spider.start_urls = start_urls
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()

    # for _start_urls in chunked_start_urls:
    #     setup_crawler(_start_urls)
    
    log.start()
    reactor.run(installSignalHandlers=0)
    
    # Haha. Rarely returns since it takes so long to scrape, and the response just times out.
    return HttpResponse("Scraping " + str(len(start_urls)) + " Amazon Pages...")
