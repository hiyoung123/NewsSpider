#!usr/bin/env python
# -*- coding:utf-8 -*-

from scrapy.exporters import CsvItemExporter
from NewsSpider.items import NewsItem
from NewsSpider.utils.bloom import BloomFilter


class NewsCSVPipeline(object):

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def __init__(self, settings):
        self.file = open('NewsSpider/data/' + settings['EXPORTER_FILE'], 'wb')
        self.exporter = CsvItemExporter(self.file, include_headers_line=True, encoding='utf-8')
        self.exporter.start_exporting()
        # self.filter = BloomFilter()
        self.count = 0
        self.saved_list = set()

    def process_item(self, item, spider):
        if isinstance(item, NewsItem):
            # if self.filter.contains(item['news_link']):
            if item['news_link'] not in self.saved_list:
                self.exporter.export_item(item)
                self.saved_list.add(item['news_link'])
                # self.filter.insert(item['news_link'])
                self.count += 1
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        print('Saved user item size: {0}'.format(self.count))