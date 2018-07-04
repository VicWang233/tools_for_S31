# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 15:07:50 2018

@author: VicWang
"""
import sqlite3
import threading

lock = threading.Lock()

'''读写数据库类'''
class set_data_2_sql():
    #初始化连接数据库
    def __init__(self):
        self.conn = sqlite3.connect('database_ver.db',check_same_thread = False)
        self.cursor = self.conn.cursor()
        #初始化数据读取
        
        '''模拟量初始化'''
    def config_analog_quantity_init(self,data):
        #data的组成为由列表为元素构成的列表
        #创建5个表
        #name：数据显示名称（主键），item：数据，row：行，column：列，frame：所在框架
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
        '''
            #INSERT：初始化数据插入，例如行列等:x[0]:模拟量名称str，x[1]行，x[2]列
            #UPDATE:用于更新模拟量数据
            #？：占位符
            #print('data',self.data)
            #print('changdu:',len(self.data))
            #print('len(self.data[0])',len(self.data[0]))
            #s = []
        '''
        try:
            lock.acquire(True)
            
            if len(self.data) == 9:
                self.cursor.executemany('REPLACE INTO analogtable_41 (name,row,column,frame) VALUES (?,?,?,?)',[(x[0],x[1],x[2],x[3]) for x in self.data])
                #result_41 = self.cursor.execute('SELECT * FROM analogtable_41 ORDER BY name')
                #print('数据库获取的值41：',list(result_41))

            elif len(self.data) == 22:
                self.cursor.executemany('REPLACE INTO analogtable_90 (name,row,column,frame) VALUES (?,?,?,?)',[(x[0],x[1],x[2],x[3]) for x in self.data])
                #result_90 = self.cursor.execute('SELECT * FROM analogtable_90 ORDER BY name')
                #print('数据库获取的值90：',list(result_90))
    
            elif len(self.data) == 12:
                self.cursor.executemany('REPLACE INTO analogtable_81 (name,row,column,frame) VALUES (?,?,?,?)',[(x[0],x[1],x[2],x[3]) for x in self.data])
                #result_81 = self.cursor.execute('SELECT * FROM analogtable_81 ORDER BY name')
                #print('数据库获取的值81：',list(result_81))

            elif len(self.data) == 5:
                self.cursor.executemany('REPLACE INTO analogtable_82 (name,row,column,frame) VALUES (?,?,?,?)',[(x[0],x[1],x[2],x[3]) for x in self.data])
                #result_82 = self.cursor.execute('SELECT * FROM analogtable_82 ORDER BY name')
                #print('数据库获取的值82：',list(result_82))

            elif len(self.data) == 6:
                self.cursor.executemany('REPLACE INTO analogtable_83 (name,row,column,frame) VALUES (?,?,?,?)',[(x[0],x[1],x[2],x[3]) for x in self.data])
                #result_83 = self.cursor.execute('SELECT * FROM analogtable_83 ORDER BY name')
                #print('数据库获取的值83：',list(result_83))

            #执行出现问题，触发sql语法报错
        except sqlite3.Error as err:
            print("Error occurred in config_analog_quantity_init:%s"%err)
        finally:
            lock.release()
            
        self.conn.commit()    
        
        '''模拟量数据'''
    def config_analog_quantity(self,data):
        self.data_init = data
        try:
            lock.acquire(True)
            if len(self.data_init) == 9:
                #print(self.data)
                self.cursor.executemany('UPDATE analogtable_41 SET item=? WHERE name=?',[(x[0],x[1]) for x in self.data_init])
                #result_41 = self.cursor.execute('SELECT * FROM analogtable_41 ORDER BY name')
                #print("update_41",list(result_41))
            elif len(self.data_init) == 22:
                self.cursor.executemany('UPDATE analogtable_90 SET item=? WHERE name=?',[(x[0],x[1]) for x in self.data_init])
            elif len(self.data_init) == 12:
                self.cursor.executemany('UPDATE analogtable_81 SET item=? WHERE name=?',[(x[0],x[1]) for x in self.data_init])
            elif len(self.data_init) == 5:
                self.cursor.executemany('UPDATE analogtable_82 SET item=? WHERE name=?',[(x[0],x[1]) for x in self.data_init])
            elif len(self.data_init) == 6:
                self.cursor.executemany('UPDATE analogtable_83 SET item=? WHERE name=?',[(x[0],x[1]) for x in self.data_init])
        except sqlite3.Error as err:
            print("Error occurred in config_analog_quantity:%s"%err)
        finally:
            self.conn.commit()
            lock.release()
        
        
        '''开关量初始化'''
    def config_switching_value_init(self,data):
        self.switching_data_init = data
        create_table_switching_value_name = '''CREATE TABLE IF NOT EXISTS analogtable_switching_name (id INTEGER PRIMARY KEY,name VARCHAR,item VARCHAR)'''
        self.cursor.execute(create_table_switching_value_name)
        try:
            lock.acquire(True)
            self.cursor.executemany('REPLACE INTO analogtable_switching_name (name,id) VALUES (?,?)',[(x[0],x[1]) for x in self.switching_data_init])
        except sqlite3.Error as err:
            print("Error occurred in config_switching_value_init:%s"%err)
        finally:
            lock.release()
        self.conn.commit()
        
        '''开关量数据'''
    def config_switching_value(self,data):
        self.switching_data = data
        try:
            lock.acquire(True)
            self.cursor.executemany('UPDATE analogtable_switching_name SET item=? WHERE id=?',[(x[0],x[1]) for x in self.switching_data])
        except sqlite3.Error as err:
            print("Error occurred in config_switching_value:%s"%err)
        finally:
            lock.release()
        self.conn.commit()
        
        '''告警量初始化'''      
    def config_warning_value_init(self,data):
        self.warning_data_init = data
        create_table_warning_value_name = '''CREATE TABLE IF NOT EXISTS analogtable_warning_name (id INTEGER PRIMARY KEY,name VARCHAR,item VARCHAR)'''
        self.cursor.execute(create_table_warning_value_name)
        try:
            lock.acquire(True)
            self.cursor.executemany('REPLACE INTO analogtable_warning_name (name,id) VALUES (?,?)',[(x[0],x[1]) for x in self.warning_data_init])
        except sqlite3.Error as err:
            print("Error occurred in config_warning_value_init:%s"%err)
        finally:
            lock.release()
        self.conn.commit()
        
        '''告警量数据'''
    def config_warning_value(self,data):
        self.warning_data = data
        try:
            lock.acquire(True)
            self.cursor.executemany('UPDATE analogtable_warning_name SET item=? WHERE id=?',[(x[0],x[1]) for x in self.warning_data])
        except sqlite3.Error as err:
            print("Error occurred in config_warning_value:%s"%err)
        finally:
            lock.release()
        self.conn.commit()
        
        '''系统设置量初始化'''       
    def config_sys_setting_init(self,data):
        self.sys_setting_data_init = data
        create_table_sys_setting = '''CREATE TABLE IF NOT EXISTS sys_setting (id INTEGER PRIMARY KEY,name VARCHAR,item VARCHAR,remark VARCHAR)'''
        self.cursor.execute(create_table_sys_setting)
        try:
            lock.acquire(True)
            self.cursor.executemany('REPLACE INTO sys_setting (id,name,remark) VALUES (?,?,?)',[(x[0],x[1],x[2]) for x in self.sys_setting_data_init])
            #test = list(self.cursor.execute('SELECT * FROM analogtable_warning_name ORDER BY id'))
            #print('test_init',test)
        except sqlite3.Error as err:
            print("Error occurred in config_sys_setting_init:%s"%err)
        finally:
            lock.release()
        self.conn.commit()
        
        '''系统设置量数据'''
    def config_sys_setting(self,data):
        self.sys_setting_data = data
        try:
            lock.acquire(True)
            self.cursor.executemany('UPDATE sys_setting SET item=? WHERE id=?',[(x[1],x[0]) for x in self.sys_setting_data])
        except sqlite3.Error as err:
            print("Error occurred in config_sys_setting:%s"%err)
        finally:
            lock.release()
        self.conn.commit()
        
        '''整流设置量初始化'''       
    def config_rec_setting_init(self,data):
        self.rec_setting_data_init = data
        create_table_rec_setting = '''CREATE TABLE IF NOT EXISTS rec_setting (id INTEGER PRIMARY KEY,name VARCHAR,item VARCHAR,remark VARCHAR)'''
        self.cursor.execute(create_table_rec_setting)
        try:
            lock.acquire(True)
            self.cursor.executemany('REPLACE INTO rec_setting (id,name,remark) VALUES (?,?,?)',[(x[0],x[1],x[2]) for x in self.rec_setting_data_init])
            #test = list(self.cursor.execute('SELECT * FROM analogtable_warning_name ORDER BY id'))
            #print('test_init',test)
        except sqlite3.Error as err:
            print("Error occurred in config_rec_setting_init:%s"%err)
        finally:
            lock.release()
        self.conn.commit()
        
        '''整流设置量数据'''
    def config_rec_setting(self,data):
        self.rec_setting_data = data
        try:
            lock.acquire(True)
            self.cursor.executemany('UPDATE rec_setting SET item=? WHERE id=?',[(x[1],x[0]) for x in self.rec_setting_data])
        except sqlite3.Error as err:
            print("Error occurred in config_rec_setting:%s"%err) 
        finally:
            lock.release()
        self.conn.commit()
        
        '''逆变设置量初始化'''       
    def config_inv_setting_init(self,data):
        self.inv_setting_data_init = data
        create_table_inv_setting = '''CREATE TABLE IF NOT EXISTS inv_setting (id INTEGER PRIMARY KEY,name VARCHAR,item VARCHAR,remark VARCHAR)'''
        self.cursor.execute(create_table_inv_setting)
        try:
            lock.acquire(True)
            self.cursor.executemany('REPLACE INTO inv_setting (id,name,remark) VALUES (?,?,?)',[(x[0],x[1],x[2]) for x in self.inv_setting_data_init])
            #test = list(self.cursor.execute('SELECT * FROM analogtable_warning_name ORDER BY id'))
            #print('test_init',test)
        except sqlite3.Error as err:
            print("Error occurred in config_inv_setting_init:%s"%err)
        finally:
            lock.release()
        self.conn.commit()
        
        '''逆变设置量数据'''
    def config_inv_setting(self,data):
        self.inv_setting_data = data
        try:
            lock.acquire(True)
            self.cursor.executemany('UPDATE inv_setting SET item=? WHERE id=?',[(x[1],x[0]) for x in self.inv_setting_data])
        except sqlite3.Error as err:
            print("Error occurred in config_inv_setting:%s"%err)
        finally:
            lock.release()
        self.conn.commit()
        
        '''电池设置量初始化'''     
    def config_bat_setting_init(self,data):
        self.bat_setting_data_init = data
        create_table_bat_setting = '''CREATE TABLE IF NOT EXISTS bat_setting (id INTEGER PRIMARY KEY,name VARCHAR,item VARCHAR,remark VARCHAR)'''
        self.cursor.execute(create_table_bat_setting)
        try:
            lock.acquire(True)
            self.cursor.executemany('REPLACE INTO bat_setting (id,name,remark) VALUES (?,?,?)',[(x[0],x[1],x[2]) for x in self.bat_setting_data_init])
            #test = list(self.cursor.execute('SELECT * FROM analogtable_warning_name ORDER BY id'))
            #print('test_init',test)
        except sqlite3.Error as err:
            print("Error occurred in config_bat_setting_init:%s"%err)
        finally:
            lock.release()
        self.conn.commit()
        
        '''电池设置量数据'''
    def config_bat_setting(self,data):
        self.bat_setting_data = data
        try:
            lock.acquire(True)
            self.cursor.executemany('UPDATE bat_setting SET item=? WHERE id=?',[(x[1],x[0]) for x in self.bat_setting_data])
        except sqlite3.Error as err:
            print("Error occurred in config_bat_setting:%s"%err)
        finally:
            lock.release()
        self.conn.commit()
        
    '''为避免读写出现问题，把读写放入一个类里，初始化使用同一个cursor，以下为读数据库内容''' 
    '''获取用户设置量状态'''       
    def get_setting_status(self):
        '''筛选status == 1的命令,不是全部筛选，出来，遇到有为1的即返回，如果有多个，排队进入97命令修改'''
        lock.acquire(True)
        setting_command_list = list(self.cursor.execute('SELECT * FROM setting_command ORDER BY name'))
        for setting_command in setting_command_list:
            if setting_command[2] == 1:
                print(setting_command)
                lock.release()
                return setting_command
        lock.release()
        return ''
    
    '''设置完成后恢复status=0'''
    def update_setting_status(self,data):
        self.setting_status_data = data
        #print('warning_value:',self.data)
        try:
            lock.acquire(True)
            self.cursor.executemany('UPDATE setting_command SET status=? WHERE name=?',[(self.setting_status_data[1],self.setting_status_data[0])])
        except sqlite3.Error as err:
            print("Error occurred in update_setting_status:%s"%err)
        finally:
            lock.release()
        self.conn.commit()       
#set_data_2_sql = set_data_2_sql()
#set_data_2_sql.config_analog_quantity_init([['系统输出有功功率',42343242,312321],['系统输出无功功率',42343242,312321],
#['系统输出视在功率',42343242,312321],['电池电流',42343242,312321],['后备时间',42343242,312321]])