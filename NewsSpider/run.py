#!usr/bin/env python
# -*- coding:utf-8 -*-

import os
from scrapy.crawler import CrawlerProcess
from NewsSpider.spiders.sina import SinaSpider
from NewsSpider.spiders.sohu import SohuSpider
from NewsSpider.spiders.netease import NeteaseSpider
from scrapy.utils.project import get_project_settings

if __name__ == "__main__":
    os.environ['SCRAPY_SETTINGS_MODULE'] = 'settings'
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(SinaSpider)
    # process.crawl(FollowSpider)
    # the script will block here until the crawling is finished
    process.start()