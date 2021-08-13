#!usr/bin/env python
# -*- coding:utf-8 -*-

import json
import scrapy
from ..items import NewsItem


def not_news_url(url):
    if "photoview" in url or "://v." in url or 'nba.' in url or '2018.163' in url or 'match' in url:
        return True


def get_date(date):
    if not date:
        return '0000-00-00 00:00'
    month = date[0:2]
    day = date[3:5]
    year = date[6:10]
    hour_minute = date[11:16]
    return year + '-' + month + '-' + day + ' ' + hour_minute


class NeteaseSpider(scrapy.Spider):

    name = 'netease'
    base_url = 'https://money.163.com/'

    cate_kv = {
                  'https://temp.163.com/special/00804KVA/cm_yaowen.js': '要闻',           # 要闻 一页70条
                  'https://temp.163.com/special/00804KVA/cm_guoji.js': '国际',            # 国际
                  'https://temp.163.com/special/00804KVA/cm_guonei.js': '国内',           # 国内  前三个为新闻
                  'https://sports.163.com/special/000587PR/newsdata_n_index.js': '体育',              # 体育要闻
                  'https://sports.163.com/special/000587PR/newsdata_n_nba.js': 'NBA',              # NBA
                  'https://sports.163.com/special/000587PR/newsdata_n_world.js': '国际足球',        # 国际足球
                  'https://sports.163.com/special/000587PR/newsdata_n_china.js': '国内足球',  # 国内足球
                  'https://sports.163.com/special/000587PR/newsdata_n_cba.js': 'CBA',  # CBA
                  'https://sports.163.com/special/000587PR/newsdata_n_allsports.js': '综合',  # 综合
                  'https://ent.163.com/special/000380VU/newsdata_index.js': '娱乐',  # 娱乐首页
                  'https://ent.163.com/special/000380VU/newsdata_star.js': '明星',  # 明星
                  'https://ent.163.com/special/000380VU/newsdata_movie.js': '电影',  # 电影
                  'https://ent.163.com/special/000380VU/newsdata_tv.js': '电视剧',  # 电视剧
                  'https://ent.163.com/special/000380VU/newsdata_show.js': '综艺',  # 综艺
                  'https://ent.163.com/special/000380VU/newsdata_music.js': '音乐',  # 音乐
                  'http://tech.163.com/special/gd2016/': '科技',  # 科技滚动，这个比较特殊，有单独地滚动页面，并且收入还挺丰富，
                  'https://money.163.com/special/00259BVP/news_flow_index.js': '财经',  # 财经首页
                  'https://money.163.com/special/00259BVP/news_flow_stock.js': '股票',  # 股票
                  'https://money.163.com/special/00259BVP/news_flow_biz.js': '商业',  # 商业
                  'https://money.163.com/special/00259BVP/news_flow_licai.js': '理财',  # 理财
                  'https://money.163.com/special/00259BVP/news_flow_fund.js': '基金',  # 基金
                  'https://money.163.com/special/00259BVP/news_flow_house.js': '房产',  # 房产
                  'https://money.163.com/special/00259BVP/news_flow_car.js': '汽车',  # 汽车
    }

    def __init__(self, category=None, time=None, *args, **kwargs):
        super(NeteaseSpider, self).__init__(*args, **kwargs)
        self.category = category
        self.time = time

    def start_requests(self):
        for url, cate in self.cate_kv.items():
            if self.category and self.category not in cate:
                continue

            yield scrapy.Request(url, meta={'cate': cate}, callback=self.parse, dont_filter=True)
            if 'tech' in url:
                for index in range(2, 10):
                    next_url = url.replace('gd2016', 'gd2016_{:0>2d}'.format(index))
                    yield scrapy.Request(next_url, meta={'cate': cate}, callback=self.parse, dont_filter=True)
            else:
                for index in range(2, 10):
                    next_url = url.replace('.js', '_{:0>2d}.js'.format(index))
                    yield scrapy.Request(next_url, meta={'cate': cate}, callback=self.parse,  dont_filter=True)

    def parse(self, response, **kwargs):
        if response.status is not 200:
            return

        if response.meta.get('cate') == '科技' or 'tech' in response.url:
            return self.parse_techlist(response)
        else:
            return self.parse_jslist(response)

    def parse_techlist(self, response):
        for index in range(1, 21):
            news_item = NewsItem()
            news_item['news_title'] = response.xpath('//ul[@class="newsList"]/li[{}]//h3/a/text()'.format(index)).extract()[0]
            news_item['news_link'] = response.xpath('//ul[@class="newsList"]/li[{}]//h3/a/@href'.format(index)).extract()[0]
            if not_news_url(news_item['news_link']):
                continue
            news_item['news_type'] = response.meta.get('cate')
            news_item['news_site'] = 'Netease'
            news_item['news_comments'] = response.xpath('//ul[@class="newsList"]/li[{}]//p[@class="shareBox"]/a[@class="commentCount  "]/text()'.format(index)).extract()[0]
            news_item['news_time'] = response.xpath('//ul[@class="newsList"]/li[{}]//p[@class="sourceDate"]/text()'.format(index)).extract()[0][:-3]
            if self.time and self.time not in news_item['news_time']:
                continue
            yield scrapy.Request(news_item['news_link'], self.parse_article1, meta={'item': news_item}, dont_filter=True)

    def parse_jslist(self, response):
        data_list = json.loads(response.text[14:-1])
        for data in data_list:
            if not_news_url(data['docurl']) or data['newstype'] != 'article':
                continue
            news_item = NewsItem()
            news_item['news_link'] = data['docurl']
            news_item['news_type'] = response.meta.get('cate')
            news_item['news_time'] = get_date(data['time'])
            news_item['news_site'] = 'Netease'
            news_item['news_comments'] = data['tienum']
            if self.time and self.time not in news_item['news_time']:
                continue
            yield scrapy.Request(news_item['news_link'], self.parse_article1, meta={'item': news_item}, dont_filter=True)

    def parse_article1(self, response):
        if response.status is not 200:
            return
        news_item = response.meta['item']
        if 'dy.163' in response.url:
            self.parse_article2(news_item, response)
            return
        news_item['news_title'] = response.xpath('//h1/text()').extract()[0]
        news_item['news_content'] = response.xpath('//div[@class="post_body"]/p[not(style)]/text()').extract()
        if not news_item['news_content']:
            print("news_item is None", response.url)
            return

        yield news_item

    def parse_article2(self, news_item, response):  # 网易号dy(订阅)
        news_item['news_title'] = response.xpath('//h2/text()').extract()
        news_item['news_content'] = response.xpath('//div[@class="content"]//p//text()').extract()
        if not news_item['news_content']:
            print("news_item is None", response.url)
            return
        yield news_item
