Amazon Product Scraper
======================

**NOTE:** Please read the [wiki](https://github.com/RobertErvin/amazon-project/wiki) for images, and more in-depth step-by-step instructions on how to navigate the project. 

The goal of this is to run a query on all of amazon.com's product base. 

It provides an admin interface of dropdown boxes. The title/value sets of these 
boxes are scraped from amazon.com. 

When a query is submitted, multiple web scrapers are then deployed to gather
the product information for the queried parameters. The products are then saved
in the SQLite3 database for further use of the study.

## Environment

- [Django 1.7](https://docs.djangoproject.com/en/dev/releases/1.7/)  										- Python Web Framework

- [Python 2.7.6](https://www.python.org/download/releases/2.7/) 

- [SQLite3](https://docs.djangoproject.com/en/1.7/ref/settings/#databases)  								- Light Relational Database

- [Scrapy](http://scrapy.org/)  - Python Web Scraping Framework

- [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) - Python Web Scraping Module to Clean DOM

- [Python-Amazon-Simple-Product-API](https://github.com/yoavaviram/python-amazon-simple-product-api)	- Basic Python API for Querying Amazon Product API

- [Python-Amazon-Product-API](http://python-amazon-product-api.readthedocs.org/en/latest/) 	 				 - Python API for Querying Amazon Product API

- [Django-Treebeard](https://github.com/tabo/django-treebeard)												- Efficient Tree Structures for Django

## Setup

Ensure you have Python 2.7.6 by running `python -V`

Ensure you have SQLite3 by running `sqlite3 --version`

`sudo apt-get update`

`sudo apt-get install python-setuptools`

`sudo apt-get install apache2`

`sudo apt-get install libapache2-mod-wsgi`

Navigate to where `requirements.txt` is located and run `sudo pip install -r requirements.txt`

`sudo python manage.py runserver`

Copy and paste the necessary code from the **Confidential Information** google doc into `scripts/webstore.py`

Run `touch ~./amazon-product-api`, then `nano ~/.amazon-product-api` and copy and paste the necessary code from **Confidential Information** into that file and press **CTRL+O -> Enter -> CTRL+X**

The apache2 server we just installed should now boot up and you should have a url in terminal you can copy/paste into your browser.

When you navigate to the url, it should return the matching Key, Value Set Pairs that match your given query. 

Select your parameters and hit submit. your screen will time out, but if you look in your terminal, you should soon see a Twisted server spin up and deploy the web scrapers. 

## Models

##### Categories

This is a self-building tree of category strings which represent the `node_ids` of amazon search categories 

##### Products

This contains all necessary information about a standard product on amazon

##### Titles

This contains query titles one would find on a searchable amazon category page. Example titles include (price, avg rating, brand)

##### Values

This contains query values which relate to query titles one would find on a searchable amazon category page. Example values for a (price) query title might include ($1.00-$4.99, $5.00-$9.99, $10.00-$19.99)

## FAQ

##### How do I repull categories?

Run the following commands

`python manage.py shell`

`execfile('scripts/get_categories.py')`

**Note:** This might take a very long time to run. It has to make thousands of requests

##### How do I repull query titles and query values?

Open up `scripts/get_query_tables.py` and change `start` and `end` to a value you'd like. These numbers represent the depths of the category tree we will grab the query titles and query values from. The wider the range, the longer it takes to run. The smaller the `start` number, the less specification you get in terms of query titles. This applies to a very large `end` number as well. A good `start` and `end	` is `6` and `9`, respectively. The number of available query titles mapped against `start` and `end` numbers would result in a bell graph. 

##### Can I run a task when the web scraper starts or stops running?

Definitely! If you navigate to `amazon_scraper/amazon_scraper/extensions/custom.py` you'll notice `spider_opened` and `spider_closed` functions. Edit these accordinly to run whatever task you want to run.   