#!usr/bin/env python
# -*- coding:utf-8 -*-

import json
import scrapy
from ..items import NewsItem
from ..utils.common import parse_time


class SinaSpider(scrapy.Spider):

    """
        'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2510&k=&num=50&page=1',  # 国内
        'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2511&k=&num=50&page=1',  # 国际
        'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2512&k=&num=50&page=1',  # 体育
        'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2513&k=&num=50&page=1',  # 娱乐
        'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2514&k=&num=50&page=1',  # 军事
        'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2515&k=&num=50&page=1',  # 科技
        'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2516&k=&num=50&page=1',  # 财经
        'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2517&k=&num=50&page=1',  # 股票
        'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2518&k=&num=50&page=1',  # 美股
        'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2669&k=&num=50&page=1',  # 社会
    """

    name = 'sina'
    base_url = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid={}&k=&num=50&page={}'

    def __init__(self, category=None, time=None, *args, **kwargs):
        super(SinaSpider, self).__init__(*args, **kwargs)
        self.category = category
        self.time = time

        self.cate_id = {
            '国内': '2510',
            '国际': '2511',
            '体育': '2512',
            '娱乐': '2513',
            '军事': '2514',
            '科技': '2515',
            '财经': '2516',
            '股票': '2517',
            '美股': '2518',
            '社会': '2669',
        }
        self.id_cate = {
            '2510': '国内',
            '2511': '国际',
            '2512': '体育',
            '2513': '娱乐',
            '2514': '军事',
            '2515': '科技',
            '2516': '财经',
            '2517': '股票',
            '2518': '美股',
            '2669': '社会',
        }

    def start_requests(self):
        for url, cate in self.id_cate.items():
            if self.category and self.category not in cate:
                continue
            for i in range(1, 51):
                yield scrapy.Request(url=self.base_url.format(url, i), callback=self.parse, dont_filter=True)

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

            if self.time and self.time not in news_item['news_time']:
                continue
            yield scrapy.Request(url=data['url'], callback=self.parse_news, meta={'item': news_item}, dont_filter=True)

    def parse_news(self, response):
        news_item = response.meta.get('item')
        news_item['news_content'] = response.xpath('//div[@id="artibody"]//p//text()').extract()
        if not news_item['news_content']:
            news_item['news_content'] = response.xpath('//div[@id="article"]//p//text()').extract()
        yield news_item
