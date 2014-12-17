from django.db import models
from query_titles.models import Title

class Value(models.Model):
    name = models.CharField(max_length=500)
    count = models.IntegerField()
    url = models.URLField(max_length=2000)
    query_title = models.ForeignKey(Title, related_name="values")