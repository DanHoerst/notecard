from django.conf.urls import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    url(r'^about/', direct_to_template, {'template': 'about/about.html'}),
    url(r'^contact/', direct_to_template, {'template': 'about/contact.html'}),
)