from django.contrib import admin
from query_titles.models import Title

class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
admin.site.register(Title, TitleAdmin)