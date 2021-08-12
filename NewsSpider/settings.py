#!usr/bin/env python
# -*- coding:utf-8 -*-

BOT_NAME = 'NewsSpider'

SPIDER_MODULES = ['NewsSpider.spiders']
NEWSPIDER_MODULE = 'NewsSpider.spiders'

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 1

DOWNLOADER_MIDDLEWARES = {
    'middlewares.MyUserAgentMiddleware': 101,
}

ITEM_PIPELINES = {
    'pipelines.NewsCSVPipeline': 300,
}