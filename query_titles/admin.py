from django.contrib import admin
from query_values.models import Value

class ValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'count', 'query_title')
admin.site.register(Value, ValueAdmin)