#!usr/bin/env python
# -*- coding:utf-8 -*-

from scrapy.exporters import CsvItemExporter
from NewsSpider.items import NewsItem


class NewsCSVPipeline(object):
    def __init__(self):
        # self.file = open('data/news.csv', 'wb')
        # self.exporter = CsvItemExporter(self.file, include_headers_line=True, encoding='utf-8')
        # self.exporter.start_exporting()
        # self.saved_list = set()
        pass

    def process_item(self, item, spider):
        # if isinstance(item, NewsItem):
        #     if item['news_id'] not in self.saved_list:
        #         self.exporter.export_item(item)
        #         self.saved_list.add(item['news_id'])
        # return item
        print(item)

    # def close_spider(self, spider):
        # self.exporter.finish_exporting()
        # self.file.close()
        # print('Saved user item size: {0}'.format(len(self.saved_list)))