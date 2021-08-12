#!usr/bin/env python
# -*- coding:utf-8 -*-

import scrapy


class SinaSpider(scrapy.Spider):

    name = 'sina'
    base_url = 'https://finance.sina.com.cn/'

    def __init__(self):
        super(SinaSpider, self).__init__()

    def start_requests(self):
        pass

    def parse(self, response, **kwargs):
        pass
