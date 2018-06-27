# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 15:07:50 2018

@author: VicWang
"""
import sqlite3

class set_data_2_sql():
    #初始化连接数据库
    def __init__(self):
        self.conn = sqlite3.connect('database_ver.db',check_same_thread = False)
        self.cursor = self.conn.cursor()
        #初始化数据读取
    def config_analog_quantity_init(self,data):
        #data的组成为由列表为元素构成的列表
        #创建5个表
        #id:主键，item：数据，name：数据显示名称，row：行，column：列
        self.data = data
        create_table_41 = '''CREATE TABLE IF NOT EXISTS analogtable_41 (name VARCHAR PRIMARY KEY,item VARCHAR,row INTEGER,column INTEGER,frame INTEGER)'''
        create_table_90 = '''CREATE TABLE IF NOT EXISTS analogtable_90 (name VARCHAR PRIMARY KEY,item VARCHAR,row INTEGER,column INTEGER,frame INTEGER)'''
        create_table_81 = '''CREATE TABLE IF NOT EXISTS analogtable_81 (name VARCHAR PRIMARY KEY,item VARCHAR,row INTEGER,column INTEGER,frame INTEGER)'''
        create_table_82 = '''CREATE TABLE IF NOT EXISTS analogtable_82 (name VARCHAR PRIMARY KEY,item VARCHAR,row INTEGER,column INTEGER,frame INTEGER)'''
        create_table_83 = '''CREATE TABLE IF NOT EXISTS analogtable_83 (name VARCHAR PRIMARY KEY,item VARCHAR,row INTEGER,column INTEGER,frame INTEGER)'''
        self.cursor.execute(create_table_41)
        self.cursor.execute(create_table_90)
        self.cursor.execute(create_table_81)
        self.cursor.execute(create_table_82)
        self.cursor.execute(create_table_83)
        try:
            #INSERT：初始化数据插入，例如行列等:x[0]:模拟量名称str，x[1]行，x[2]列
            #UPDATE:用于更新模拟量数据
            #？：占位符
            #print('data',self.data)
            print('changdu:',len(self.data))
            print('len(self.data[0])',len(self.data[0]))
            #s = []
            if len(self.data) == 9:
                self.cursor.executemany('REPLACE INTO analogtable_41 (name,row,column,frame) VALUES (?,?,?,?)',[(x[0],x[1],x[2],x[3]) for x in self.data])
                result_41 = self.cursor.execute('SELECT * FROM analogtable_41 ORDER BY name')
                print('数据库获取的值41：',list(result_41))
                #print(list(result_41))
                #s = list(result_41)
                #print('S41:',s)
                #self.conn.commit()
            elif len(self.data) == 22:
                self.cursor.executemany('REPLACE INTO analogtable_90 (name,row,column,frame) VALUES (?,?,?,?)',[(x[0],x[1],x[2],x[3]) for x in self.data])
                result_90 = self.cursor.execute('SELECT * FROM analogtable_90 ORDER BY name')
                print('数据库获取的值90：',list(result_90))
                #s += list(result_90)
                #print('S90:',s)
                #self.conn.commit()
            elif len(self.data) == 12:
                self.cursor.executemany('REPLACE INTO analogtable_81 (name,row,column,frame) VALUES (?,?,?,?)',[(x[0],x[1],x[2],x[3]) for x in self.data])
                result_81 = self.cursor.execute('SELECT * FROM analogtable_81 ORDER BY name')
                print('数据库获取的值81：',list(result_81))
                #s += list(result_81)
                #self.conn.commit()
            elif len(self.data) == 5:
                self.cursor.executemany('REPLACE INTO analogtable_82 (name,row,column,frame) VALUES (?,?,?,?)',[(x[0],x[1],x[2],x[3]) for x in self.data])
                result_82 = self.cursor.execute('SELECT * FROM analogtable_82 ORDER BY name')
                print('数据库获取的值82：',list(result_82))
                #s += list(result_82)
                #self.conn.commit()
            elif len(self.data) == 6:
                self.cursor.executemany('REPLACE INTO analogtable_83 (name,row,column,frame) VALUES (?,?,?,?)',[(x[0],x[1],x[2],x[3]) for x in self.data])
                result_83 = self.cursor.execute('SELECT * FROM analogtable_83 ORDER BY name')
                print('数据库获取的值83：',list(result_83))
                #s += list(result_83)
                #print('S:',s)
                #self.conn.commit()
            #self.conn.commit()
            #执行出现问题，触发sql语法报错
        except sqlite3.Error as err:
            print("Error occurred:%s"%err)
        
        
        #result_41 = self.cursor.execute('SELECT * FROM analogtable_41 ORDER BY id')
        #result_90 = self.cursor.execute('SELECT * FROM analogtable_90 ORDER BY id')
        #result_81 = self.cursor.execute('SELECT * FROM analogtable_81 ORDER BY id')
        #result_82 = self.cursor.execute('SELECT * FROM analogtable_82 ORDER BY id')
        #result_83 = self.cursor.execute('SELECT * FROM analogtable_83 ORDER BY id')
        #print('数据库获取的值41：',list(result_41))
        #print('数据库获取的值90：',list(result_90))
        #print('数据库获取的值81：',list(result_81))
        #print('数据库获取的值82：',list(result_82))
        #print('数据库获取的值83：',list(result_83))
        self.conn.commit()    
        #self.conn.close()
    def config_analog_quantity(self,data):
        self.data = data
        try:
            if len(self.data) == 9:
                self.cursor.executemany('UPDATE analogtable_41 SET item=? WHERE name=?',[(x[0],x[1]) for x in self.data])
            elif len(self.data) == 22:
                self.cursor.executemany('UPDATE analogtable_90 SET item=? WHERE name=?',[(x[0],x[1]) for x in self.data])
            elif len(self.data) == 12:
                self.cursor.executemany('UPDATE analogtable_81 SET item=? WHERE name=?',[(x[0],x[1]) for x in self.data])
            elif len(self.data) == 5:
                self.cursor.executemany('UPDATE analogtable_82 SET item=? WHERE name=?',[(x[0],x[1]) for x in self.data])
            elif len(self.data) == 6:
                self.cursor.executemany('UPDATE analogtable_83 SET item=? WHERE name=?',[(x[0],x[1]) for x in self.data])
        except sqlite3.Error as err:
            print("Error occurred:%s"%err)
        
    def config_setting_quantity(self,data):
        self.data = data
        
    def config_switching_value(self,data):
        self.data = data
        
    def config_warning_value(self,data):
        self.data = data
        
#set_data_2_sql = set_data_2_sql()
#set_data_2_sql.config_analog_quantity_init([['系统输出有功功率',42343242,312321],['系统输出无功功率',42343242,312321],
#['系统输出视在功率',42343242,312321],['电池电流',42343242,312321],['后备时间',42343242,312321]])