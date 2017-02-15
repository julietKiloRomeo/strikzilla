# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 13:53:26 2017

@author: jkr
"""

from rest_framework import serializers

class scoreSerializer(serializers.Serializer):
    score  = serializers.FloatField()
    ticker = serializers.CharField(max_length=200)
    date   = serializers.DateTimeField()
    
class priceSerializer(serializers.Serializer):
    price  = serializers.FloatField()
    ticker = serializers.CharField(max_length=200)
    date   = serializers.DateTimeField()
    
    