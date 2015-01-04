# -*- coding: utf-8 -*-
__author__ = '程鸣'

"""
Copyright 2014 Shenma Co., Ltd.
Create time: 2015/1/4 14:00
"""

import requests

r = requests.get('http://localhost:8080/cgi-bin/get_result.py?date=20141231')
print(r.text)
