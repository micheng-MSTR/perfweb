# -*- coding: utf-8 -*-
__author__ = '程鸣'

"""
Copyright 2014 Shenma Co., Ltd.
Create time: 2015/1/4 14:06
"""

from BaseHTTPServer import HTTPServer
from CGIHTTPServer import CGIHTTPRequestHandler
import BaseHTTPServer
 
def _bare_address_string(self):
    host, port = self.client_address[:2]
    return str(host)
 
BaseHTTPServer.BaseHTTPRequestHandler.address_string = \
        _bare_address_string
     
port = 8080
httpd = HTTPServer(('', port), CGIHTTPRequestHandler)
print('Starting simple_httpd on port: ' + str(port))
httpd.serve_forever()