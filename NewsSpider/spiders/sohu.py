#!usr/bin/env python
#-*- coding:utf-8 -*-

import json
import scrapy
from ..items import NewsItem
from ..utils.common import parse_time


class SohuSpider(scrapy.Spider):

    """
        'http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=1460&page=1&size=20',    # 时政
        'http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=1461&page=1&size=20',    # 国际
        'http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=1463&page=1&size=20',    # 财经
        'http://v2.sohu.com/integration-api/mix/region/82?size=25&adapter=pc&page=1',       # 真财经
        'http://v2.sohu.com/integration-api/mix/region/5676?size=25&adapter=pc&page=1',     # 科技
        'http://v2.sohu.com/integration-api/mix/region/131?size=25&adapter=pc&page=1',      # 娱乐
        'http://v2.sohu.com/integration-api/mix/region/4357?size=25&adapter=pc&page=1',     # 体育

    """
    name = 'sohu'
    base_url = 'https://finance.sohu.com.cn/'

    start_urls = [
                  'http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=1460&page={}&size=20',  # 时政
                  'http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=1461&page={}&size=20',  # 国际
                  'http://v2.sohu.com/public-api/feed?scene=CATEGORY&sceneId=1463&page={}&size=20',  # 财经 以上三个为新闻
                  'http://v2.sohu.com/integration-api/mix/region/82?size=25&adapter=pc&page={}',  # 真·财经
                  'http://v2.sohu.com/integration-api/mix/region/5676?size=25&adapter=pc&page={}',  # 科技  翻30页
                  'http://v2.sohu.com/integration-api/mix/region/131?size=25&adapter=pc&page={}',  # 娱乐
                  'http://v2.sohu.com/integration-api/mix/region/4357?size=25&adapter=pc&page={}',  # 4357-4367都是体育，足球、篮球为主
                  'http://v2.sohu.com/integration-api/mix/region/4302?size=25&adapter=pc&page={}',  # 综合体育
                  ]

    def __init__(self):
        super(SohuSpider, self).__init__()

    def start_requests(self):
        for url in self.start_urls:
            for i in range(1, 30):
                yield scrapy.Request(url=url.format(i), callback=self.parse, dont_filter=True)

    def parse(self, response, **kwargs):
        if 'public-api' in response.url:  # 是新闻类型的API
            data_list = json.loads(response.text)
        elif 'integration-api' in response.url:
            data_list = json.loads(response.text)['data']
        else:
            return

        for data in data_list:
            if ('integration-api' in response.url) and (data['resourceType'] == 3):
                continue
            if data['type'] == 3:  # 是图集
                continue
            news_item = NewsItem()
            try:
                news_item['news_title'] = data['title']
                news_item['news_time'] = parse_time(str(data['publicTime'])[0:10])
                news_item['news_site'] = 'Sohu'
                news_item['news_comments'] = data.get('comment_total', 0)
                news_item['news_type'] = None
                news_item['news_link'] = 'http://www.sohu.com/a/' + str(data['id']) + '_' + str(data['authorId'])
            except KeyError:  # 其中一个原因：不是文章而是集合，所以没有authorId，authorName
                print(data_list.index(data))
                print(response.url)
                print(data)
                return
            yield scrapy.Request(news_item['news_link'], self.parse_news, meta={'item': news_item}, dont_filter=True)

    def parse_news(self, response):
        news_item = response.meta.get('item')
        news_item['news_content'] = response.xpath('//article[@class="article"]//p//text()').extract()
        if not news_item['news_content']:
            news_item['news_content'] = response.xpath('//article[@class="article-text"]//p//text()').extract()
        yield news_item
