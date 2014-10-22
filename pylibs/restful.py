#!/usr/bin/python
# -*- coding: utf-8 -*-

"restful 0.1.0"

from BaseHTTPServer import BaseHTTPRequestHandler

class Restful(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        """
        初始化
        """
        BaseHTTPRequestHandler.__init__(self,request, client_address, server)

    def do_POST(self):
        """
        重写post方法, 接收post参数并进行相关处理
        """
        datas = self.rfile.read(int(self.headers['content-length']))
        self.processDatas(datas)

    def processDatas(self, datas):
        """
        处理通过post获取的数据
        """
        pass