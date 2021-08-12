#!usr/bin/env python
#-*- coding:utf-8 -*-

import scrapy


class TonghsSpider(scrapy.Spider):

    name = 'tonghs'
    base_url = 'https://money.163.com/'

    def __init__(self):
        super(TonghsSpider, self).__init__()

    def start_requests(self):
        pass

    def parse(self, response, **kwargs):
        pass