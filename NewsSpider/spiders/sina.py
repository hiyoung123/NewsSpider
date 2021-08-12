#!usr/bin/env python
# -*- coding:utf-8 -*-

import json
import scrapy
from ..items import NewsItem
from ..utils.common import parse_time


class SinaSpider(scrapy.Spider):

    """
        'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2512&k=&num=50&page=1',  # 体育
        'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2513&k=&num=50&page=1',  # 娱乐
        'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2514&k=&num=50&page=1',  # 军事
        'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2515&k=&num=50&page=1',  # 科技
        'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2516&k=&num=50&page=1',  # 财经
        'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2517&k=&num=50&page=1',  # 股票
        'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2518&k=&num=50&page=1',  # 美股
    """

    name = 'sina'
    base_url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid={}&k=&num=50&page={}'

    def __init__(self):
        super(SinaSpider, self).__init__()
        self.all = False
        self.category = '2512'
        self.time = '08-12'
        self.cate_id = {
            'sport': '2512',
            'ent': '2513',
            'war': '2514',
            'tech': '2515',
            'money': '2516',
            'stock': '2517',
            'usstock': '2518',
        }
        self.id_cate = {
            '2512': 'sport',
            '2513': 'ent',
            '2514': 'war',
            '2515': 'tech',
            '2516': 'money',
            '2517': 'stock',
            '2518': 'usstock',
        }

    def start_requests(self):
        if self.all:
            return self.start_requests_all()
        else:
            return self.start_requests_by_cate()

    def start_requests_all(self):
        for cate in self.cate_id.values():
            for i in range(1, 51):
                url = self.base_url.format(cate, i)
                yield scrapy.Request(url=url, meta={'cate': cate, 'page': i}, callback=self.parse, dont_filter=True)

    def start_requests_by_cate(self):
        for i in range(1, 51):
            url = self.base_url.format(self.category, i)
            yield scrapy.Request(url=url, meta={'cate': self.category, 'page': i}, callback=self.parse, dont_filter=True)

    def parse(self, response, **kwargs):
        if response.status is not 200:
            return

        response_dict = json.loads(response.text)
        data_list = response_dict['result']['data']
        lid = response_dict['result']['lid']
        for data in data_list:
            if 'video' in data['url'] or 'k.sina' in data['url']:
                continue
            news_item = NewsItem()
            # news_item['news_id'] = 0
            news_item['news_title'] = data['title']
            news_item['news_time'] = parse_time(data['ctime'])
            news_item['news_site'] = 'Sina'
            news_item['news_comments'] = data.get('comment_total', 0)
            news_item['news_type'] = self.id_cate[str(lid)]
            news_item['news_link'] = data['url']

            if self.time not in news_item['news_time']:
                continue
            yield scrapy.Request(url=data['url'], callback=self.parse_news, meta={'item': news_item}, dont_filter=True)

    def parse_news(self, response):
        news_item = response.meta.get('item')
        news_item['news_content'] = response.xpath('//div[@id="artibody"]//p//text()').extract()
        if not news_item['news_content']:
            news_item['news_content'] = response.xpath('//div[@id="article"]//p//text()').extract()
        yield news_item
