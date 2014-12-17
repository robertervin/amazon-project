from django.db import models
from treebeard.mp_tree import MP_Node

class Category(MP_Node):
    name = models.CharField(max_length=100)
    node_id = models.IntegerField()

    node_order_by = ['name']

    def __unicode__(self):
        return 'Category: %s' % self.name