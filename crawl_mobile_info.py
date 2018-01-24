#!/usr/bin/env python
# -*- coding:utf8 -*-
# author: BullFrog
# update: 20180124

import time
import datetime
import requests
from init_db import new_db
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('UTF-8')

db = new_db()

def crawl_mobile_info():
    # result 用于统计爬取结果数
    result = 0
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

    # 取待抓取的网站
    with open('mobile_info.txt', 'r') as f:
        for url in f.readlines():
            import_data = []    # 用于数据入库的变量
            result_tmp = []
            print "----start 正在处理 URL ：", url
            # url ="http://product.pconline.com.cn/mobile/tcl/549581_detail.html"

            mobile_res = requests.get(url, headers=header_login)
            mobile_bs = BeautifulSoup(mobile_res.content, "lxml", from_encoding='gb2312')

            try:
                name = mobile_bs.select("div .hd h3")[0]
                biaoti = name.text
            except:
                # 如果抓取不到则将 url 写入待处理文件中，以后再分析
                biaoti = "N"
                with open('mobile_info_except.txt', 'a') as e:
                    e.writelines(url)
                continue

            # 设置页面中需要抓取的字段
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

                        # 每个字段就是一个字典，key 为 canshu 中的值，value 为数据
                        # result_tmp 是以列表形式的每行数据
                        result_url[m1.text] = result_value
                        result_tmp.append(result_url)

            # 数据清洗，比对 canshu_data 与 canshu 中的数据
            canshu_data = []
            for rr in result_tmp:
                canshu_data.append(rr.keys()[0])

            # 如果 canshu 中的数据在 canshu_data 中没有，则此数据的 value 为 None
            data = set(canshu).difference(set(canshu_data))
            for d in data:
                result_tmp.append({d: 'None'})

            # 每条数据第一个字段值为手机型号
            import_data.append([biaoti])
            # 对数据按canshu 的顺序进行排序，便于数据入库
            # 将canshu中的数据值依次加入import_data 列表中
            for c in canshu:
                import_data.extend((r.values()[0] for r in result_tmp if r.keys()[0] == c))

            print "当前 URL 总共爬取 %d 个字段，数据为： %s" % (len(import_data), import_data)

            # 数据入库
            db.import_data(import_data)

            result = result + 1
            print "----end URL 爬取完成，这是爬取的 %d 个 URL" %result
        return result


def main():
    start_time = time.time()
    print "程序开始： ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
    mobile_info_num = crawl_mobile_info()

    print "--------------------------------------------------"
    print "所有手机网页爬取完成，总共爬取 %d 个手机网页" % mobile_info_num
    end_time = time.time()
    print "程序结束： ", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time))

    print "程序总耗时： ", end_time - start_time


if __name__ == '__main__':
    '''
        需要抓取的字段：
        手机类型
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


