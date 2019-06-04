#!/usr/bin/env python
# coding=utf-8

"""
__title__ = 'mmzl_proteams'
__author__ = 'apple'
__mtime__ = '2018/2/4'
买卖助理团队成员抓取
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

import re
import time
import urllib.request as request
from urllib.error import URLError
from bs4 import BeautifulSoup
from src.cookies import get_cookie
from src.datautil import *
from js2xml import parse, pretty_print
from lxml import html

headers = {
        'Cookie': 'ul=1; Hm_lpvt_7bfd038651e1737c7e541dcf6d879459=1519952823; Hm_lvt_7bfd038651e1737c7e541dcf6d879459=1519952823; mmzl_sp=b93tprq296g4jquupqpadbj6i3',
        'Host': 'sp.mai2.cc',
        'Referer': 'http://sp.mai2.cc/proteams',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/63.0.3239.132 Safari/537.36'
}

flag_mmzl_stop = False


# 获取团队分组
def get_team_groups(cb=None):
    print('获取团队分组')
    cookie = get_cookie('sp.mai2.cc')
    if cookie is None:
        if cb:
            cb('获取登陆信息失败，请使用Chrome浏览器重新登陆海淘后重试')
        return None
    headers['Cookie'] = "mmzl_sp=%s" % cookie
    try:
        groups_url = 'http://sp.mai2.cc/prodistr/lists'
        groups_lists = request.Request(url=groups_url, headers=headers)
        doc = request.urlopen(groups_lists)
        bs_obj = BeautifulSoup(doc, 'html.parser')  # 获取页面内容转化为bs对象
        user_config = bs_obj.select('body script')[1].string  # 获取登陆用户信息
        user_config_text = parse(user_config, debug=False)
        user_config_tree = pretty_print(user_config_text)
        user = html.etree.HTML(user_config_tree)
        mobile = user.xpath("//property[@name='mobile']/string/text()")[0]

        # 获取团队列表信息
        src = bs_obj.select('body script')[6].string
        src_text = parse(src, debug=False)
        src_tree = pretty_print(src_text)
        # 生成结果展示图一
        selector = html.etree.HTML(src_tree)
        # 自己去匹配自己想要的数据
        content = selector.xpath("//property[@name='teams']//object")
        for obj in content:
            if flag_mmzl_stop:
                return None
            owner_mobile = obj.xpath("./property[@name='owner_mobile']/string/text()")[0]  # 获取owner_mobile，来过滤数据
            if owner_mobile == mobile:
                g_id = obj.xpath("./property[@name='id']/string/text()")[0]  # 获取id，来请求维护的客户列表
                g_name = obj.xpath("./property[@name='team_name']/string/text()")[0]  # 获取id，来请求维护的客户列表
                return (g_id, g_name)
    except URLError as ue:
        if cb:
            cb('数据解析错误')
        return None
    except KeyError as ke:
        if cb:
            cb('数据解析错误')
        return None
    except ValueError as ve:
        if cb:
            cb('数据解析错误')
        return None
    return None


# 获取团队成员列表
def get_proteams(cb_log=None, remark='1UAHP'):
    print('开始抓取会员联系方式')
    if cb_log:
        cb_log('读取浏览器缓存中...')
    try:
        request_url = 'http://sp.mai2.cc/prodistr/lists?f=team&q=%s' % remark
        print(request_url)
        proteams_request = request.Request(url=request_url, headers=headers)
        doc = request.urlopen(proteams_request)
        bs_obj = BeautifulSoup(doc, 'html.parser')  # 获取页面内容转化为bs对象
        pagination_ul = bs_obj.find('div', attrs={'class': 'pagination'}).ul  # 获得分页器
        pagination_li = pagination_ul.find_all('li')  # 获得分页数
        total_pages = len(pagination_li) - 5  # 获取总页数
        page_index = 1
        pieces = []
        while page_index <= total_pages:  # 第一页已经获取到了, 所以从1开始
            if flag_mmzl_stop:
                return
            # 处理每页数据
            members_table = bs_obj.find('div', attrs={'id': 'J_distrLists'}).table
            members_mobiles = members_table.find_all('div', attrs={'class': 'distr-mobile'})  # 获取成员电话号码单元格
            for mobile_td in members_mobiles:
                if flag_mmzl_stop:
                    return
                mobile = mobile_td.get_text().strip()  # 获取电话号码
                if mobile not in pieces:
                    pieces.append(mobile)
            page_index += 1
            if page_index <= total_pages:
                # 请求下一页数据
                request_url = request_url + '&p=%s' % page_index
                proteams_request = request.Request(url=request_url, headers=headers)
                doc = request.urlopen(proteams_request)
                bs_obj = BeautifulSoup(doc, 'html.parser')  # 获取页面内容转化为bs对象

        # from pandas import DataFrame
        # df = DataFrame(data=pieces, columns=['团员联系方式'])
        # df.to_excel('./优海淘会员列表.xls', index=False)
        return pieces
    except URLError as e:
        print(e)
    except KeyError as keyError:
        print(keyError)
    except ValueError as ve:
        print(ve)


def get_orders(member, start_date, end_date, page_index='1'):

    """
     获取指定代理商指定时间内的所有订单
    :param member:
    :param start_date:
    :param end_date:
    :param page_index:
    :return: 订单页面bs对象
    """
    try:
        request_url = 'http://sp.mai2.cc/order/lists?f%5Bid%5D=&f%5Bstatus%5D=0&f%5Borigin%5D=0&f%5Btitle%5D=' \
                      '&f%5Bmobile%5D=&f%5Bdistr%5D=&f%5Bdistr_name%5D=&f%5Bdistr_mobi%5D=' + member + '&f%5Btn%5D=' \
                      '&f%5Border_start%5D=' + start_date + '+00%3A00%3A00&f%5Border_end%5D=' + end_date + '+23%3A59%3A59' \
                      '&f%5Bpay_start%5D=&f%5Bpay_end%5D=&f%5Bproduct_id%5D=&p=' + page_index
        order_request = request.Request(url=request_url, headers=headers)
        doc = request.urlopen(order_request)
        bs_obj = BeautifulSoup(doc, 'html.parser')  # 获取页面内容转化为bs对象
        if bs_obj is None:
            return None
        order_table = bs_obj.find('div', attrs={'id': 'J_orderLists'}).table  # 获取装载订单列表的容器
        try:
            if order_table.attrs['class'][0] == 'no-item':  # 这种情况下没有订单
                return None
        except KeyError:  # 如果出现异常了，证明有订单列表
            pass
        orders = order_table.find_all(lambda tag: tag.name == 'tr' and len(tag.attrs) > 0)  # 订单项
        pagination = bs_obj.find('div', attrs={'class': 'pagination'})  # 获得分页器
        return orders, pagination
    except Exception as e:
        print(e)


# 生成业绩表
def build_achievement(m, cb_log=None, remark='1UAHP'):
    cookie = get_cookie('sp.mai2.cc')
    if cookie is None:
        if cb_log:
            cb_log('获取登陆信息失败，请使用Chrome浏览器重新登陆海淘后重试')
        return
    headers['Cookie'] = "mmzl_sp=%s" % cookie
    members = get_proteams(cb_log=cb_log, remark=remark)  # 所有代理商
    # import pandas as pd
    # members = pd.read_excel('./优海淘会员列表.xls')['团员联系方式']
    # members = ['15107478373']
    if members is None:
        if cb_log:
            cb_log('获取信息失败，请使用Chrome浏览器重新登陆海淘后重试')
        return
    time.sleep(1)
    order_chat = []  # 业绩数据
    start_date = ''  # 查询起始时间，例如2018-11-1
    end_date = ''  # 查询截止时间，例如2018-11-30

    fname = ''
    if m == 0:
        month, year = getLastMonths()
        if cb_log:
            cb_log('导出%d年%d月的业绩' % (year, month))
        fname = '{year}-{month}月优海淘业绩.xls'.format(year=year, month=month)
        start_date = '{year}-{month}-1'.format(year=year, month=month)  # 设置查询的起始时间
        end_date = '{year}-{month}-{day}'.format(year=year, month=month, day=getDays(month, year)[1])  # 设置查询结束时间
    elif m == 1:
        cu_month, cu_year = getMonths()  # 获取当前月份
        if cb_log:
            cb_log('导出%d年%d月的业绩' % (cu_year, cu_month))
        fname = '{year}-{month}月优海淘业绩.xls'.format(year=cu_year, month=cu_month)
        start_date = '{year}-{month}-1'.format(year=cu_year, month=cu_month)  # 设置查询开始时间
        end_date = '{year}-{month}-{day}'.format(year=cu_year, month=cu_month, day=getDays(cu_month, cu_year)[1])  # 设置查询结束时间

    for i in range(len(members)):
        if flag_mmzl_stop:
            return
        member = str(members[i])
        print('开始抓取会员%s的订单' % member)
        if cb_log:
            cb_log('正在导出业绩数据...%d/%d' % (i + 1, len(members)))
        result = get_orders(member, start_date=start_date, end_date=end_date)  # 获取代理商的订单
        if result is None:
            time.sleep(0.1)
            continue
        orders = result[0]  # 订单项
        pagination = result[1]  # 获得分页器
        if pagination is not None:  # 如果只有一页，则无此容器
            pagination_li = pagination.ul.find_all('li')
            total_pages = len(pagination_li) - 5  # 获取总页数，除去5个跳转链接，剩下的就是页数连接
        else:
            total_pages = 1
        page_index = 1
        while page_index <= total_pages:  # 第一页已经获取到了, 所以从1开始
            if flag_mmzl_stop:
                return
            # 处理每页数据
            if page_index != 1:  # 第一页数据已经加载
                result = get_orders(member, start_date=start_date, end_date=end_date, page_index=str(page_index))
                orders = result[0]  # 订单项

            row_index = 0
            while row_index < len(orders):  # 真正的订单数据
                if flag_mmzl_stop:
                    return
                # 由于每个订单包含两行,所以依次取两行
                # 订单id
                order_id = orders[row_index].find_all('span', attrs={'class': 'order-id'})[0].get_text().strip()
                print('    开始处理会员%s的订单%s' % (member, order_id))
                row_item = orders[row_index + 1]
                row_index += 2
                # 获取订单状态
                status = row_item.find_all('td')[2].get_text().strip()
                if status == '已关闭' or status == '已取消':
                    print('    订单%s无效' % order_id)
                    continue

                # 获取订单总额单元格
                # amounts_td = row_item.find_all('td')[1].find_all(lambda tag: tag.name == 'div' and len(tag.attrs) == 0)
                # print('%s的订单总额信息%s' % (order_id, amounts_td))
                # 订单总金额
                # amount_money = float(re.findall(r'\d+\.?\d*', amounts_td[0].get_text().strip())[0])  # 订单总额数值
                # if re.search(r'\d+\.?\d*', amounts_td[1].get_text().strip()):
                #     freight = float(re.findall(r'\d+\.?\d*', amounts_td[1].get_text().strip())[0])  # 获取运费
                # else:
                #     freight = 0.0
                # money = float('%.2f' % (amount_money - freight))  # 计算订单除去运费金额

                # 处理每个订单下所有商品
                goods_container = row_item.find_all('div', attrs={'class': 'row-item'})  # 获取商品列表容器
                money = 0.0  # 订单总价
                out_of_stock_money = 0.0  # 缺货金额
                vivi_money = 0.0  # VIVIrain 包
                zypp_money = 0.0  # 自用品牌金额
                zypp_real_money = 0.0  # 自用品牌真实金额
                for goods in goods_container:
                    if flag_mmzl_stop:
                        return
                    # 商品名称
                    goods_name = goods.find('div', attrs={'class': 'goods-name'}).get_text().strip()
                    # 商品数量
                    # goods_count = int(goods.find('div', attrs={'class': 'col-quantity'}).div.get_text().strip())
                    # 商品结算价
                    price = float(re.findall(r'\d+\.?\d*',
                                             goods.find('div', attrs={'class': 'col-price'}).get_text().strip())[0])
                    money += price
                    goods_tag = goods.find('li', attrs={'class': 'goods-tag'})  # 是否退款标签
                    is_refund = goods_tag is not None
                    if is_refund:
                        print('        订单%s退款了' % order_id)
                        # 退款了
                        out_of_stock_money += price  #

                    if re.search(r"(悦薇娅)|(ECEC)", goods_name) and not is_refund:  # 是否包含有’ECEC‘和’悦薇娅‘产品
                        zypp_money += price  # 自用品牌销售额
                    elif re.search(r".*VIVIrain.*包.*", goods_name):  # VIVIrain 品牌包
                        vivi_money += price  # 销售额
                    zypp_real_money = zypp_money  # 实际金额

                # 组装行数据
                order_dict = {"订单号": order_id, "订单金额": money, '缺货金额': out_of_stock_money,
                              '实际金额': money - out_of_stock_money, 'VIVIrain 包': vivi_money,
                              '自用品牌销售额': zypp_money, '实际金额 ': zypp_real_money
                              }
                # print(order_dict)
                order_chat.append(order_dict)

            # 准备加载下一页
            page_index += 1  # 页索引增加

    try:
        from pandas import DataFrame
        df = DataFrame(data=order_chat)
        df.to_excel(fname, index=False, columns=["订单号", "订单金额", '缺货金额', '实际金额', 'VIVIrain 包', '自用品牌销售额', '实际金额 '])
        if cb_log:
            cb_log('导出优海淘业绩完成')
    except Exception as e:
        print('保存业绩表出错', e)
        if cb_log:
            cb_log('保存业绩表出错')


def stop_mmzl():
    global flag_mmzl_stop
    flag_mmzl_stop = True


if __name__ == '__main__':
    build_achievement(0)
