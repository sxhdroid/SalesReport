#!/usr/bin/env python
# coding=utf-8

"""
__title__ = 'cookies'
__author__ = 'apple'
__mtime__ = '2018/12/4'
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
import os
import sqlite3
import win32crypt


def get_cookie(host):
    cookiepath = os.environ['LOCALAPPDATA'] + r"\Google\Chrome\User Data\Default\Cookies"
    try:
        conn = sqlite3.connect(cookiepath)
        cursor = conn.cursor()
        sql = "select host_key,name,encrypted_value " \
              "from cookies " \
              "where host_key = '%s' or host_key = '%s'" % (host, 'www' + host)
        cursor = cursor.execute(sql)
        ret_dict = {}
        for host_key, name, encrypted_value in cursor.fetchall():
            ret_dict[name] = win32crypt.CryptUnprotectData(encrypted_value)[1].decode()
        cursor.close()
        conn.close()
    except sqlite3.OperationalError as so:
        print('获取登陆信息失败，请使用Chrome浏览器登陆后重试')
        return None
    if len(ret_dict) == 0:
        return None
    if 'mmzl_sp' in ret_dict.keys():
        return ret_dict['mmzl_sp']
    elif 'PHPSESSID' in ret_dict.keys():
        return ret_dict['PHPSESSID']
    return None


if __name__ == '__main__':
    # 以下是测试代码
    cookie = get_cookie('sp.mai2.cc')
    print(cookie)