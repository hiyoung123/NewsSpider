#!usr/bin/env python
# -*- coding:utf-8 -*-

BOT_NAME = 'NewsSpider'

SPIDER_MODULES = ['NewsSpider.spiders']
NEWSPIDER_MODULE = 'NewsSpider.spiders'

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 2

DOWNLOADER_MIDDLEWARES = {
}

ITEM_PIPELINES = {
    'pipelines.NewsCSVPipeline': 300,
}