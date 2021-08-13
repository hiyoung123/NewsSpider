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

    def __init__(self):
        super(NeteaseSpider, self).__init__()
        self.category = '财经'
        self.time = '08-12'

    def start_requests(self):
        for url, cate in self.cate_kv.items():
            if self.category and self.category not in cate:
                continue
            if 'tech' in url:
                for index in range(1, 21):
                    next_url = url.replace('gd2016', 'gd2016_{:0>2d}'.format(index))
                    yield scrapy.Request(next_url, self.parse_techlist)
            else:
                for index in range(1, 21):
                    next_url = url.replace('.js', '_{:0>2d}.js'.format(index))
                    yield scrapy.Request(next_url, self.parse_jslist)

    def parse(self, response, **kwargs):
        pass

    def parse_techlist(self, response):
        for index in range(1, 21):
            news_item = NewsItem()
            news_item['title'] = response.xpath(
                '//ul[@class="newsList"]/li[{}]//h3/a/text()'.format(index)).extract()
            news_item['title'] = news_item['title'][0]
            news_item['url'] = response.xpath(
                '//ul[@class="newsList"]/li[{}]//h3/a/@href'.format(index)).extract()
            news_item['url'] = news_item['url'][0]
            if not_news_url(news_item['url']):
                continue
            # news_item['attribute'] = get_attribute(response.url, news_item['url'])
            news_item['date'] = response.xpath(
                '//ul[@class="newsList"]/li[{}]//p[@class="sourceDate"]/text()'.format(index)).extract()
            news_item['date'] = news_item['date'][0][:-3]
            yield scrapy.Request(news_item['url'], self.parse_article1, meta={'news_item': news_item})

    def parse_jslist(self, response):
        news_list = json.loads(response.text[14:-1])
        for news in news_list:
            if not_news_url(news['docurl']) or news['newstype'] != 'article':
                continue
            news_item = NewsItem()
            news_item['url'] = news['docurl']
            # news_item['attribute'] = get_attribute(response.url, news_item['url'])
            news_item['date'] = get_date(news['time'])
            yield scrapy.Request(news_item['url'], self.parse_article1, meta={'news_item': news_item})

    def parse_article1(self, response):
        news_item = response.meta['news_item']
        if 'dy.163' in response.url:
            self.parse_article2(news_item, response)
            return
        news_item['title'] = response.xpath('//h1/text()').extract()
        news_item['content'] = response.xpath(
            '//div[@id="endText"]//p[not(style)]//text()').extract()
        if not news_item['content']:  # 不保存，只在日志中输出错误
            # news_item['content'] = "ERROR"
            print("news_item is None", response.url)
            return
        news_item['source'] = response.xpath(
            '//div[@class="post_time_source"]/a[@id="ne_article_source"]/text()').extract()
        # 一般来说格式是可以了，但是有些会后带一个地方分部门之类的东西，如下面注释中北京，考虑在pipeline中修改
        news_item['source_url'] = response.xpath(
            '//div[@class="post_time_source"]/a[@id="ne_article_source"]/@href').extract()
        if isinstance(news_item['source_url'], list):
            if len(news_item['source_url']) != 0:
                news_item['source_url'] = news_item['source_url'][0]
            else:
                news_item['source_url'] = 'ERROR'
        if "#" in news_item['source_url']:
            news_item['source_url'] = ''
        yield news_item

    def parse_article2(self, news_item, response):  # 网易号dy(订阅)
        news_item['title'] = response.xpath('//h2/text()').extract()
        news_item['content'] = response.xpath(
            '//div[@class="content"]//p//text()').extract()
        news_item['source'] = response.xpath(
            '//p[@class="time"]/span[3]/text()').extract()
        news_item['source_url'] = ''
        yield news_item