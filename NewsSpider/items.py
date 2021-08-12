#!usr/bin/env python
# -*- coding:utf-8 -*-

from scrapy import Item, Field


class NewsItem(Item):
    """ 新闻信息 """
    # news_id = Field()        # 新闻ID
    news_title = Field()     # 新闻标题
    news_content = Field()   # 新闻内容
    news_time = Field()      # 发布时间
    news_site = Field()      # 新闻来源
    news_comments = Field()  # 评论数量
    news_type = Field()      # 新闻类型
    news_link = Field()      # 新闻链接
