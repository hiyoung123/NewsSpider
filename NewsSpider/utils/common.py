#!usr/bin/env python
# -*- coding:utf-8 -*-

import time


def parse_time(ctime):
    ctime = int(ctime)
    time_struct = time.strptime(time.ctime(ctime), '%a %b %d %H:%M:%S %Y')
    time_final = time.strftime("%Y-%m-%d %H:%M", time_struct)
    return time_final
