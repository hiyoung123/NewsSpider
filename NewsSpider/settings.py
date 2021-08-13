#!usr/bin/env python
# -*- coding:utf-8 -*-


import datetime


BOT_NAME = 'NewsSpider'

SPIDER_MODULES = ['NewsSpider.spiders']
NEWSPIDER_MODULE = 'NewsSpider.spiders'

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 16

# DOWNLOAD_DELAY = 1

DOWNLOADER_MIDDLEWARES = {
    'NewsSpider.middlewares.MyUserAgentMiddleware': 101,
}

ITEM_PIPELINES = {
    'NewsSpider.pipelines.NewsCSVPipeline': 300,
}

EXPORTER_FILE = "news.csv"


today = datetime.datetime.now()
log_file = 'NewsSpider/log/scrapy_{}_{}_{}.log'.format(today.year, today.month, today.day)
LOG_LEVEL = 'DEBUG'
LOG_FILE = log_file
