# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 15:52:59 2017

@author: jkr
"""

from rest_framework.test import APIRequestFactory
from django.test import Client
from django.test import TestCase

import json

from score.views import sctr_view

class test_sctr_post(TestCase):

    def test_1(self):

        data = '{"data":{"NVDA":[1.1,2.4,3.0], "BBY":[1,2,3,4,5,6,7,8]}}'
        
        factory  = APIRequestFactory()
        request  = factory.post('/score/api/sctr/?format=json', data, content_type='application/json')
        response = sctr_view.as_view()(request)
        response.render() 

        print response.content

