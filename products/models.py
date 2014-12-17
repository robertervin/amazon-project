from django.db import models

class Product(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=500)
    product_url = models.URLField(max_length=1000, blank=True)
    reviews_url = models.URLField(max_length=1000, blank=True, null=True)
    ASIN = models.CharField(max_length=50, null=True, blank=True)
    avg_rating = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    num_reviews = models.IntegerField(default=0)
    price = models.IntegerField()
    upc = models.IntegerField(null=True, blank=True)
    image = models.URLField(max_length=1000)

    published = models.BooleanField(default=False)
    