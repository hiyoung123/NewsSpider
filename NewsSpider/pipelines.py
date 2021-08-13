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
        self.filter = BloomFilter()
        self.count = 0

    def process_item(self, item, spider):
        if isinstance(item, NewsItem):
            if not self.filter.contains(item['news_link']):
                self.exporter.export_item(item)
                self.filter.insert(item['news_link'])
                self.count += 1
                print('已经爬取 {}，当前为 {}'.format(self.count, item['news_link']))
            else:
                print('{} 已经存在'.format(item['news_link']))
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        print('Saved user item size: {0}'.format(self.count))
