#!/usr/bin/env python
# -*- coding:utf8 -*-
# author: tliu
# update: 20180106

import json
import requests
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')


def crawl_mobile_info():
    result = []
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


    with open('mobile_info.txt', 'r') as f:
        for line in f.readlines():
            result_tmp = []
            url = line
            print "----start 正在处理 URL ：", url
            # url ="http://product.pconline.com.cn/mobile/apple/575351_detail.html"

            mobile_res = requests.get(url, headers=header_login)
            mobile_bs = BeautifulSoup(mobile_res.content, "lxml", from_encoding='gb2312')

            # 搜索基本参数、网络支持等
            '''
            for base1 in mobile_bs.select("div .bd table th i"):
                print base1.string
                # 需要去掉最后一个 None
                print "-" * 30
            '''

            canshu = [u'上市时间', u'屏幕大小', u'屏幕分辨率', u'像素密度', u'系统', u'电池容量', u'CPU品牌', u'CPU', u'CPU频率', u'GPU', u'运行内存', u'机身容量', u'后置摄像头', u'前置摄像头', u'重量', u'尺寸']

            # 搜索手机类型、上市时间等字段的值
            for m in mobile_bs.select("div .bd tbody tr")[:-6]:
                # 页面中的一行，就是一下 start 与 end 之间的数据
                # print "-------m: start", m
                # print "-------m: end"

                for m1 in m.select("th"):
                    result_value = []

                    # 检测到一个，检查是否在需要爬取的字段中
                    # 如果是需要爬取的字段，则抓取相信信息
                    if m1.text in canshu:
                        result_url = {}
                        # print "匹配到的m1.text:", m1.text

                        # 以下针对不同信息，制定不同爬取策略。
                        # 当搜索到.poptxt class 时
                        if m.select("td .poptxt"):
                            for a in m.select("td .poptxt"):
                                result_value.append(a.text)
                        # 否则当搜索到 td 时
                        else:
                            for a in m.select("td"):
                                result_value.append(a.text.rstrip('\n\r').lstrip('\n\r'))

                        result_url[m1.text] = result_value
                        # print "aaa", result_url
                        result_tmp.append(result_url)

            # 数据清洗，比对 canshu_data 与 canshu 中的数据
            canshu_data = []
            for rr in result_tmp:
                canshu_data.append(rr.keys()[0])

            # 如果 canshu 中的数据在 canshu_data 中没有，则此数据的 value 为 None
            data = set(canshu).difference(set(canshu_data))
            for d in data:
                result_tmp.append({d: 'None'})

            print "当前 URL 总共爬取 %d 个字段，数据为： %s" % (len(result_tmp), result_tmp)
            result.append(result_tmp)
            print "----end URL 爬取完成，这是爬取的 %d 个 URL" %len(result)
        return result


def main():
    mobile_info = crawl_mobile_info()
    print "mobile_info", mobile_info
    for m in mobile_info:
        print m

    print len(mobile_info)

if __name__ == '__main__':
    '''
        需要抓取的字段：
        上市时间
        屏幕大小
        屏幕分辨率
        像素密度
        系统
        电池容量
        CPU品牌
        CPU
        CPU频率
        GPU
        运行内存
        机身容量
        后置摄像头
        前置摄像头
        重量
        尺寸
    '''
    main()


