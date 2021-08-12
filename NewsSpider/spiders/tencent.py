#!usr/bin/env python
# -*- coding:utf-8 -*-

import scrapy


class TencentSpider(scrapy.Spider):

    name = 'tencent'
    base_url = 'https://new.qq.com/ch/finance/'

    def __init__(self):
        super(TencentSpider, self).__init__()

    def start_requests(self):
        pass

    def parse(self, response, **kwargs):
        pass
