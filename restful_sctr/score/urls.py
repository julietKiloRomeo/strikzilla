# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 15:10:19 2017

@author: jkr
"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^[/]?$', views.strikzilla_view.as_view(), name='my_rest_view'),
]