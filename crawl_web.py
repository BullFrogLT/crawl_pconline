#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: BullFrog
# update: 20180104

import re
import requests
from bs4 import BeautifulSoup
import logging
from collections import deque


# 定义LOG
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(filename)s[line:%(lineno)d] %(message)s',
    datefmt='[%Y-%m-%d %H:%M:%S]',
    filename='mobile.log',
    filemode='a'
)

que = deque()


def get_mobile_url(header_login, url_login):

    logging.info("开始处理 %s 网页数据:" %url_login,)
    web_res = requests.get(url=url_login, headers=header_login)
    if 200 == web_res.status_code:
        # 定义一个 list，存储所有手机详细信息的URL地址，后续将 list 写入文件
        mobile_list = []
        web_bs = BeautifulSoup(web_res.text, "lxml")

        # 使用BeautifulSoup搜索到所有手机信息，缩小范围
        pic_div = web_bs.select("div .item-pic")

        # 为了过滤出所有手机信息的 url，使用正则表达式
        # 结果类似 http://product.pconline.com.cn/mobile/honor/601631
        rule = 'a href="(.*?).html'
        for div in pic_div:
            a = re.findall(rule, str(div))
            if [] != a:
                # 将爬取到的所有手机详细信息添加_detail.html 标记，并将URL加入到mobile_list中
                mobile_list.append(a[0] + "_detail.html\n")

        # 将抓取到的手机URL写入文件
        with open("mobile_info.txt", "a") as f:
            f.writelines(mobile_list)

        # 将抓取到的手机URL写入列队
        # deque.extend(mobile_list)

        logging.info(" 检测到 %d 个手机网址，写入文件成功" % len(mobile_list))

        # 如果存在下一页，则返回 True ，继续爬取下一页中的手机数据
        if web_bs.select("#JlistItems li.item.item-next-page"):
            return True
        else:
            return False



def main():
    """
    本工具主要功能为抓取太平洋电脑网中的手机信息
    URL：http://product.pconline.com.cn/mobile/
    :return:
    """

    # 登录
    # 无需登录
    header_login = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'product.pconline.com.cn',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    }

    offset = 25     # 网页 URL 偏移量


    url_flag = True
    while url_flag:
        # 拼接首页的 URL
        url_login = "http://product.pconline.com.cn/mobile/{NUM}s1.shtml".format(NUM=int(-25) + offset)
        url_flag = get_mobile_url(header_login, url_login)
        offset = offset + 25    # 根据网页规则，为了定位到新网址，偏移量自增25

    # 打印性检测到手机信息总个数
    mobile_file = open("mobile_info.txt")
    mobile_num = len(mobile_file.readlines())
    logging.info("总共爬取 %d 个手机信息" %mobile_num)


if __name__ == '__main__':
    # 爬取页面信息，并抓取页面信息中的手机详细地址
    main()
