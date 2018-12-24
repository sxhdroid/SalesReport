#!/usr/bin/env python
# coding=utf-8

"""
__title__ = 'datautil'
__author__ = 'apple'
__mtime__ = '2018/12/7'
# code is far away from bugs with the god animal protecting
    I love animals. They taste delicious.
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
from datetime import datetime
import calendar


def getLastMonths():
    d = datetime.now()
    year = d.year
    month = d.month
    if month == 1:
        month = 12
        year -= 1
    else:
        month -= 1
    return month, year


def getMonths():
    d = datetime.now()
    year = d.year
    month = d.month
    return month, year


def getDays(m, y):
    return calendar.monthrange(y, m)


if __name__ == '__main__':
    m, y = getMonths()
    print(getDays(m, y))