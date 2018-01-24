#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: BullFrog
# update: 20180108

import sqlite3


class new_db:
    def __init__(self):
        self.dbname = "mobile.db"
        self.conn = sqlite3.connect(self.dbname)
        self.cur = self.conn.cursor()

    def create_mobile_table(self):
        init_sql = """
        CREATE TABLE IF NOT EXISTS mobile_info ( 
        BASIC_PARAMETERS TEXT,
        NETWORK TEXT,
        SCREEN TEXT,
        HARDWARE TEXT，
        PHOTOGRAPG TEXT,
        APPEARANCE TEXT，
        DATA_APPLICATION TEXT,
        BASIC_FUNCTION TEXT，
        MULTIMEDIA TEXT
        """
        self.cur.execute(init_sql)
        self.conn.commit()


    def create_mobile_table_tmp(self):
        init_sql = """CREATE TABLE IF NOT EXISTS mobile_info_tmp (
        手机型号 TEXT,
        上市时间 TEXT, 
        屏幕大小 TEXT, 
        屏幕分辨率 TEXT, 
        像素密度 TEXT, 
        系统 TEXT, 
        电池容量 TEXT, 
        CPU品牌 TEXT, 
        CPU TEXT, 
        CPU频率 TEXT, 
        GPU TEXT, 
        运行内存 TEXT, 
        机身容量 TEXT, 
        后置摄像头 TEXT, 
        前置摄像头 TEXT, 
        重量 TEXT, 
        尺寸 TEXT)
        """

        self.cur.execute(init_sql)
        self.conn.commit()

    def import_data(self, result):
        insert_sql = "INSERT INTO " \
                    "mobile_info_tmp ('手机型号', '上市时间', '屏幕大小', '屏幕分辨率', '像素密度', '系统', '电池容量', 'CPU品牌', 'CPU', 'CPU频率', " \
                    "'GPU', '运行内存', '机身容量', '后置摄像头', '前置摄像头', '重量', '尺寸') " \
                    "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
                     (result[0][0], result[1][0], result[2][0], result[3][0], result[4][0], \
                      result[5][0], result[6][0], result[7][0], result[8][0], result[9][0], \
                      result[10][0], result[11][0], result[12][0], result[13][0], result[14][0], result[15][0], result[16][0])
        print "sql:", insert_sql
        self.cur.execute(insert_sql)
        self.conn.commit()

db = new_db()
db.create_mobile_table_tmp()