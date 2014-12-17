from django.db import models
from categories.models import Category

class Title(models.Model):
    name = models.CharField(max_length=500)
    category = models.ForeignKey(Category)