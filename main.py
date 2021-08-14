#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import sys
import argparse
from scrapy.cmdline import execute


def main(args):
    sys.path.append(os.path.abspath(__file__))
    if args.category and args.time:
        execute('scrapy crawl {} -a category={} -a time={} -s EXPORTER_FILE={}'.format(args.spider, args.category, args.time, args.file).split())
    elif args.category:
        execute('scrapy crawl {} -a category={} -s EXPORTER_FILE={}'.format(args.spider, args.category, args.file).split())
    elif args.time:
        execute('scrapy crawl {} -a time={} -s EXPORTER_FILE={}'.format(args.spider, args.time, args.file).split())
    else:
        execute('scrapy crawl {} -s EXPORTER_FILE={}'.format(args.spider, args.file).split())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', dest='spider', required=True, choices=['sohu', 'sina', 'netease'], help='spider name, sohu|sina|netease')
    parser.add_argument('-c', dest='category', required=False, default=None, help='filter crawl news category.')
    parser.add_argument('-t', dest='time', required=False, default=None, help='filter crawl news time, Example mm-dd')
    parser.add_argument('-f', dest='file', required=False, default='news.csv', help='the file name of save data, default=news.csv')
    args = parser.parse_args()
    main(args)
