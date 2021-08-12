#!usr/bin/env python
#-*- coding:utf-8 -*-

import scrapy


class SohuSpider(scrapy.Spider):

    name = 'sohu'
    base_url = 'https://finance.sohu.com.cn/'

    def __init__(self):
        super(SohuSpider, self).__init__()

    def start_requests(self):
        pass

    def parse(self, response, **kwargs):
        pass
