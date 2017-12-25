#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import  HttpResponse
def hello(requests):
    return  render(requests,'temp/index.html')

