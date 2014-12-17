from django.contrib import admin
from products.models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'ASIN', 'avg_rating', 'num_reviews',
                'product_url', 'reviews_url')
admin.site.register(Product, ProductAdmin)