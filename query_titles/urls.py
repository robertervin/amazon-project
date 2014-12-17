from django.conf.urls import patterns, url

from query_titles import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^submit/', views.scrape, name='scrape'),
)