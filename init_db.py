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
        A TEXT, 
        B TEXT, 
        C TEXT, 
        D TEXT, 
        E TEXT, 
        F TEXT, 
        G TEXT, 
        H TEXT, 
        I TEXT, 
        J TEXT, 
        K TEXT, 
        L TEXT, 
        M TEXT, 
        N TEXT, 
        O TEXT, 
        P TEXT, 
        Q TEXT, 
        R TEXT ) 
        """

        self.cur.execute(init_sql)
        self.conn.commit()


