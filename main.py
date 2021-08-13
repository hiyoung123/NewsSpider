#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import sys
import argparse
from scrapy.cmdline import execute


def main(args):
    sys.path.append(os.path.abspath(__file__))
    if args.category and args.time:
        execute('scrapy crawl {} -a category={} -a time={}'.format(args.spider, args.category, args.time).split())
    elif args.category:
        execute('scrapy crawl {} -a category={}'.format(args.spider, args.category).split())
    elif args.time:
        execute('scrapy crawl {} -a time={}'.format(args.spider, args.time).split())
    else:
        execute('scrapy crawl {}'.format(args.spider).split())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', dest='spider', required=True, choices=['sohu', 'sina', 'netease'], help='spider name, sohu|sina|netease')
    parser.add_argument('-c', dest='category', required=False, default=None, help='filter crawl news category.')
    parser.add_argument('-t', dest='time', required=False, default=None, help='filter crawl news time, Example mm-dd')
    # parser.add_argument('--spider', required=True, choices=['sohu', 'sina', 'netease'], help='spider name, sohu|sina|netease')
    # parser.add_argument('--category', required=False, default=None, help='filter crawl news category.')
    # parser.add_argument('--time', required=False, default=None, help='filter crawl news time, Example mm-dd')
    args = parser.parse_args()
    main(args)
