# -*- coding: utf-8 -*-
__author__ = '程鸣'

"""
Copyright 2014 Shenma Co., Ltd.
Create time: 2015/1/4 14:09
"""

import cgi
import cgitb
cgitb.enable()

form_data = cgi.FieldStorage()
date = form_data.getvalue('date')
if __name__ == "__main__":
    print('\n')
    print(date)