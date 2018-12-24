#!/usr/bin/env python
# coding=utf-8

"""
__title__ = 'order_spider'
__author__ = 'apple'
__mtime__ = '2018/2/2'
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


import urllib.request as request
import re
import time
from pandas import DataFrame
from urllib.error import URLError
from bs4 import BeautifulSoup
from src.cookies import get_cookie
from src.datautil import *


headers = {
        'Cookie': '_EP=e8cfb4cec7de; SHOPEX_SID=4ca79540a9deda7147126d7f0128799a; PHPSESSID=rh2jnne2988ppu62077iqmquj5; q1._-=81361354',
        'Host': 'www.alifenxiao.com', 'Referer': 'http://www.alifenxiao.com/shopadmin/index.php',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

flag_stop = False


def get_order(create_b_date, create_e_date, u_name, page_size='50'):
    from urllib import parse
    u_name = parse.quote(u_name)
    # order_list_url = 'http://www.alifenxiao.com/shopadmin/index.php?ctl=order/order&act=index&_ajax=true&_h=560&_w=997&_wg=undefined'
    order_list_url = 'http://www.alifenxiao.com/shopadmin/index.php?ctl=order/order&view=&act=finder&p[0]=&p[1]=&p[2]=' \
                     '&p[3]=window.finder[%274fddc9%27]&p[4]=' + page_size + '&page=1&_finder[view]=' \
                     '&_finder[select]=multi&_finder[id]=order_id&_finder[type]=&_finder[withTools]=true' \
                     '&_finder[editMode]=&0=&create_b_date=' + create_b_date + '&create_e_date=' + create_e_date + \
                     '&update_b_date=&update_e_date=&member_name=' + u_name + '&status[]=_ANY_' \
                     '&tag[]=_ANY_&pay_status[]=_ANY_&ship_status[]=_ANY_&delivery[]=_ANY_&payment[]=_ANY_' \
                     '&create_b_h=0&create_b_m=0&create_e_h=0&create_e_m=0&o_source=all' \
                     '&_finder[orderBy]=createtime%20DESC&_finder[orderType]=&_finder[_name]=4fddc9&_ajax=true' \
                     '&_h=600&_w=884&_wg=order'
    # print(order_list_url)
    try:
        my_request = request.Request(url=order_list_url, headers=headers)
        return request.urlopen(my_request)
    except URLError as e:
        print(e)


def get_detail(order_id):
    if order_id is None:
        return None
    try:
        detail_info_url = 'http://www.alifenxiao.com/shopadmin/index.php?ctl=order/order&act=detail&p[0]=' \
                      + order_id + '&_ajax=true&_h=600&_w=853&_wg=order'
        detail_request = request.Request(url=detail_info_url, headers=headers)
        doc = request.urlopen(detail_request)
        bs_obj = BeautifulSoup(doc, 'html.parser')  # 获取页面内容转化为bs对象
        # print('详细信息', bs_obj)
        return bs_obj
    except URLError as e:
        print(e)


# 获取当前订单商品列表
def get_goods(order_id):
    if order_id is None:
        return None
    try:
        goods_info_url = 'http://www.alifenxiao.com/shopadmin/index.php?ctl=order/order&act=detail_items' \
                         '&p[0]=' + order_id + '&_ajax=true&_h=560&_w=853&_wg=order'
        detail_request = request.Request(url=goods_info_url, headers=headers)
        doc = request.urlopen(detail_request)
        bs_obj = BeautifulSoup(doc, 'html.parser')  # 获取页面内容转化为bs对象
        return bs_obj
    except URLError as e:
        print(e)


# 加载订单数据
def load_order(create_b_date, create_e_date, u_name, page_size='50'):
    orders = []
    # 分页查询指定月份的订单
    doc = get_order(create_b_date=create_b_date, create_e_date=create_e_date, u_name=u_name, page_size=page_size)
    time.sleep(0.2)
    bs_obj = BeautifulSoup(doc, 'html.parser')  # 获取页面内容转化为bs对象
    # 获取订单总数
    total_text = bs_obj.findAll(name='td', text=re.compile(r'共\d+条'))[0].text
    total = int(re.findall(r'\d+', total_text)[0])
    print('客户%s的订单条数为%s' % (u_name, total))
    mod = 0 if total % int(page_size) == 0 else 1
    # 计算总页数
    total_pages = total // int(page_size) + mod
    for page in range(total_pages):
        all_rows = bs_obj.find_all(name='div', attrs={'class': 'row'})
        # 遍历订单列表，获取需要的信息
        for order_div in all_rows:
            uname = order_div.find('div', attrs={'key': 'member_id'}).get_text().strip()  # 取得订单的分销商用户名
            if u_name != uname:  # 搜索接口请求后会搜到用户名类似的订单，所以进行过滤
                continue
            pay_status = order_div.find('div', attrs={'key': 'pay_status'}).get_text().strip()  # 取得分销商支付状态
            is_pay = 0 if pay_status == '未支付' or pay_status == '已退款' else 1  # 是否已经支付
            create_e_date = order_div.find('div', attrs={'key': 'createtime'}).get_text().strip()  # 取得下单时间
            if is_pay:
                order_id_cell = order_div.find('div', attrs={'key': 'order_id'})
                order_id = order_id_cell.get_text()  # 取得当前项的订单id
                orders.append(order_id.strip())
        if total_pages > 1:
            # 取下一页的数据
            doc = get_order(create_b_date=create_b_date, create_e_date=create_e_date, u_name=u_name, page_size=page_size)
            bs_obj = BeautifulSoup(doc, 'html.parser')  # 获取页面内容转化为bs对象
    return orders


def __get_customer(index='1', page_size='50', remark='小红'):
    from urllib import parse
    remark = parse.quote(remark)
    request_url = 'http://www.alifenxiao.com/shopadmin/index.php?ctl=distributor/fenxiaomember&view=' \
                  '&act=finder&p[0]=&p[1]=&p[2]=&p[3]=window.finder[%27640a24%27]&p[4]=' + page_size +'&page=' + index + \
                  '&_finder[view]=&_finder[select]=multi&_finder[id]=member_id&_finder[type]=' \
                  '&_finder[withTools]=true&_finder[editMode]=&confirm=1&coo_params=1&area=&minregtime=' \
                  '&maxregtime=&minadvance=&maxadvance=&remark=' + remark + '&member_lv_id[]=_ANY_&grade_id[]=_ANY_' \
                                                                            '&point[]=_ANY_&tag[]=_ANY_&sex[]=_ANY_&attrsearch___16[]=_ANY_&confirm=1&coo_params=true' \
                                                                            '&_finder[orderBy]=member_id%20desc&_finder[orderType]=&_finder[_name]=640a24' \
                                                                            '&_ajax=true&_h=600&_w=1028&_wg=member'
    my_request = request.Request(url=request_url, headers=headers)
    return request.urlopen(my_request)


def customers(remark, cb_log):
    page_size = 50  # 请求页面记录大小
    try:
        response = __get_customer(index='1', page_size=str(page_size), remark=remark)
    except URLError as e:
        if e.reason == 'Unauthorized':
            cb_log('请使用浏览器重新登录阿里分销平台之后重试')
        return
    bs_obj = BeautifulSoup(response, 'html.parser')  # 获取页面内容转化为bs对象
    # 获取总数
    total_text = bs_obj.findAll(name='td', text=re.compile(r'共\d+条'))[0].text
    total = int(re.findall(r'\d+', total_text)[0])
    mod = 0 if total % page_size == 0 else 1
    # 计算总页数
    total_pages = total // page_size + mod
    # print('总页数:', total_pages)
    time.sleep(1)
    pieces = []
    # 获取所有合作的分销商
    for page_index in range(total_pages):
        if flag_stop:
            return None
        if cb_log:
            cb_log('读取浏览器缓存中...')
        page_index += 1
        response = __get_customer(index=str(page_index), page_size=str(page_size), remark=remark)
        bs_obj = BeautifulSoup(response, 'html.parser')  # 获取页面内容转化为bs对象
        all_rows = bs_obj.find_all(name='div', attrs={'class': 'row'})
        # 遍历列表，获取分销商用户名
        for customer in all_rows:
            if flag_stop:
                return None
            uname = customer.find('div', attrs={'key': 'uname'}).text
            pieces.append(uname.strip())
    # df = DataFrame(data=pieces, columns=['分销商用户名'])
    # df.to_excel('分销商列表.xls', sheet_name='合作中分销商', index=False)
    return pieces


def build_row(order_id):
    if order_id is None:
        return
    print('开始抓取订单号为%s的数据' % order_id)
    bs_obj = get_detail(order_id=order_id)  # 获取订单详情
    time.sleep(0.1)
    goods = get_goods(order_id)  # 获取商品列表

    price = re.findall(r'\d+\.?\d*', bs_obj.find_all('th', text=re.compile(r'商品总额：'))[0].parent.td.text)[0]
    remark = bs_obj.find_all('strong', text=re.compile(r'订单备注：'))[0].parent.get_text()  # 订单备注
    out_of_stock_price = 0.0  # 订单退款金额
    if re.search(r"(退款\d+\.?\d*)", remark) is not None:  # 如果有退款
        out_of_stock_price = re.findall(r'\d+\.?\d*', re.findall(r"(退款\d+\.?\d*)", remark)[0])[0]  # 取出退款金额
    goods_a_tags = goods.find_all('a', attrs={'href': re.compile('^../index.php*'), 'target': '_blank'})  # 获取商品链接
    zypp_money = 0.0
    for tag_a in goods_a_tags:
        if re.search(r"(悦薇娅)|(ECEC)", tag_a.text):  # 是否包含有’ECEC‘和’悦薇娅‘产品
            tds = tag_a.parent.parent.find_all('td', attrs={'class': 'Colamount'})  # 获取产品价格和数量单元格
            goods_price = float(tds[0].get_text().strip())  # 商品价格
            goods_count = int(tds[1].get_text().strip())  # 购买数量
            zypp_money += goods_price * goods_count  # 自用品牌销售额
    zypp_money = float('%.2f' % zypp_money)
    zypp_real_money = zypp_money  # 实际金额

    # 组装行数据
    order_dict = {"订单号": order_id, "订单金额": float(price),
                    '缺货金额': out_of_stock_price, '实际金额': float(price) - float(out_of_stock_price),
                    '自用品牌销售额': zypp_money, '实际金额 ': zypp_real_money}
    return order_dict


def start(m, remark, cb_log=None):
    cookie = get_cookie('.alifenxiao.com')
    print('cookie %s' % cookie)
    if cookie is None:
        cb_log('获取登陆信息失败，请使用Chrome浏览器登陆后重试')
        return
    headers['Cookie'] = "PHPSESSID=%s" % cookie
    page_size = 50  # 请求页面记录大小
    create_b_date = ''  # 查询起始时间，例如2018-11-1
    create_e_date = ''  # 查询截止时间，例如2018-12-1
    fname = ''
    if m == 0:
        month, year = getLastMonths()
        cb_log('导出%d年%d月的业绩' % (year, month))
        fname = '{year}-{month}月阿里分销业绩.xls'.format(year=year, month=month)
        create_b_date = '{year}-{month}-1'.format(year=year, month=month)  # 设置查询的起始时间
        cu_month, cu_year = getMonths()  # 获取当前月份
        create_e_date = '{year}-{month}-1'.format(year=cu_year, month=cu_month)  # 设置查询结束时间
    elif m == 1:
        cu_month, cu_year = getMonths()  # 获取当前月份
        cb_log('导出%d年%d月的业绩' % (cu_year, cu_month))
        fname = '{year}-{month}月阿里分销业绩.xls'.format(year=cu_year, month=cu_month)
        create_b_date = '{year}-{month}-1'.format(year=cu_year, month=cu_month)  # 设置查询开始时间
        create_e_date = '{year}-{month}-{day}'.format(year=cu_year, month=cu_month, day=getDays(cu_month, cu_year)[1])  # 设置查询结束时间
    all_customers = customers(remark, cb_log)  # 先取得维护的客户列表
    if all_customers is None:
        return
    order_chat = list()  # 业绩数据
    i = 1
    tot = len(all_customers)
    for customer in all_customers:
        if flag_stop:
            return
        if cb_log:
            cb_log('正在导出业绩数据...%d/%d' % (i, tot))
            i += 1
        # 根据每个用户查询订单
        order_ids = load_order(create_b_date=create_b_date, create_e_date=create_e_date, u_name=customer, page_size=str(page_size))
        for order_id in order_ids:
            if flag_stop:
                return
            order_chat.append(build_row(order_id))

    try:
        # 生成业绩表
        df = DataFrame(data=order_chat)
        df.to_excel(fname, index=False, columns=["订单号", "订单金额", '缺货金额', '实际金额', '自用品牌销售额', '实际金额 '])
    except Exception as e:
        print('保存业绩表出错', e)
        cb_log('保存业绩表出错')


def stop():
    global flag_stop
    flag_stop = True


if __name__ == '__main__':
    start(0, '小红')
