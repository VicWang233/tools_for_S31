# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 21:09:58 2018

@author: VicWang


s.strip()     #开头和结尾
s.lstrip()   #开头
s.rstrip()  #结尾

#import binascii
#------------------------------------------------------
#各种转换
a = 0x0A  #表示16进制数
b = 10    #表示10进制数
print(hex(b)) #10转16                输出0xa
print(a)  #输出10进制数             输出10
print((b'a')) #转换为bytes供串口传输   输出b'a'
print(chr(49))   #10进制整形转换成对应ASCII字符 输出1
print(chr(0x31))  #16进制整形转换成对应ASCII字符 输出1
print(hex(ord('1')))    #ASCII转16进制，输出0x31
print((ord('1')))     #ASCII转10进制，输出49
print(int('1010',2))   #2进制转10进制
print(bin(10))        #十进制转2进制
#-------------------------------------------------------

"""
import logging
import tkinter as tk
from tkinter import simpledialog
import serial.tools.list_ports as list_ports
import serial
import time
from configparser import ConfigParser   #取configparser模块中的ConfigParser类
import threading
import ctypes
import tkinter.font as tkFont
import share_variable
import protocol_config_apply_to_get_analog_quantity as protocol
import protocol_config_apply_to_get_sysdata as protocol_sysdata
import protocol_config_apply_to_get_switching_value as protocol_switch
import protocol_config_apply_to_get_warning_value as protocol_warning
import protocol_config_for_history_event as protocol_history
import protocol_config_for_fault_event as protocol_fault
import sql_config
import os
import csv

'''
数据库操作初始化
'''
sql = sql_config.set_data_2_sql()


'''
函数名称：destory
功能描述：点击后关闭窗口，并且清除对应窗口后台运行的其他线程
参数意义：parent：表示要毁灭的窗口对象。
函数调用：sql.clear_all_value():详见sql_config.py
'''
def destory(parent):
    sql.clear_all_value()
    parent.destroy()
    os._exit(0) 
'''
-------------------------------------------------------------------------------
文件类函数定义
-------------------------------------------------------------------------------
'''
###########指定section和option的序号调出参数名###########
'''
类名称：cfg_tool
功能描述:从cfg文件中调取需要的内容
参数意义：ConfigParser：处理cfg、ini、conf等文件的包
'''
class cfg_tool(ConfigParser):           #继承父类
    '''
    函数名称：__init__(self,filename)
    功能描述：初始化cfg文件类函数，即执行下面类的其他函数时会默认先执行此函数。
    参数意义：self：表示类本身(后面将不在解释self)。filename:表示要读取的文件名
    函数调用：read:读文件。sections：选取cfg中所有的section(形如[analog_num])，返回一个列表
    '''
    def __init__(self,filename):                 #初始化，定义需要搞的cfg文件名，
        self.filename = filename
        self.conf = ConfigParser(allow_no_value=True,strict = False)    #定义加载cfg文件的对象
        self.conf.read(self.filename)                          #读cfg文件
        self.sections = self.conf.sections()
    '''
    函数名称：Pick_Section_number(self,section_num_you_choose)
    功能描述：从sections列表中寻找指定的section
    参数意义：section_num_you_choose:指定的section
    函数调用：无
    '''  
    def Pick_Section_number(self,section_num_you_choose):
        for section in self.sections:                          #循环找出对应的section
            if section == section_num_you_choose:
                return int(self.conf.options(section)[0])
        
    '''
    函数名称：Pick_Option_In_Section(self,section_you_choose,option_row_you_choose,option_list_i,*args)
    功能描述：选出cfg某section中的某行的某个元素
    参数意义：section_you_choose:所选section，格式为字符串。option_row_you_choose：所选行。option_list_i：所选列。*args:可选参数，预留。
    函数调用：items：返回section_you_choose下所有option。isinstance：判断是否为同一类型的变量
    '''  
    def Pick_Option_In_Section(self,section_you_choose,option_row_you_choose,option_list_i,*args):
                options = self.conf.items(section_you_choose)
                option = list(options[option_row_you_choose])[0].split('\t')[option_list_i]
                if option == 'a' or option == 'b' or option == 'c':
                    return ''
                else:
                    if isinstance(args,(str)):
                        option = args
                        print(option)
                    else:
                        return option
    
    '''
    函数名称：Pick_Option(self,section_you_choose,option_row_you_choose)
    功能描述：选出所选的行
    参数意义：section_you_choose:所选section，格式为字符串。option_row_you_choose：所选行。
    函数调用：无
    ''' 
    def Pick_Option(self,section_you_choose,option_row_you_choose):
        options = self.conf.items(section_you_choose)
        return list(options[option_row_you_choose])[0].split('\t')
#######一下函数暂时用不到#######
    '''
    函数名称：Change_Value_In_CFG(self,section_you_choose,option_you_choose,new_option_value)
    功能描述：改变cfg中某个元素的值
    参数意义：section_you_choose:所选section，格式为字符串。option_row_you_choose：所选行。new_option_value：新值
    函数调用：无
    '''     
    def Change_Value_In_CFG(self,section_you_choose,option_you_choose,new_option_value):
        self.openfile = open(self.filename,'w')
        self.conf.set(section_you_choose,option_you_choose,new_option_value)
        self.conf.write(self.openfile)
        self.openfile.close()
        print("%s的值%s改为%s"%(section_you_choose,option_you_choose,new_option_value))
        #return self.conf.get(section_you_choose,option_row_you_choose)
        #####专门获取系统[Config_for_Sysdata]中的传入值,再把Config_for_Sysdata中的值清空####
    
  
'''
类名称：logging_file()
功能描述:logging模块输出日志类，输出log文件日志
参数意义：无
函数调用：无
'''              
class logging_file():
    '''
    函数名称：__init__(self)
    功能描述：初始化logging
    参数意义：无
    函数调用：basicConfig：log输出文件基本配置
    '''  
    def __init__(self):
        logging.basicConfig(
            level = logging.INFO,
            format = '%(asctime)s %(message)s',
            filename = 'toolss.log',
            filemode = 'w'
                            )
    '''
    函数名称：print_the_logging(self,CID2,status_for_IO,message)
    功能描述：输出log到log日志文件
    参数意义：CID2：CID2。status_for_IO:判断是读命令还是写命令,message：命令字符串
    函数调用：info：输出字符串到log
    '''  
    def print_the_logging(self,CID2,status_for_IO,message):
        self.message = message
        self.status_for_IO = status_for_IO
        self.CID2 = CID2
        #logging.info('CID2:'+self.CID2+','+self.status_for_IO+':'+self.message)
        logging.info('%s%s%s%s%s%s'%('CID2:',self.CID2,',',self.status_for_IO,':',self.message))
        
'''
类名称：output_csv()
功能描述:输出列表至csv文件
参数意义：无
函数调用：无
''' 
class output_csv():
    '''
    函数名称：__init__(self)
    功能描述：初始化csv类
    参数意义：无
    函数调用：writer：确定csv文件名，以及根据','来判断分割点。writerow:把一个列表写入csv的行，每个元素占一行
    '''  
    def __init__(self):
        if share_variable.polling_status == '3':
            self.cfg_tool_for_history = cfg_tool('ToolsDebugChs.cfg')
            self.filename = '历史记录%s.csv'%(time.strftime('%Y-%m-%d,%H-%M-%S'))
            with open(self.filename,'a',newline = '') as csv_out_file:
                self.filewriter = csv.writer(csv_out_file,delimiter = ',')
                self.index = ['事件名称','ID','事件日期','事件事件','事件状态','事件等级']
                self.filewriter.writerow(self.index)
        elif share_variable.polling_status == '4':
            self.filename = '故障点数据%s-%s.csv'%(share_variable.fault_file_status,time.strftime('%Y-%m-%d,%H-%M-%S'))
            with open(self.filename,'a',newline = '') as csv_out_file:
                self.filewriter = csv.writer(csv_out_file,delimiter = ',')
                self.index = ['记录编号','记录意义','第一点(最新点)','第二点','第三点','第四点']
                self.filewriter.writerow(self.index)
    '''
    函数名称：Output_csv_for_analog_quantity(self)
    功能描述：输出模拟量数据到csv文件
    参数意义：无
    函数调用：无
    '''
    def Output_csv_for_analog_quantity(self):
        with open('模拟量数据保存.csv','w',newline = '') as csv_out_file: 
            self.filewriter = csv.writer(csv_out_file,delimiter = ',')
            self.filewriter.writerow(self.receive_data)

    '''
    函数名称：Output_csv_for_history_event(self,receive_data)
    功能描述：输出历史记录数据到csv文件
    参数意义：receive_data：接收到的数据
    函数调用：protocol_analyse：详见protocol_config_for_history_event.py
    '''
    def Output_csv_for_history_event(self,receive_data):
        self.receive_data = receive_data
        self.data = protocol_history.protocol_analyse(self.receive_data,self.cfg_tool_for_history)
        with open(self.filename,'a',newline = '') as csv_out_file:
            self.filewriter = csv.writer(csv_out_file,delimiter = ',')
            self.filewriter.writerow(self.data)   #加载列 deque形式为([1,2,3,4,5,6],[6,5,4,3,2,1],etc..)
    '''
    函数名称：Output_csv_for_fault_event(self,status,receive_data_time,receive_data_name,receive_data_value_1,receive_data_value_2,receive_data_value_3,receive_data_value_4)
    功能描述：输出故障点数据到csv文件
    参数意义：详细见下面。
    函数调用：calc_receive_fault_data_in_xxx,calc_receive_fault_data_in_bits
    '''                    
    def Output_csv_for_fault_event(self,status,receive_data_time,receive_data_name,receive_data_value_1,receive_data_value_2,receive_data_value_3,receive_data_value_4):
        '''
        status = 1 表示整流   
        status = 2 表示逆变 
        receive_data_time 表示解析出的时间
        receive_data_value_1~4 表示四个点的数据
        num代表数据量，整流239，逆变149
        row0_Rec代表cfg第一列
        '''
        self.status = status
        self.receive_data_time = receive_data_time
        self.receive_data_name = receive_data_name
        self.receive_data_value_1 = receive_data_value_1
        self.receive_data_value_2 = receive_data_value_2
        self.receive_data_value_3 = receive_data_value_3
        self.receive_data_value_4 = receive_data_value_4
        with open(self.filename,'a',newline = '') as csv_out_file:
            self.filewriter = csv.writer(csv_out_file,delimiter = ',')
            '''整流部分'''
            if self.status == 1:
                num_Rec = share_variable.fault_num_rec
                row0_Rec = share_variable.fault_row0_list_for_rec
                for i in range(num_Rec): 
                    if share_variable.fault_row4_list_for_rec[i] == 'xxx':
                        '''整流-处理成数字的部分'''
                        data_1 = self.calc_receive_fault_data_in_xxx(i,self.receive_data_value_1[int(row0_Rec[i])-1],'Rec')
                        data_2 = self.calc_receive_fault_data_in_xxx(i,self.receive_data_value_2[int(row0_Rec[i])-1],'Rec')
                        data_3 = self.calc_receive_fault_data_in_xxx(i,self.receive_data_value_3[int(row0_Rec[i])-1],'Rec')
                        data_4 = self.calc_receive_fault_data_in_xxx(i,self.receive_data_value_4[int(row0_Rec[i])-1],'Rec')
                        self.write_row_list = [i,self.receive_data_name[i],data_1,data_2,data_3,data_4]                        
                    else:
                        ''' 整流-'Y'来判断数值的部分'''
                        if share_variable.fault_row2_list_for_rec[i] == 'bits':
                            '''整流-多位判断'''
                            data_1 = self.calc_receive_fault_data_in_bits(i,self.receive_data_value_1[int(row0_Rec[i])-1],'Rec','bits')
                            data_2 = self.calc_receive_fault_data_in_bits(i,self.receive_data_value_2[int(row0_Rec[i])-1],'Rec','bits')
                            data_3 = self.calc_receive_fault_data_in_bits(i,self.receive_data_value_3[int(row0_Rec[i])-1],'Rec','bits')
                            data_4 = self.calc_receive_fault_data_in_bits(i,self.receive_data_value_4[int(row0_Rec[i])-1],'Rec','bits')
                        else:
                            '''整流-单位判断'''
                            data_1 = self.calc_receive_fault_data_in_bits(i,self.receive_data_value_1[int(row0_Rec[i])-1],'Rec','bit')
                            data_2 = self.calc_receive_fault_data_in_bits(i,self.receive_data_value_2[int(row0_Rec[i])-1],'Rec','bit')
                            data_3 = self.calc_receive_fault_data_in_bits(i,self.receive_data_value_3[int(row0_Rec[i])-1],'Rec','bit')
                            data_4 = self.calc_receive_fault_data_in_bits(i,self.receive_data_value_4[int(row0_Rec[i])-1],'Rec','bit')
                           # print('bit_datalist:',[self.receive_data_value_1[num],self.receive_data_value_2[num],self.receive_data_value_3[num],self.receive_data_value_4[num]])
                        self.write_row_list = [i,self.receive_data_name[i],data_1,data_2,data_3,data_4]
                    self.filewriter.writerow(self.write_row_list)  
                    '''逆变部分'''
            else:
                num_Inv = share_variable.fault_num_inv
                row0_Inv = share_variable.fault_row0_list_for_inv
                for i in range(num_Inv):    
                    if share_variable.fault_row4_list_for_inv[i] == 'xxx':
                        '''逆变-处理成数字的部分'''
                        data_1 = self.calc_receive_fault_data_in_xxx(i,self.receive_data_value_1[int(row0_Inv[i])-1],'Inv')
                        data_2 = self.calc_receive_fault_data_in_xxx(i,self.receive_data_value_2[int(row0_Inv[i])-1],'Inv')
                        data_3 = self.calc_receive_fault_data_in_xxx(i,self.receive_data_value_3[int(row0_Inv[i])-1],'Inv')
                        data_4 = self.calc_receive_fault_data_in_xxx(i,self.receive_data_value_4[int(row0_Inv[i])-1],'Inv')
                        self.write_row_list = [i,self.receive_data_name[i],data_1,data_2,data_3,data_4]
                    else:
                        ''' 逆变-'Y'来判断数值的部分 '''
                        if share_variable.fault_row2_list_for_inv[i] == 'bits':
                            '''逆变-多位判断'''
                            data_1 = self.calc_receive_fault_data_in_bits(i,self.receive_data_value_1[int(row0_Inv[i])-1],'Inv','bits')
                            data_2 = self.calc_receive_fault_data_in_bits(i,self.receive_data_value_2[int(row0_Inv[i])-1],'Inv','bits')
                            data_3 = self.calc_receive_fault_data_in_bits(i,self.receive_data_value_3[int(row0_Inv[i])-1],'Inv','bits')
                            data_4 = self.calc_receive_fault_data_in_bits(i,self.receive_data_value_4[int(row0_Inv[i])-1],'Inv','bits')
                            #if i == 20:
                            #    print('20:data_1',data_1)
                            #    print('20:int(row0_Inv[i])-1',int(row0_Inv[i])-1)
                        else:
                            '''逆变-单位判断'''
                            data_1 = self.calc_receive_fault_data_in_bits(i,self.receive_data_value_1[int(row0_Inv[i])-1],'Inv','bit')
                            data_2 = self.calc_receive_fault_data_in_bits(i,self.receive_data_value_2[int(row0_Inv[i])-1],'Inv','bit')
                            data_3 = self.calc_receive_fault_data_in_bits(i,self.receive_data_value_3[int(row0_Inv[i])-1],'Inv','bit')
                            data_4 = self.calc_receive_fault_data_in_bits(i,self.receive_data_value_4[int(row0_Inv[i])-1],'Inv','bit')
                        self.write_row_list = [i,self.receive_data_name[i],data_1,data_2,data_3,data_4]
                    self.filewriter.writerow(self.write_row_list)
            self.filewriter.writerow([self.receive_data_time])

    '''
    函数名称：calc_receive_fault_data_in_xxx(self,row,value,rec_or_inv)
    功能描述：故障点数据算法函数(xxx的情况)
    参数意义：row：行。value：值。rec_or_inv：整流or逆变
    函数调用：round：百度
    '''       
    def calc_receive_fault_data_in_xxx(self,row,value,rec_or_inv):
        '''
        根据cfg第6个字符串来判断需要对数据进行哪些操作，
        calcvalue为接收到的原始数据
        '''   
        self.calcvalue = int(value,16)
        if rec_or_inv == 'Rec':
            if share_variable.fault_row6_list_for_rec[row] == '10':
                return round(self.calcvalue/10,2)
            elif share_variable.fault_row6_list_for_rec[row] == '1024-ms-dv':
                return round(self.calcvalue/1024*1000/3/1.732,2)
            elif share_variable.fault_row6_list_for_rec[row] == '100':
                return round(self.calcvalue/100,2)
            elif share_variable.fault_row6_list_for_rec[row] == '4096-ms-dv':
                return round(self.calcvalue/4096*1000/3/1.732,2)
            elif share_variable.fault_row6_list_for_rec[row] == 'xxx':
                return ''
            else:
                return '?'
        elif rec_or_inv == 'Inv':
            #print("fault_cfg_tool.Pick_Option_In_Section('Inv',row,6)",fault_cfg_tool.Pick_Option_In_Section('Inv',row,6))
            if share_variable.fault_row6_list_for_inv[row] == '1024-ms-dv':
                return round(self.calcvalue/1024*1000/3/1.732,2)
            elif share_variable.fault_row6_list_for_inv[row] == '1024-mv':
                return round(self.calcvalue/1024/1.732,2)
            elif share_variable.fault_row6_list_for_inv[row] == '100':
                return round(self.calcvalue/100,2)
            elif share_variable.fault_row6_list_for_inv[row] == '1024-ms-m8-d10':
                return round(self.calcvalue/1024*1000/3*8/10,2)
            elif share_variable.fault_row6_list_for_inv[row] == '1024-ms':
                return round(self.calcvalue/1024*1000/3,2)
            elif share_variable.fault_row6_list_for_inv[row] == 'xxx':
                return ''
            else:
                return '?'

    '''
    函数名称：calc_receive_fault_data_in_bits(self,row,value,rec_or_inv,bit_or_bits)
    功能描述：故障点数据算法函数(bit or bits的情况)
    参数意义：row：行。value：值。rec_or_inv：整流or逆变
    函数调用：zfill：百度
    ''' 
    def calc_receive_fault_data_in_bits(self,row,value,rec_or_inv,bit_or_bits):
        '''
        bit代表cfg第四个数split('-')拆分成数组,第一个元素为低位，第二个为高位
        for循环用于长度小于16前面补0
        receive_data_value16转10转2后的值是否与cfg第4个值相等，相等则'Y'，否则空
        bitvalue 为接收到的需要用bit或bits来处理的value
        '''
        self.bitvalue = value
        self.bit_or_bits = bit_or_bits                 
        receive_data_value_bin = bin(int(self.bitvalue,16)).lstrip('0b').zfill(16)[::-1]
        if self.bit_or_bits == 'bits' and rec_or_inv == 'Rec':
            bit = share_variable.fault_row3_list_for_rec[row].split('-')
            #if row == 20:
           #    print('20:bits',bit)
            #    print('20:self.bitvalue',self.bitvalue)
            #    print('20:receive_data_value_bin',receive_data_value_bin)
           #     print('20:int(receive_data_value_bin[int(bit[0]):int(bit[1])+1])',int(receive_data_value_bin[int(bit[0]):int(bit[1])+1]))
           #     print('20:int(share_variable.fault_row4_list_for_rec[row])',int(share_variable.fault_row4_list_for_rec[row]))
            if int(receive_data_value_bin[int(bit[0]):int(bit[1])+1]) == int(share_variable.fault_row4_list_for_rec[row][::-1]):
                return 'Y'
            else:
                return ''
        elif self.bit_or_bits == 'bits' and rec_or_inv == 'Inv':
            bit = share_variable.fault_row3_list_for_inv[row].split('-')
            if int(receive_data_value_bin[int(bit[0]):int(bit[1])+1]) == int(share_variable.fault_row4_list_for_inv[row][::-1]):
                return 'Y'
            else:
                return ''
        elif self.bit_or_bits == 'bit' and rec_or_inv == 'Rec':
            bit = share_variable.fault_row3_list_for_rec[row].split('-')
            if int(receive_data_value_bin[int(bit[0])]) == int(share_variable.fault_row4_list_for_rec[row]):
                return 'Y'
            else:
                return ''
        elif self.bit_or_bits == 'bit' and rec_or_inv == 'Inv':
            bit = share_variable.fault_row3_list_for_inv[row].split('-')
            if int(receive_data_value_bin[int(bit[0])]) == int(share_variable.fault_row4_list_for_inv[row]):
                return 'Y'
            else:
                return ''
        else:
            return '??'
        
'''
-------------------------------------------------------------------------------
通信类函数定义
-------------------------------------------------------------------------------
'''
#函数功能：split函数各位，并返回需求位。
#protocol_str:可选字符串
#protocol_option可选参数：VER版本，ADR设备，CID1，CID2，DATA_NUM数据个数。
#函数功能，拆分协议响应，返回所选option的值

'''
函数名称：data_split(protocol_str,protocol_option)
功能描述：分割接收到的协议字符串
参数意义：protocol_str：协议字符串。protocol_option：所要挑出的部分。
函数调用：zfill：百度
''' 
def data_split(protocol_str,protocol_option):
    protocol = ''
    protocol = protocol_str
    #起始位判断
    if protocol[0] =='~':
        #print("起始位为:%s"%protocol[0])
        pass
    else:
        print("起始位错误:",protocol[0])
        return 0

    protocol_Drop_startbit = protocol.split("~")[1]   #split掉“~”
    protocol_CID2_dict = {
                          '00':'状态正常',
                          '01':'VER错',
                          '02':'CHKSUM错',
                          '03':'LCHKSUM',
                          '04':'CID2无效',
                          '05':'命令格式错',
                          '06':'无效数据',
                          '80':'无效权限',
                          '81':'操作失败',
                          '82':'存储芯片故障'
                          }
    if protocol_option == 'VER':
        return protocol_Drop_startbit[:2]
    elif protocol_option == 'ADR':
        return protocol_Drop_startbit[2:4]
    elif protocol_option == 'CID1':
        return protocol_Drop_startbit[4:6]
    elif protocol_option == 'CID2':
        return protocol_Drop_startbit[6:8]
    elif protocol_option == 'LCHKSUM':
        return protocol_Drop_startbit[8]
    elif protocol_option == 'LENGTH':
        return protocol_Drop_startbit[9:12]
    elif protocol_option == 'CHKSUM':
        if len(protocol_Drop_startbit) == 16:
            return protocol_Drop_startbit[12:]
        else:
            return protocol_Drop_startbit[len(protocol_Drop_startbit)-4:len(protocol_Drop_startbit)]
    elif protocol_option == 'DATAFLAG' or  protocol_option == 'DATA_NUM_for_Sysdata':
        return protocol_Drop_startbit[12:14]
    elif protocol_option == 'DATA_INFO_for_switch' or protocol_option == 'DATA_INFO_for_Sysdata':
        return protocol_Drop_startbit[14:len(protocol_Drop_startbit)-4]
    elif protocol_option == 'DATA_NUM':
        return protocol_Drop_startbit[14:16]
    elif protocol_option == 'DATA_INFO':
        return protocol_Drop_startbit[16:len(protocol_Drop_startbit)-4]
    elif protocol_option == 'CID2_DICT':
        return protocol_CID2_dict

#数据验证函数，验证CID1和lchksum以及chksum是否正确，全部正确返回1，否则返回0
#command：命令
'''
函数名称：data_split(protocol_str,protocol_option)
功能描述：数据验证函数，验证CID1、lchksum、chksum是否正确
参数意义：command：命令字符串
函数调用：str_to_int_ten、get_chksum、data_reverse
''' 
def data_verify(command):
    protocol_Drop_startbit = command.split("~")[1]
    protocol_CID1 = data_split(command,'CID1')   #CID1
    protocol_lchksum = data_split(command,'LCHKSUM')   #LENGTH的lchksum
    protocol_chksum = data_split(command,'CHKSUM')
    ####################2A验证##########################
    if protocol_CID1 == '2A':
                pass
    else:
                print("CID1:2AH错误",protocol_CID1)
                return 0
    protocol_length1 = protocol_Drop_startbit[9]
    protocol_length2 = protocol_Drop_startbit[10]
    protocol_length3 = protocol_Drop_startbit[11]


    #-------------------------------------------------
    protocol_length1=str_to_int_ten(protocol_length1) 
    protocol_length2=str_to_int_ten(protocol_length2)  #字符A转换成对应16进制A再转成10进制的值2
    protocol_length3=str_to_int_ten(protocol_length3)
    protocol_length2_3_re =data_reverse((protocol_length1+protocol_length2+protocol_length3)%16,4)  #求和后摸16取余不加1
       
       
    ############lchksum验证###############
    protocol_lchksum = str_to_int_ten(protocol_lchksum)
    #print("protocol_lchksum减1:",protocol_lchksum-1)
    str_to_bin = bin(((protocol_lchksum-1)))           #10进制转2进制字符串
    protocol_lchksum_final = str_to_bin.split('0b')[1].zfill(4)                  #去掉0b
    if protocol_lchksum_final == protocol_length2_3_re:    #比较lchksum的值与后三位计算出来的值是否相等
        #print("LCHKSUM校验值正确")
        pass
    elif protocol_Drop_startbit[8]==protocol_Drop_startbit[9]==protocol_Drop_startbit[10]==protocol_Drop_startbit[11]=='0':
        #print("LCHKSUM校验值正确，info为0")   #如果length为0000
        pass
    elif ((protocol_Drop_startbit[10]+protocol_Drop_startbit[11])=='6A' and protocol_Drop_startbit[8]=='0') :
        #print("LCHKSUM校验值正确，LENID等于6A")    #6A时且lchksum = '0'时
        pass
    else:
        print("LCHKSUM校验值错误")
        return 0
    ############chksum验证###############
    get_chksum_1 = get_chksum(protocol_Drop_startbit[0:len(protocol_Drop_startbit)-4])
    if get_chksum_1 != protocol_chksum:
        #print("CHKSUM校验码错误")
        return 0

    return 1   

'''
函数名称：assemble_command(Device_VER,Device_ADR,body)
功能描述：命令组装函数，拼接命令各个部分，并根据前面的部分计算chksum组成完整命令
参数意义：Device_VER：设备版本号。Device_ADR：设备号。body：命令中间部分
函数调用：get_chksum
''' 
def assemble_command(Device_VER,Device_ADR,body):
            chksum = get_chksum(Device_VER+Device_ADR+body)
            massage = '%s%s%s%s%s%s'%('~',Device_VER,Device_ADR,body,chksum,'\r')
            return massage

            
#################轮询COM口函数#########################
#返回设备com号，通过发送指令来判断COM口是否有响应。
'''
函数名称：figure_out_available_com(command)
功能描述：查询可用串口函数
参数意义：command：尝试向串口发送的命令
函数调用：Serial():串口对象、list_ports.comports()：列出串口号列表。
'''
def figure_out_available_com(command):
    ser = serial.Serial()
    port_list = list(list_ports.comports())
    com_list = []
    for port in port_list:
        com_list.append(str(port).split(' ')[0])
    while 1:                                   #循环判断哪个com口时通的
            for com in com_list:

                ser.port = com
                ser.baudrate =9600
                try:                              #尝试开串口，监听异常
                    ser.open()                    
                    ser.write(command.encode())        #的写一串发送代码
                    time.sleep(1)                   #睡1秒
                    if ser.inWaiting()>0:           #如果串口有返回数据
                        return com                      #返回com号，结束
                    elif ser.inWaiting()== 0:       #如果串口无返回数据，继续循环
                                    print("%s未返回"%com)   #输出无返回
                                    ser.close()
                except(OSError,serial.SerialException):     #如果触发串口占用异常
                                    print("%s占用或串口不可用"%com)
'''
-------------------------------------------------------------------------------
UI类函数定义
-------------------------------------------------------------------------------
'''
object_cfg_tool = cfg_tool('ToolsDebugChs.cfg')
fault_cfg_tool = cfg_tool('EventChs.cfg')
#################通用label函数#########################
#window=label所在框架，name=label名称，text_1=label显示的文本,row_1=label所在行,column_1=label所在列
#width_1=label的宽度,relief_1=label 的风格（可选参数'sunken','groove',
#暂时用不上    

#dialogname表示修改值弹窗的名称，i表示cfg文件当中的行。

'''
类名称：Common_label_for_setting(object)
功能描述：通用标签设置类
参数意义：object：继承boject类
函数调用：无
'''            
      
class Common_label_for_setting(object):  #不可继承tk类，会出现多个空弹窗。
    '''
    通用标签类。
    common_label为普通标签类方法
    common_label_for_modify为带对话框属性的标签类方法，用于设置量。
    ''' 
    '''
    函数名称：__init__(self,window)
    功能描述：类初始化
    参数意义：window：所在框架
    函数调用： tkFont.Font：字体格式设置
    '''     
    def __init__(self,window):
        super().__init__()
        self.window = window
        self.ft = tkFont.Font(size = 10)
        #object_cfg_tool.Change_Value_In_CFG('Config_for_Sysdata','SYSData_List','temporary_variable',self.res,object_cfg_tool.Pick_Option_In_Section('SYSData_List',self.i,0))
        '''动态标签'''
    '''
    函数名称：common_label_strvar(self,text_1,row_1,column_1,width_1,relief_1)
    功能描述：动态显示标签设定函数
    参数意义：text_1：标签要显示的内容。row_1：行。column_1：列。width_1：宽度。relief_1：风格。
    函数调用： tkFont.Font：字体格式设置、grid：用于部署
    ''' 
    def common_label_strvar(self,text_1,row_1,column_1,width_1,relief_1):
        label = tk.Label(self.window,textvariable=text_1,relief = relief_1,width = width_1,height=1,anchor = 'w',bg = 'white',font = self.ft)
        label.grid(row=row_1,column=column_1,sticky = 'W'+'N')
        '''静态标签'''
    '''
    函数名称：common_label(self,text_1,row_1,column_1,width_1,relief_1)
    功能描述：静态显示标签设定函数
    参数意义：text_1：标签要显示的内容。row_1：行。column_1：列。width_1：宽度。relief_1：风格。
    函数调用： tkFont.Font：字体格式设置、grid：用于部署
    ''' 
    def common_label(self,text_1,row_1,column_1,width_1,relief_1):
        label = tk.Label(self.window,text=text_1,relief = relief_1,width = width_1,height=1,anchor = 'w',bg = 'white',font = self.ft)
        label.grid(row=row_1,column=column_1,sticky = 'W'+'N')

        #双击可设定值的label
    '''
    函数名称：common_label_for_modify(self,text_1,row_1,column_1,width_1,relief_1,dialogname,i,cfg_section)
    功能描述：点击可弹窗修改值的动态显示标签设定函数
    参数意义：text_1：标签要显示的内容。row_1：行。column_1：列。width_1：宽度。relief_1：风格。dialogname：修改值的名称。i：cfg中的第i行。cfg_section：所选的cfg的section
    函数调用： tkFont.Font：字体格式设置、grid：用于部署
    ''' 
    def common_label_for_modify(self,text_1,row_1,column_1,width_1,relief_1,dialogname,i,cfg_section):
        def print_float(self):
            self.res = simpledialog.askfloat(dialogname,"修改值")
            '''根据cfg中第三个数字作为标志位来进行判断输入的值是否符合要求
               如果第三个数字为0，则判断输入值是否在列表中存在。（列表从cfg同行第4个元素中取）
               如果第三个数字为1，则判断输入值是否在范围内。（范围在cfg同行第4个元素中取）
            '''
            #######判断输入值是否符合要求########
            #########object_cfg_tool.Pick_Option_In_Section('SYSData_List',i,2) == 0
            #########此类情况是在特定值有效时可用#################
            #print('Pick_Option_In_Section(cfg_section,i,2)',object_cfg_tool.Pick_Option_In_Section(cfg_section,i,2))
            if object_cfg_tool.Pick_Option_In_Section(cfg_section,i,2) == '0':
                #把option[3]转换为列表，再把每个元素转换成float类型
                list_for_standard_value = list(map(lambda x:float(x),object_cfg_tool.Pick_Option_In_Section(cfg_section,i,3).split('、')))
                #print('list_for_standard_value',list_for_standard_value)
                #判断输入值与有效的值是否有交集，即判断输入值是否在
                if self.res in set(list_for_standard_value):
                    pass
                else:
                    self.res = None
                    tk.messagebox.showerror("错误","输入数据有误，不在范围内")
            #########object_cfg_tool.Pick_Option_In_Section('SYSData_List',i,2) == 1
            #########此类情况是在范围内有效可用#################        
            elif object_cfg_tool.Pick_Option_In_Section(cfg_section,i,2) == '1':
                print('object_cfg_tool.Pick_Option_In_Section(cfg_section,i,3)',object_cfg_tool.Pick_Option_In_Section(cfg_section,i,3))
                if float(object_cfg_tool.Pick_Option_In_Section(cfg_section,i,3))<=self.res<=float(object_cfg_tool.Pick_Option_In_Section(cfg_section,i,4)):
                    pass
                else:
                    self.res = None
                    tk.messagebox.showerror("错误","输入数据有误，不在范围内")
            ##########如果ser不是None，则认为值没问题，把值转换为float后写入CFG文件中##########
            if self.res != None:
                '''系统cfg对应命令'''
                share_variable.polling_status = '1'#轮询状态改变
                if cfg_section == 'SYSData_List': 
                    share_variable.res = float_2_hex_2_com(self.res)
                    share_variable.Sysdata_0 = object_cfg_tool.Pick_Option_In_Section(cfg_section,i,0)
                elif cfg_section == 'RECData_List':
                    share_variable.res_rec = float_2_hex_2_com(self.res)
                    share_variable.Recdata_0 = object_cfg_tool.Pick_Option_In_Section(cfg_section,i,0)
                elif cfg_section == 'INVData_List':
                    share_variable.res_inv = float_2_hex_2_com(self.res)
                    share_variable.Invdata_0 = object_cfg_tool.Pick_Option_In_Section(cfg_section,i,0)
                elif cfg_section == 'BattData_List':
                    share_variable.res_bat = float_2_hex_2_com(self.res)
                    share_variable.Batdata_0 = object_cfg_tool.Pick_Option_In_Section(cfg_section,i,0)
            else:
                pass
       #return res
        name = tk.Label(self.window,textvariable=text_1,relief = relief_1,width = width_1,height=1,anchor = 'w',bg = 'white',font = self.ft)
        name.bind('<Double-Button-1>',print_float)

        name.grid(row=row_1,column=column_1,sticky = 'W'+'N')        
        #输入的设定值的合理性判断函数。
    #def entry_verify(self):

'''
类名称：Setting_window()
功能描述：通用设置量窗口设置类
参数意义：无
函数调用：无
''' 
class Setting_window():
    '''
    函数名称：__init__(self,name_num,name_list,name_for_setting)
    功能描述：设置窗口初始化
    参数意义：name_num：cfg中对应的section下的数量值。name_list：对应的section的名称。name_for_setting：设置的状态
    函数调用：Common_label_for_setting、common_label、Pick_Option_In_Section
    '''     
    def __init__(self,name_num,name_list,name_for_setting):
        share_variable.setting_window_name = name_for_setting
        share_variable.polling_status = '2'
        self.name_num = name_num
        self.name_list = name_list
        self.setting_win = tk.Toplevel()
        self.geometry = ('600x800')
        self.common_label_for_setting = Common_label_for_setting(self.setting_win)
        self.common_label_for_setting.common_label('参数名称',0,0,23,'raised')
        self.common_label_for_setting.common_label('当前值',0,1,10,'raised')
        self.common_label_for_setting.common_label('备注信息',0,2,75,'raised')
        self.dict = {}
        self.sql_sys_setting_namelist = []
        self.sql_rec_setting_namelist = []
        self.sql_inv_setting_namelist = []
        self.sql_bat_setting_namelist = []
        self.num = int(object_cfg_tool.Pick_Option_In_Section(name_num,0,0))
        for i in range(self.num):
            
            #参数名称加载
            self.Sysdata_name = object_cfg_tool.Pick_Option_In_Section(name_list,i,1)
            self.common_label_for_setting.common_label(self.Sysdata_name,i+1,0,23,'groove')
            #备注加载
            self.Sysdata_remark = object_cfg_tool.Pick_Option_In_Section(name_list,i,5)      ###！注意这个5可能会变
            self.common_label_for_setting.common_label(self.Sysdata_remark,i+1,2,75,'groove')
            #当前值设置为stringvar并加载
            self.dict['%s%s'%('variable',str(i))] = tk.StringVar()
            self.common_label_for_setting.common_label_for_modify(self.dict['%s%s'%('variable',str(i))],i+1,1,10,'groove',object_cfg_tool.Pick_Option_In_Section(self.name_list,i,1),i,self.name_list)
            #id、参数、备注写入append到临时数组
            if share_variable.setting_window_name == 'sys':
                self.sql_sys_setting_namelist.append([i,self.Sysdata_name,self.Sysdata_remark])
            elif share_variable.setting_window_name == 'rec':
                self.sql_rec_setting_namelist.append([i,self.Sysdata_name,self.Sysdata_remark])
            elif share_variable.setting_window_name == 'inv':
                self.sql_inv_setting_namelist.append([i,self.Sysdata_name,self.Sysdata_remark])
            elif share_variable.setting_window_name == 'bat':
                self.sql_bat_setting_namelist.append([i,self.Sysdata_name,self.Sysdata_remark])
        #id、参数、备注写入sql
        if share_variable.setting_window_name == 'sys':
            sql.config_sys_setting_init(self.sql_sys_setting_namelist)
        elif share_variable.setting_window_name == 'rec':
            sql.config_rec_setting_init(self.sql_rec_setting_namelist)
        elif share_variable.setting_window_name == 'inv':
            sql.config_inv_setting_init(self.sql_inv_setting_namelist)
        elif share_variable.setting_window_name == 'bat':
            sql.config_bat_setting_init(self.sql_bat_setting_namelist)
    '''
    函数名称：reflash_data(self,getting_value_title,got_value_title,receive_protocol_str)
    功能描述：设置量数值刷新函数，配合多线程
    参数意义：getting_value_title：设置量窗口状态（获取数据中）。got_value_title：（已获取数据）。receive_protocol_str：获取的协议字符串
    函数调用：protocol_sysdata.analysis_protocol
    '''                 
    def reflash_data(self,getting_value_title,got_value_title,receive_protocol_str):
        self.sql_sys_setting_valuelist = []
        self.sql_rec_setting_valuelist = []
        self.sql_inv_setting_valuelist = []
        self.sql_bat_setting_valuelist = []
        self.receive_protocol_str = receive_protocol_str
        if self.receive_protocol_str == '':
            self.setting_win.title(getting_value_title)
            for i in range(self.num):
               #stringvar赋值
               self.dict['%s%s'%('variable',str(i))].set('\\')
               #值写入临时数组
               if share_variable.setting_window_name == 'sys':
                   self.sql_sys_setting_valuelist.append([i,'\\'])
               elif share_variable.setting_window_name == 'rec':
                   self.sql_rec_setting_valuelist.append([i,'\\'])
               elif share_variable.setting_window_name == 'inv':
                   self.sql_inv_setting_valuelist.append([i,'\\'])
               elif share_variable.setting_window_name == 'bat':
                   self.sql_bat_setting_valuelist.append([i,'\\'])
               
        else:
            self.setting_win.title(got_value_title)
            self.sysdata_return_list = protocol_sysdata.analysis_protocol(self.receive_protocol_str)
            #print("self.sysdata_return_list",self.sysdata_return_list)
            for i in range(len(self.sysdata_return_list)-2):
                self.dict['%s%s'%('variable',str(i))].set(self.sysdata_return_list[i])
                if share_variable.setting_window_name == 'sys':
                   self.sql_sys_setting_valuelist.append([i,self.sysdata_return_list[i]])
                elif share_variable.setting_window_name == 'rec':
                   self.sql_rec_setting_valuelist.append([i,self.sysdata_return_list[i]])
                elif share_variable.setting_window_name == 'inv':
                   self.sql_inv_setting_valuelist.append([i,self.sysdata_return_list[i]])
                elif share_variable.setting_window_name == 'bat':
                   self.sql_bat_setting_valuelist.append([i,self.sysdata_return_list[i]])
                   
        if share_variable.setting_window_name == 'sys':
            sql.config_sys_setting(self.sql_sys_setting_valuelist)
        elif share_variable.setting_window_name == 'rec':
            sql.config_rec_setting(self.sql_rec_setting_valuelist)
        elif share_variable.setting_window_name == 'inv':
            sql.config_inv_setting(self.sql_inv_setting_valuelist)
        elif share_variable.setting_window_name == 'bat':
            sql.config_bat_setting(self.sql_bat_setting_valuelist)
        
'''
类名称：Setting_the_password()
功能描述：负责密码的窗口搭建以及密码接收发送。
参数意义：无
函数调用：无
'''  
class Setting_the_password():
    '''
    函数名称： __init__(self)
    功能描述：密码窗口初始化
    参数意义：无
    函数调用：tk.Toplevel()：弹窗。tk.Button：按钮
    '''  
    def __init__(self):
        self.win_for_password = tk.Toplevel()
        self.win_for_password.title("输入密码(位数写死为6位,不是六位会导致chksum验证出错。)")
        self.password = tk.StringVar()
        self.label = tk.Label(self.win_for_password,text = '请输入6位密码:',width = 15)
        self.label.grid(row = 0,column = 0)
        self.button_setting = tk.Button(self.win_for_password,text = '设置',command = self.password_modify)
        self.button_setting.grid(row = 0,column = 1)
        self.entry = tk.Entry(self.win_for_password,textvariable = self.password,width = 20,show = '*')
        self.entry.grid(row = 1,column = 0)
        self.button_cancel = tk.Button(self.win_for_password,text = '取消',command = self.destory_win)
        self.button_cancel.grid(row = 1,column = 1)
        
    '''
    函数名称：destory_win(self)
    功能描述：关闭窗口触发函数
    参数意义：无
    函数调用：无
    ''' 
    def destory_win(self):
        self.win_for_password.destroy()
    '''
    函数名称：password_modify(self)
    功能描述：将用户输入的密码传值给share_vairable临时数据库等待调用。并改变轮询status
    参数意义：无
    函数调用：无
    '''         
    def password_modify(self):
        self.receive_password = ''.join(list(map(lambda x:hex(ord(x)).lstrip('0x'),list(self.password.get()))))   
        share_variable.receive_password = self.receive_password
        share_variable.polling_status = '1'
        #tk.messagebox.showinfo('密码接收成功','请等待,密码发送中')
        self.destory_win()

'''
类名称：Switching_Value_Window()
功能描述：开关量窗口类
参数意义：无
函数调用：无
''' 
class Switching_Value_Window():
    '''
    函数名称：__init__(self,name_num,name_list)
    功能描述：开关量窗口初始化
    参数意义：name_num：cfg中对应的section下的数量值。name_list：对应的section的名称。
    函数调用：Common_label_for_setting、common_label、switch_win.protocol：窗口关闭时触发函数、sql.config_switching_value_init()
    '''     
    def __init__(self,name_num,name_list):
        share_variable.switching_window_name = 'switch'
        self.switch_win = tk.Toplevel()
        self.name_num = name_num
        self.num = int(object_cfg_tool.Pick_Option_In_Section(self.name_num,0,0))
        self.name_list = name_list
        self.switch_win.title('开关量状态-正在获取数据')
        self.common_label_win = Common_label_for_setting(self.switch_win)
        self.common_label_win.common_label('开关量名称',0,0,20,'raised')
        self.common_label_win.common_label('开关量状态',0,1,20,'raised')
        self.switch_win.protocol('WM_DELETE_WINDOW',self.close_win)   #关闭窗口时触发
        self.dict = {}
        self.sql_switching_namelist = []
        
        '''循环读取cfg中开关量名称并加载到后台，同时写入数据库'''
        for i in range(self.num):
            #开关量名称加载
            self.Switching_Value_name = object_cfg_tool.Pick_Option_In_Section(self.name_list,i,1)
            self.common_label_win.common_label(self.Switching_Value_name,i+1,0,20,'groove')
            #开关量值stringvar并加载
            self.dict['%s%s'%('variable',str(i))] = tk.StringVar()
            self.common_label_win.common_label_strvar(self.dict['%s%s'%('variable',str(i))],i+1,1,20,'groove')
            #存入sql
            self.sql_switching_namelist.append([self.Switching_Value_name,i])
        sql.config_switching_value_init(self.sql_switching_namelist)
        '''循环读取开关量数据并加载到后台'''
    
    '''
    函数名称：reflash_switching_value(self)
    功能描述：开关量刷新函数，配合多线程使用
    参数意义：无
    函数调用：protocol_switch.analysis_protocol、Pick_Option_In_Section
    '''            
    def reflash_switching_value(self):
        self.sql_switching_valuelist = []
        if share_variable.receive_switch_data_str == '':
            self.switch_win.title('开关量状态-正在获取数据')
            for i in range(self.num):
               self.dict['%s%s'%('variable',str(i))].set('\\')
               self.sql_switching_valuelist.append(['\\',object_cfg_tool.Pick_Option_In_Section(self.name_list,i,1)])
        else:
            self.switch_win.title('开关量状态-已获取数据')
            self.switching_value_return_list = protocol_switch.analysis_protocol(share_variable.receive_switch_data_str)
            for switching_value in self.switching_value_return_list:
               self.dict['%s%s'%('variable',str(self.switching_value_return_list.index(switching_value)))].set(switching_value)
               self.sql_switching_valuelist.append([switching_value,self.switching_value_return_list.index(switching_value)])
        sql.config_switching_value(self.sql_switching_valuelist)
    '''
    函数名称：close_win(self)
    功能描述：窗口关闭时switching_window_name清空
    参数意义：无
    函数调用：无
    ''' 
    def close_win(self):
        share_variable.switching_window_name = ''
        self.switch_win.destroy()

'''
类名称：Warning_Value_Window()
功能描述：告警量窗口类
参数意义：无
函数调用：无
'''
class Warning_Value_Window():
    '''
函数名称：__init__(self)
    功能描述：告警量窗口类初始化
    参数意义：无
    函数调用：Common_label_for_setting、common_label
    '''
    def __init__(self):
        share_variable.warning_window_name = 'warning'
        self.warning_win = tk.Toplevel()
        self.warning_win.title('告警量状态-正在获取数据')
        self.common_label_win_top = Common_label_for_setting(self.warning_win)
        self.list_for_menu = ['告警量part1名称','告警量part1状态','告警量part2名称','告警量part2状态',
                    '告警量part3名称','告警量part3状态','告警量part4名称','告警量part4状态',]
        self.dict = {}  #用于动态变量批量处理(批量赋值Stringvar)
        self.sql_warning_namelist = []
        for list_part in self.list_for_menu:
            self.common_label_win_top.common_label(list_part,0,self.list_for_menu.index(list_part),20,'raised')
        
        self.warning_value_name_sections = ['Warning_Value_list_part1','Warning_Value_list_part2',
                                  'Warning_Value_list_part3','Warning_Value_list_part4'] 
        self.range_length = range(17)
        for i in range(4):
            for j in self.range_length:
                #告警量名称加载
                self.warning_Value_name = object_cfg_tool.Pick_Option_In_Section(self.warning_value_name_sections[i],j,1)
                self.common_label_win_top.common_label(self.warning_Value_name,j+1,2*i,20,'groove')
                #告警量值加载
                self.dict['%s%s%s'%('variable',str(i),str(j))] = tk.StringVar()
                self.common_label_win_top.common_label_strvar(self.dict['%s%s%s'%('variable',str(i),str(j))],j+1,2*i+1,20,'groove')
                
                self.sql_warning_namelist.append([self.warning_Value_name,j+i*17])
        sql.config_warning_value_init(self.sql_warning_namelist)                 
        self.warning_win.protocol('WM_DELETE_WINDOW',self.close_win)
    '''
    函数名称：reflash_Warning_value(self)
    功能描述：告警量刷新窗口函数，用于刷新数据，配合多线程使用
    参数意义：无
    函数调用：protocol_warning.analysis_protocol、 sql.config_warning_value
    '''        
    def reflash_Warning_value(self):
        self.sql_warning_valuelist = []
        if share_variable.receive_warning_data_str == '':
            self.warning_win.title('告警量状态-正在获取数据')
            for i in range(4):                     #外部循环section
                for j in self.range_length:                #内部循环section的option并赋值
                    self.dict['%s%s%s'%('variable',str(i),str(j))].set('\\')
        else:
            self.warning_win.title('告警量状态-已获取数据')
            self.warning_value_return_list = protocol_warning.analysis_protocol(share_variable.receive_warning_data_str)
            self.warning_value_return_part1 = self.warning_value_return_list[:17]
            self.warning_value_return_part2 = self.warning_value_return_list[17:34]
            self.warning_value_return_part3 = self.warning_value_return_list[34:51]
            self.warning_value_return_part4 = self.warning_value_return_list[51:]
            self.warning_value_return_part_list = [self.warning_value_return_part1,self.warning_value_return_part2,
                                             self.warning_value_return_part3,self.warning_value_return_part4]
            
            for i in range(4):                     #外部循环section
               for j in self.range_length:                #内部循环section的option并赋值
                   self.dict['%s%s%s'%('variable',str(i),str(j))].set(self.warning_value_return_part_list[i][j])
                   self.sql_warning_valuelist.append([self.warning_value_return_part_list[i][j],j+i*17])
            sql.config_warning_value(self.sql_warning_valuelist)
    def close_win(self):
        share_variable.warning_window_name = ''
        self.warning_win.destroy()

'''
类名称：main_menu()
功能描述：主菜单加载函数
参数意义：无
函数调用：无
'''
class main_menu():
    '''
    函数名称：__init__(self,parent)
    功能描述：菜单初始化
    参数意义：parent：所在框架
    函数调用：tk.Menu
    '''    
    def __init__(self,parent):
        self.parent = parent
        self.menu_main_button = tk.Menu(self.parent)
        self.parent.config(menu = self.menu_main_button)
    '''
    函数名称：set_the_menu(self,label_name,menulist,commandlist)
    功能描述：设定每个菜单下的标签以及绑定的函数
    参数意义：label_name：菜单名。menulist：标签名列表。commandlist：每个标签绑定的命令名列表
    函数调用：tk.Menu、add_cascade、add_command
    ''' 
    def set_the_menu(self,label_name,menulist,commandlist):
        self.label_name = label_name
        self.menulist = menulist
        self.commandlist = commandlist
        self.weight_name = tk.Menu(self.menu_main_button,tearoff = 0)
        self.menu_main_button.add_cascade(label = self.label_name,menu = self.weight_name)
        self.length = len(self.menulist)
        for i in range(self.length):
            self.weight_name.add_command(label = self.menulist[i],command = self.commandlist[i])
         

    
#通讯异常状态下所有数据全部置0
'''
函数名称：set_analog_quantity_to_zero(frame_2,frame_3)
功能描述：模拟量数据全部清零（在通信异常状态下回触发）
参数意义：frame_2：框架2。frame_3：框架3
函数调用：Common_label_for_setting、common_label、Pick_Section_number
''' 
def set_analog_quantity_to_zero(frame_2,frame_3):
    Common_label_frame2 = Common_label_for_setting(frame_2)
    Common_label_frame3 = Common_label_for_setting(frame_3)
    for i in range(0,object_cfg_tool.Pick_Section_number('Analog1_Num')):
            if i == 8 or i == 16 or i == 20:
                Common_label_frame2.common_label('',i+1,2,10,'groove')
            elif i == 0 or i == 1 or i == 21 or i == 22:
                Common_label_frame2.common_label(0,i+1,2,10,'groove')
                Common_label_frame2.common_label(0,i+1,3,10,'groove')
                Common_label_frame2.common_label(0,i+1,4,10,'groove')
            else:
                Common_label_frame2.common_label(0,i+1,2,10,'groove')
        #Analog2_data中的数据置0        
    for i in range(0,object_cfg_tool.Pick_Section_number('Analog2_Num')):
            if i == 6 or i == 13:
                Common_label_frame3.common_label('',i+1,2,10,'groove')
            else:
                Common_label_frame3.common_label(0,i+1,2,10,'groove')
                
'''
类名称：set_analog_quantity()
功能描述：模拟量名称及数据加载到面板
参数意义：无
函数调用：无
''' 
class set_analog_quantity():
    '''
    函数名称：set_analog_quantity()
    功能描述：模拟量名称及数据加载到面板
    参数意义：无
    函数调用：Common_label_for_setting、common_label、sql.config_analog_quantity_init
    ''' 
    def __init__(self,frame2,frame3):
        self.frame2 = frame2
        self.frame3 = frame3
        self.dict = {}
        ###协议中没有的cfg中有的，初始化为0
        disable_label_in_frame2 = Common_label_for_setting(self.frame2)
        disable_label_in_frame3 = Common_label_for_setting(self.frame3)
        disable_label_in_frame2.common_label('',9,2,10,'groove') #空
        disable_label_in_frame2.common_label('',17,2,10,'groove')#空
        disable_label_in_frame2.common_label('',21,2,10,'groove')#空
        disable_label_in_frame3.common_label(0.0,12,2,10,'groove')#监控变量1
        disable_label_in_frame3.common_label(0.0,13,2,10,'groove')#监控变量2
        disable_label_in_frame3.common_label('',7,2,10,'groove')#空
        disable_label_in_frame3.common_label('',14,2,10,'groove')#空

        #字典用于对应位置
        #key:对应的值的名称 value=[框架，行，列]
        self.common_label_dict_41 = {
                             '输入线电压(V)':[self.frame2,1,2],
                             'B相输入线电压(V)':[self.frame2,1,3],
                             'C相输入线电压(V)':[self.frame2,1,4],
                             '输出相电压(V)':[self.frame2,8,2],
                             '输出电流(A)':[self.frame2,10,2],
                             '输出频率(Hz)':[self.frame2,16,2],
                             '电池电压(V)':[self.frame3,1,2],
                             '电池温度(℃)':[self.frame3,3,2],
                             '电池容量(%)':[self.frame3,5,2],
                                   }
        self.common_label_dict_90 = {
                             '输入滤波器电流(A)':[self.frame2,22,2],
                             'B相输入滤波器电流(A)':[self.frame2,22,3],
                             'C相输入滤波器电流(A)':[self.frame2,22,4],
                             '6p整流器相电流(A)':[self.frame2,23,2],
                             'B相6p整流器相电流(A)':[self.frame2,23,3],
                             'C相6p整流器相电流(A)':[self.frame2,23,4],
                             '12p整流器相电流(A)':[self.frame2,24,2],
                             'B相12p整流器相电流(A)':[self.frame2,24,3],
                             'C相12p整流器相电流(A)':[self.frame2,24,4],
                             '逆变相电压(V)':[self.frame2,25,2],
                             '逆变相电流(A)':[self.frame2,26,2],
                             '电感电流(A)':[self.frame2,27,2],
                             '输出电容电流(A)':[self.frame2,28,2],
                             '输出视在功率(KVA)':[self.frame2,29,2],
                             '整流调试变量1':[self.frame3,8,2],
                             '整流调试变量2':[self.frame3,9,2],
                             '逆变调试变量3':[self.frame3,10,2],
                             '逆变调试变量4':[self.frame3,11,2],
                             '逆变母线电压(V)':[self.frame3,16,2],
                             '整流母线电压(V)':[self.frame3,17,2],
                             '母线半压(V)':[self.frame3,18,2],
                             'UPS序列号':[self.frame3,22,2]
                                    }
        self.common_label_dict_81 = {
                             '输入相电流(A)':[self.frame2,2,2],
                             'B相输入相电流(A)':[self.frame2,2,3],
                             'C相输入相电流(A)':[self.frame2,2,4],
                             '输入频率(Hz)':[self.frame2,3,2],
                             '旁路线电压(V)':[self.frame2,4,2],
                             '旁路相电压(V)':[self.frame2,5,2],
                             '旁路频率(Hz)':[self.frame2,6,2],
                             '输出线电压(V)':[self.frame2,7,2],
                             '输出有功功率(KW)':[self.frame2,11,2],
                             '输出功率因数':[self.frame2,13,2],
                             '负载(%)':[self.frame2,14,2],
                             '峰值比':[self.frame2,15,2],
                                    }
        self.common_label_dict_82 = {
                            '系统输出有功功率(KW)':[self.frame2,18,2],
                            '系统输出无功功率(KVAR)':[self.frame2,19,2],
                            '系统输出视在功率(KVA)':[self.frame2,20,2],
                            '电池电流(A)':[self.frame3,2,2],
                            '后备时间(Min)':[self.frame3,4,2]
                                     }
        self.common_label_dict_83 = {
                            '输出无功功率(KVAR)':[self.frame2,12,2],
                            '电池老化系数':[self.frame3,6,2],
                            '总输入功率因数':[self.frame3,15,2],
                            '环境温度(℃)':[self.frame3,19,2],
                            'IGBT模块温度(℃)':[self.frame3,20,2],
                            '充电电压(V)':[self.frame3,21,2]
                                     }
        self.common_label_dict_list = [self.common_label_dict_41,
            self.common_label_dict_90,self.common_label_dict_81,
            self.common_label_dict_82,self.common_label_dict_83]
        for i in range(5):
            #定义sql取行列值的列表。
            sql_init_data = []
            for j in range(len(self.common_label_dict_list[i])):
                #第i个字典，第j个字典元素
                self.label_key = list(self.common_label_dict_list[i].keys())[j]
                self.label_value = self.common_label_dict_list[i].get(self.label_key)
                self.dict['%s%s%s'%('variable',str(i),str(j))] = tk.StringVar()
                Common_label_quantity = Common_label_for_setting(self.label_value[0])
                Common_label_quantity.common_label_strvar(self.dict['%s%s%s'%('variable',str(i),str(j))],self.label_value[1],self.label_value[2],10,'groove')
                if self.label_value[0] == self.frame2:
                    sql_init_data.append([self.label_key,self.label_value[1],self.label_value[2],2])
                else:
                    sql_init_data.append([self.label_key,self.label_value[1],self.label_value[2],3])
            sql.config_analog_quantity_init(sql_init_data)
    '''
    函数名称：reflash_analog_quantity(self,common_label_dict)
    功能描述：模拟量刷新函数，配合多线程使用
    参数意义：common_label_dict：从queue队列获取的模拟量值列表
    函数调用： sql.config_analog_quantity
    ''' 
    def reflash_analog_quantity(self,common_label_dict):
        sql_data = []
        if len(common_label_dict) == 9:
            for j in range(9):
                #第一行将接收到的模拟量值set给StringVar
                #第二行sql_data.append[模拟量值，主键]
                #sql_data存入sql
                self.dict['%s%s%s'%('variable','0',str(j))].set(common_label_dict[j])
                sql_data.append([common_label_dict[j],list(self.common_label_dict_list[0].keys())[j]])
            sql.config_analog_quantity(sql_data)
        elif len(common_label_dict) == 22:
            for j in range(22):
                self.dict['%s%s%s'%('variable','1',str(j))].set(common_label_dict[j])
                sql_data.append([common_label_dict[j],list(self.common_label_dict_list[1].keys())[j]])
            sql.config_analog_quantity(sql_data)
        elif len(common_label_dict) == 12:
            for j in range(12):
                self.dict['%s%s%s'%('variable','2',str(j))].set(common_label_dict[j])
                sql_data.append([common_label_dict[j],list(self.common_label_dict_list[2].keys())[j]])
            sql.config_analog_quantity(sql_data)
        elif len(common_label_dict) == 5:
            for j in range(5):
                self.dict['%s%s%s'%('variable','3',str(j))].set(common_label_dict[j])
                sql_data.append([common_label_dict[j],list(self.common_label_dict_list[3].keys())[j]])
            sql.config_analog_quantity(sql_data)
        elif len(common_label_dict) == 6:
            for j in range(6):
                self.dict['%s%s%s'%('variable','4',str(j))].set(common_label_dict[j])
                sql_data.append([common_label_dict[j],list(self.common_label_dict_list[4].keys())[j]])
            sql.config_analog_quantity(sql_data)
'''
函数名称：request_for_history_event()
功能描述：更改轮询状态至状态3，使主线程开始读取历史记录数据
参数意义：无
函数调用： tk.messagebox.showinfo
''' 
def request_for_history_event():
    share_variable.polling_status = '3'
    tk.messagebox.showinfo('历史数据','数据正在导出中')
'''
函数名称：request_for_fault_event()
功能描述：更改轮询状态至状态4，使主线程开始读取故障点记录数据
参数意义：无
函数调用：无
'''    
def request_for_fault_event():
    share_variable.polling_status = '4'
    share_variable.fault_status = 'rec1'
    '''取cfg数量到临时变量，后面写入cfg仍有用'''
    share_variable.fault_num_rec = int(fault_cfg_tool.Pick_Option_In_Section('Rec_Num',0,0))
    share_variable.fault_num_inv = int(fault_cfg_tool.Pick_Option_In_Section('Inv_Num',0,0))
    '''初始化cfg中的name到临时数组变量中'''
    for i in range(share_variable.fault_num_rec):
        '''
        fault_cfg_list_i：cfg中第i行的内容组成的列表
        row0~6见cfg行
        '''
        fault_cfg_list_i = fault_cfg_tool.Pick_Option('Rec',i)
        #print('fault_cfg_list_i',fault_cfg_list_i)
        share_variable.fault_row0_list_for_rec.append(fault_cfg_list_i[0])    
        share_variable.fault_row2_list_for_rec.append(fault_cfg_list_i[2])
        share_variable.fault_row3_list_for_rec.append(fault_cfg_list_i[3])
        share_variable.fault_row4_list_for_rec.append(fault_cfg_list_i[4])
        share_variable.fault_namelist_for_rec.append(fault_cfg_list_i[5])
        share_variable.fault_row6_list_for_rec.append(fault_cfg_list_i[6])
          
    for i in range(share_variable.fault_num_inv):
        fault_cfg_list_i = fault_cfg_tool.Pick_Option('Inv',i)
        #print('fault_cfg_list_i',fault_cfg_list_i)
        share_variable.fault_row0_list_for_inv.append(fault_cfg_list_i[0])    
        share_variable.fault_row2_list_for_inv.append(fault_cfg_list_i[2])
        share_variable.fault_row3_list_for_inv.append(fault_cfg_list_i[3])
        share_variable.fault_row4_list_for_inv.append(fault_cfg_list_i[4])
        share_variable.fault_namelist_for_inv.append(fault_cfg_list_i[5])
        share_variable.fault_row6_list_for_inv.append(fault_cfg_list_i[6])
        
    time.sleep(0.5)
    tk.messagebox.showinfo('故障点数据','数据正在导出中')
#预留，用于后续控制扩展

def donothing():

   filewin = tk.Toplevel()
   button = tk.Button(filewin, text="Do nothing button",relief = 'groove')
   button.pack()

#彩蛋
def Easter_egg():
    def egg():
         tk.messagebox.showinfo('恭喜你发现了彩蛋','软件的作者是个实习生,邮箱xyq152438@foxmail.com.')
    egg_win = tk.Toplevel()
    button = tk.Button(egg_win, text="V000.00.01.00",relief = 'groove',command = egg)
    button.pack()


'''
-------------------------------------------------------------------------------
函数处理类函数定义
-------------------------------------------------------------------------------
'''
##################单精度float值转16进制计算函数######################
#例：输入2，输出00000040(hex:40000000)
'''
函数名称：float_2_hex_2_com(s)
功能描述：浮点数转单精度float值
参数意义：s：浮点数
函数调用：ctypes：处理C语言类型数据的包，可以调用c封装成dll的函数。这东西很有用。
''' 
def float_2_hex_2_com(s):
    if s == 0 or s == 0.0:
        return '00000000'
    fp = ctypes.pointer(ctypes.c_float(s))
    cp = ctypes.cast(fp,ctypes.POINTER(ctypes.c_longlong))
    hex_value = str(hex(cp.contents.value)).lstrip('0x').upper()
    hex_value = hex_value[::-1]                 #--------
    hex_new_value = ''
    for i in range(0,7,2):            #把串口显示值转换为float值
        hex_new_value+=hex_value[i+1]
        hex_new_value+=hex_value[i]
    return hex_new_value

#################数值取反函数#########################
#data为十进制数字，bit为2进制位数。
'''
函数名称：data_reverse(data,bit)
功能描述：数值取反，10进制转2进制后取反
参数意义：data：传入的十进制数据。bit：2进制位数
函数调用：无
''' 
def data_reverse(data,bit):                                     #
        clear_bin_list = list(bin(data).lstrip('0b').zfill(bit))      #10进制转2进制字符串,把字符串转换成数组
        clear_bin_str =''.join(list(map(lambda x:str(abs(int(x)-1)),clear_bin_list)))
        return clear_bin_str

##############单个字符转十进制数值函数###############
#字符串A转换成对应数字10进制,即'A'→10   
'''
函数名称：str_to_int_ten(data)
功能描述：16进制转10进制
参数意义：data：传入的16进制数据
函数调用：无
'''
def str_to_int_ten(data):
    return int('%s%s'%('0x',data),16)

#################十六进制单精度float值转浮点数函数#############
'''
函数名称：calc_float(data)
功能描述：根据浮点数格式与IEEE-754标准(32)计算浮点数。
参数意义：data：传入的8位数值
函数调用：无
'''
def calc_float(data):     
        if len(data)%8 != 0 :
            print("info长度有错误,不是8的倍数")
            return 0
        elif len(data)%8 ==0:
            data = data[::-1]                 #--------
            data_new = ''
            for i in range(0,7,2):            #把串口显示值转换为float值
                data_new+=data[i+1]
                data_new+=data[i]              #--------
        data_new_list = []
        for i in range(8):                     #把float转换成10进制数字列表，把列表元素处理成2进制构成字符串
            data_new_list.append(str_to_int_ten(data_new[i]))
            data_new_list[i] = bin(data_new_list[i]).lstrip('0b').zfill(4)
        data_new_str = ''.join(data_new_list)   #D31-D0，列表转字符串
        data_new_str_E = int(data_new_str[1:9],2)      #计算公式的E值
        data_new_str_M = int(data_new_str[9:32],2)     #计算公式的M值
        float_data = round(float((1+data_new_str_M*(pow(2,-23)))*pow(2,data_new_str_E-127)),2) #公式
        if data_new_list[0] =='1':
            float_data = 0-float_data
        return float_data     

###############校验和生成函数########################
#函数功能：获取chksum
#data_str_exclude_chksum：不包括~以及chksum的中间部分
'''
函数名称：get_chksum(data_str_exclude_chksum)
功能描述：计算chksum
参数意义：data_str_exclude_chksum：不包括chksum的命令
函数调用：data_reverse
'''
def get_chksum(data_str_exclude_chksum):
    sum_chksum = 0   #存储所有字符的十进制和（除去CHKSUM）
    for chksum_i in data_str_exclude_chksum:
        sum_chksum+=int(ord(chksum_i))
    sum_chksum_bin = data_reverse(sum_chksum%65535,16)     #默认长度为16位
    sum_chksum_bin = int(sum_chksum_bin,2)
    return hex(sum_chksum_bin+1).lstrip('0x').upper()       #取反+1转16进制去掉'0x'换算成大写，返回校验和
    
'''
-------------------------------------------------------------------------------
线程类函数定义
-------------------------------------------------------------------------------
'''
 
'''
函数名称：RepeatTimer(threading.Timer)
功能描述：定时器函数，创建新定时器线程，并可设定执行周期和执行函数
参数意义：threading.Timer：继承的threading模块的Timer类。self.interval：不用关注。*self.args：执行周期（可选参数）。*self.kwargs（执行函数）
函数调用：
'''   
class RepeatTimer(threading.Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args,*self.kwargs)

'''
函数名称：new_threading()
功能描述：创建新线程，暂时用不到。
参数意义：tar：目标函数
函数调用：threading.Thread
'''   
class new_threading():
    def __init__(self,tar):
        self.target = tar
        thread = threading.Thread(target = self.target)
        thread.start()
'''
串口判断，收发数据类(核心)
'''  

'''
类名称：send_message()
功能描述：串口数据命令的组成，发送，接收，初步解析。（核心类）
参数意义：
函数调用：。。
'''    
class send_message():
    '''
    函数名称：__init__(self,serial,parent)
    功能描述：初始化串口对象、UI对象和输出日志对象
    参数意义：serial：串口对象。parent：UI对象
    函数调用：无
    ''' 
    def __init__(self,serial,parent):
        self.ser = serial
        self.parent = parent
        self.massage = ''
        self.logging = logging_file()
        '''串口状态判断'''
        
    '''
    函数名称：judge_ser_status(self,frame2,frame3)
    功能描述：向串口发送请求指令，判断串口是否有返回。
    参数意义：frame2、frame3表示框架
    函数调用：figure_out_available_com
    ''' 
    def judge_ser_status(self,frame2,frame3):
        self.frame2 = frame2
        self.frame3 = frame3
        if self.ser.isOpen() == False:
            self.parent.title('串口助手-通讯异常')
            #set_analog_quantity_to_zero(self.frame2,self.frame3)
            self.ser.port = figure_out_available_com('~10002A500000FDA7\r')
            #self.ser.port = 'COM4'
            self.ser.baudrate = 9600
            self.ser.timeout = 1
            self.ser.open()
            return 0
        elif self.ser.isOpen() == True:
            return 1
    '''
    函数名称：assemble_command_for_quantity(self,body)
    功能描述：对模拟量请求指令进行拼装，返回完整指令赋值给固定变量等待发送。
    参数意义：body：表示'~'到chksum之前的命令字符串
    函数调用：get_chksum
    '''        
    def assemble_command_for_quantity(self,body):
        self.Device_VER = share_variable.Device_VER
        self.Device_ADR = share_variable.Device_ADR
        self.chksum = get_chksum(self.Device_VER+self.Device_ADR+body)
        self.massage = '%s%s%s%s%s%s'%('~',self.Device_VER,self.Device_ADR,body,self.chksum,'\r')
        return self.massage
        
        '''用于密码'''
    '''
    函数名称：assemble_command_for_password(self,receive_password)
    功能描述：对密码请求指令进行拼装，返回完整指令赋值给固定变量等待发送。
    参数意义：receive_password：从用户输入端得到的密码
    函数调用：assemble_command_for_quantity
    '''   
    def assemble_command_for_password(self,receive_password):#receive_password = share_variable
        self.receive_password = receive_password
        if self.receive_password == '':
            self.massage == '0'
            return self.massage
        else:
            self.massage = self.assemble_command_for_quantity(('%s%s'%('2A84400C',self.receive_password)))
            return self.massage
            
        '''用于设置量'''
    '''
    函数名称：assemble_command_for_setting(self,min_str,res_0,data_0)
    功能描述：对设置请求指令进行拼装，返回完整指令赋值给固定变量等待发送。
    参数意义：min_str：固定2A98600A。res_0：用户修改的指令值。data_0：用户修改的值对应cfg指令值
    函数调用：assemble_command_for_quantity
    ''' 
    def assemble_command_for_setting(self,min_str,res_0,data_0):  #min_str = '2A98600A' etc.
        self.res_0 = res_0
        self.data_0 = data_0
        if self.res_0 =='' or self.data_0 =='':
            self.massage = '0'
            return self.massage
        else:
            self.massage = self.assemble_command_for_quantity('%s%s%s'%(min_str,self.res_0,self.data_0))
            return self.massage
        
      
        '''组成完整命令并发送'''
    '''
    函数名称：assemble_commmand_and_send(self)
    功能描述：根据业务逻辑轮询串口并发送命令
    参数意义：
    函数调用：assemble_command、assemble_command_for_password、receive_inWaiting
    ''' 
    def assemble_commmand_and_send(self):
        '''判断setting_command表状态'''
        self.setting_command = sql.get_setting_status()
        if self.setting_command != '':            
            if self.setting_command[0][0] == 'password':
                self.receive_password = ''.join(list(map(lambda x:hex(ord(x)).lstrip('0x'),list(self.setting_command[0][1]))))   
                share_variable.receive_password = self.receive_password
                share_variable.polling_status = '1'
                sql.update_setting_status(['password',0])
                
            elif self.setting_command[0] == 'volt':
                share_variable.res = float_2_hex_2_com(int(self.setting_command[1]))
                share_variable.Sysdata_0 = 'A1'
                sql.update_setting_status(['volt',0])
                share_variable.polling_status = '1'
            elif self.setting_command[0] == 'freq':
                share_variable.res = float_2_hex_2_com(int(self.setting_command[1]))
                share_variable.Sysdata_0 = 'A2'
                sql.update_setting_status(['freq',0])
                share_variable.polling_status = '1'
            else:
                pass
        else:
            pass
        self.res = share_variable.res
        self.Sysdata_0 = share_variable.Sysdata_0
        self.res_rec = share_variable.res_rec
        self.Recdata_0 = share_variable.Recdata_0
        self.res_inv = share_variable.res_inv
        self.Invdata_0 = share_variable.Invdata_0
        self.res_bat = share_variable.res_bat
        self.Batdata_0 = share_variable.Batdata_0
        
        '''密码指令'''
        self.massage_84 = self.assemble_command_for_password(share_variable.receive_password)
        '''初始请求指令(获取设备版本号)'''
        self.massage_4F = '~10002A500000FDA7\r' 
        '''模拟量和调试级参数获取指令'''
        self.massage_41 = assemble_command(share_variable.Device_VER,share_variable.Device_ADR,'2A410000')      #获取标准模拟量数据指令
        self.massage_90 = assemble_command(share_variable.Device_VER,share_variable.Device_ADR,'2A900000')      #获取调试量数据
        self.massage_81 = assemble_command(share_variable.Device_VER,share_variable.Device_ADR,'2A810000')       #获取自定义模拟量数据1
        self.massage_82 = assemble_command(share_variable.Device_VER,share_variable.Device_ADR,'2A820000')       #获取自定义模拟量数据2
        self.massage_83 = assemble_command(share_variable.Device_VER,share_variable.Device_ADR,'2A830000')       #获取自定义模拟量数据3
        self.massage_43 = assemble_command(share_variable.Device_VER,share_variable.Device_ADR,'2A430000')       #获取开关量
        self.massage_44 = assemble_command(share_variable.Device_VER,share_variable.Device_ADR,'2A440000')       #获取告警量
        self.massage_80 = assemble_command(share_variable.Device_VER,share_variable.Device_ADR,'2A800000')       #获取系统调试级参数
        self.massage_91 = assemble_command(share_variable.Device_VER,share_variable.Device_ADR,'2A910000')       #获取整流调试级参数
        self.massage_92 = assemble_command(share_variable.Device_VER,share_variable.Device_ADR,'2A920000')       #获取逆变调试级参数
        self.massage_93 = assemble_command(share_variable.Device_VER,share_variable.Device_ADR,'2A930000')       #获取电池调试级参数
        '''读取历史记录'''
        self.massage_96 = assemble_command(share_variable.Device_VER,share_variable.Device_ADR,'2A960000')
        '''设定调试级参数指令'''
        self.massage_97 = self.assemble_command_for_setting('2A97600A',self.Sysdata_0,self.res)                  #设定系统调试级参数
        self.massage_98 = self.assemble_command_for_setting('2A98600A',self.Recdata_0,self.res_rec)              #设定整流调试级参数
        self.massage_99 = self.assemble_command_for_setting('2A99600A',self.Invdata_0,self.res_inv)              #设定逆变调试级参数
        self.massage_9A = self.assemble_command_for_setting('2A9A600A',self.Batdata_0,self.res_bat)              #设定电池调试级参数
        '''故障点数据(特殊)lchksum =  E002,最后的'01'表示整流数据,'02'表示逆变数据'''
        self.massage_A3_Rec = assemble_command(share_variable.Device_VER,share_variable.Device_ADR,'2AA3E00201')   #A3整流
        self.massage_A3_Inv = assemble_command(share_variable.Device_VER,share_variable.Device_ADR,'2AA3E00202')   #A3逆变
        self.massage_A4_Rec = assemble_command(share_variable.Device_VER,share_variable.Device_ADR,'2AA4E00201')   #A4整流
        self.massage_A4_Inv = assemble_command(share_variable.Device_VER,share_variable.Device_ADR,'2AA4E00202')   #A4逆变
        self.massage_A5_Rec = assemble_command(share_variable.Device_VER,share_variable.Device_ADR,'2AA5E00201')   #A5整流
        self.massage_A5_Inv = assemble_command(share_variable.Device_VER,share_variable.Device_ADR,'2AA5E00202')   #A5逆变
        self.massage_A6_Rec = assemble_command(share_variable.Device_VER,share_variable.Device_ADR,'2AA6E00201')   #A6整流
        self.massage_A6_Inv = assemble_command(share_variable.Device_VER,share_variable.Device_ADR,'2AA6E00202')   #A6逆变
        '''轮询并向串口发送数据'''
        massage_list_0 = [self.massage_4F,self.massage_41,self.massage_90,self.massage_81,self.massage_82,self.massage_83,
                          self.massage_43,self.massage_44,self.massage_80,self.massage_91,self.massage_92,self.massage_93]
        massage_list_1 = [self.massage_97,self.massage_98,self.massage_99,self.massage_9A,self.massage_84]
        self.receive_inWaiting(massage_list_0,massage_list_1,share_variable.polling_status)
        
        '''循环发送数据'''  
    '''
    函数名称：receive_inWaiting(self,massage_list_0,massage_list_1,status)
    功能描述：循环发送数据具体实现
    参数意义：massage_list_0：非设置量命令列表。massage_list_1：设置命令量命令列表。status：轮询标志位
    函数调用：无
    '''
    def receive_inWaiting(self,massage_list_0,massage_list_1,status): #command = '4F' etc. massage = 'massage_4F' etc.
        '''
        status为轮询状态，status == 0,表明正常轮询(模拟量，设置量)，
                         status == 1，表明有用户设置量插入。开始轮询用户设置量
                         status == 2,表明需要读取设置量信息
                         status == 3,表明需要读取历史数据
                         status == 4,表明需要读取故障点数据
        massage_list_0 = [massage_4F,massage_41,massage_90,massage_81,massage_82,
                        massage_83,massage_43,massage_44,massage_80,massage_91]
        massage_list_1 = [massage_97,massage_98,massage_84]
        '''
        self.status = status
        '''模拟量轮询区'''
        if share_variable.Device_CID2 == '' and self.status == '0':
            self.ser.write(massage_list_0[0].encode())
            share_variable.Device_CID2 = '4F' 
            self.logging.print_the_logging(share_variable.Device_CID2,'模拟量接收,send:',massage_list_0[0])
        elif share_variable.Device_CID2 == '4F' and self.status == '0':
            self.ser.write(massage_list_0[1].encode())
            share_variable.Device_CID2 = '41' #
            self.logging.print_the_logging(share_variable.Device_CID2,'模拟量接收,send:',massage_list_0[1])
        elif share_variable.Device_CID2 == '41' and self.status == '0':
            self.ser.write(massage_list_0[2].encode())
            share_variable.Device_CID2 = '90' #
            self.logging.print_the_logging(share_variable.Device_CID2,'模拟量接收,send:',massage_list_0[2])
        elif share_variable.Device_CID2 == '90' and self.status == '0':
            self.ser.write(massage_list_0[3].encode())
            share_variable.Device_CID2 = '81' #
            self.logging.print_the_logging(share_variable.Device_CID2,'模拟量接收,send:',massage_list_0[3])
        elif share_variable.Device_CID2 == '81' and self.status == '0':
            self.ser.write(massage_list_0[4].encode())
            share_variable.Device_CID2 = '82' #
            self.logging.print_the_logging(share_variable.Device_CID2,'模拟量接收,send:',massage_list_0[4])
        elif share_variable.Device_CID2 == '82' and self.status == '0':
            self.ser.write(massage_list_0[5].encode())
            share_variable.Device_CID2 = '83' #
            self.logging.print_the_logging(share_variable.Device_CID2,'模拟量接收,send:',massage_list_0[5])
            
            '''开关量\告警量轮询区'''
        elif share_variable.Device_CID2 == '83' and self.status == '0':
            if share_variable.switching_window_name == 'switch': #如果窗口标志为switch（表明窗口已开），进入循环
                self.ser.write(massage_list_0[6].encode())
                share_variable.Device_CID2 = '43'
                self.logging.print_the_logging(share_variable.Device_CID2,'开关量接收,send:',massage_list_0[6])
            else:
                share_variable.Device_CID2 = '43'               #标志位不为switch则CID2=43继续循环
        elif share_variable.Device_CID2 == '43' and self.status == '0':
            if share_variable.warning_window_name == 'warning':
                self.ser.write(massage_list_0[7].encode())
                share_variable.Device_CID2 = '44'
                self.logging.print_the_logging(share_variable.Device_CID2,'告警量接收,send:',massage_list_0[7])
            else:
                share_variable.Device_CID2 = '44'
            
                '''循环一次，CID2置为41重新循环'''
        elif share_variable.Device_CID2 == '44' and self.status == '0':
            self.ser.write(massage_list_0[1].encode())
            share_variable.Device_CID2 = '41'
            self.logging.print_the_logging(share_variable.Device_CID2,'模拟量接收,send:',massage_list_0[1])   
        
            '''设置量窗口数据发送区'''
        elif self.status == '2' and share_variable.setting_window_name == 'sys':
            self.ser.write(massage_list_0[8].encode())
            share_variable.Device_CID2 = '80'
            self.logging.print_the_logging(share_variable.Device_CID2,'系统调试参数,send:',massage_list_0[8])
        elif self.status == '2' and share_variable.setting_window_name == 'rec':
            self.ser.write(massage_list_0[9].encode())
            share_variable.Device_CID2 = '91'
            self.logging.print_the_logging(share_variable.Device_CID2,'整流调试参数,send:',massage_list_0[9])
        elif self.status == '2' and share_variable.setting_window_name == 'inv':
            self.ser.write(massage_list_0[10].encode())
            share_variable.Device_CID2 = '92'
            self.logging.print_the_logging(share_variable.Device_CID2,'逆变调试参数,send:',massage_list_0[10])
        elif self.status == '2' and share_variable.setting_window_name == 'bat':
            self.ser.write(massage_list_0[11].encode())
            share_variable.Device_CID2 = '93'
            self.logging.print_the_logging(share_variable.Device_CID2,'电池调试参数,send:',massage_list_0[11])
            '''历史记录请求请求命令发送区'''
        elif self.status == '3':
            share_variable.Device_CID2 = '96'
            self.ser.write(self.massage_96.encode())
            self.logging.print_the_logging(share_variable.Device_CID2,'历史记录请求,send:',self.massage_96) 
            '''故障点数据请求命令轮询发送区'''
        elif self.status == '4':
            
            if  share_variable.fault_status == 'rec1':
                #print('f1')
                share_variable.Device_CID2 = 'A3'
                self.ser.write(self.massage_A3_Rec.encode())
                self.logging.print_the_logging(share_variable.Device_CID2,'整流故障记录请求,send:',self.massage_A3_Rec)
                share_variable.fault_status = 'inv1'   #日志记录完成后，更改故障状态至逆变
                share_variable.fault_file_status = 'Rec1'   #文件保存名称暂存
            elif  share_variable.fault_status == 'inv1':
                #print('f2')
                self.ser.write(self.massage_A3_Inv.encode())
                self.logging.print_the_logging(share_variable.Device_CID2,'逆变故障记录请求,send:',self.massage_A3_Inv)
                share_variable.Device_CID2 = 'A4'
                share_variable.fault_status = 'rec2'
                share_variable.fault_file_status = 'Inv1'
            elif share_variable.fault_status == 'rec2':
                #print('f3')
                self.ser.write(self.massage_A4_Rec.encode())
                self.logging.print_the_logging(share_variable.Device_CID2,'整流故障记录请求,send:',self.massage_A4_Rec)
                share_variable.fault_status = 'inv2'
                share_variable.fault_file_status = 'Rec2'
            elif share_variable.fault_status == 'inv2':
                #print('f4')
                self.ser.write(self.massage_A4_Inv.encode())
                self.logging.print_the_logging(share_variable.Device_CID2,'逆变故障记录请求,send:',self.massage_A4_Inv)
                share_variable.Device_CID2 = 'A5'
                share_variable.fault_status = 'rec3'
                share_variable.fault_file_status = 'Inv2'
            elif share_variable.fault_status == 'rec3':
                #print('f5')
                self.ser.write(self.massage_A5_Rec.encode())
                self.logging.print_the_logging(share_variable.Device_CID2,'整流故障记录请求,send:',self.massage_A5_Rec)
                share_variable.fault_status = 'inv3'
                share_variable.fault_file_status = 'Rec3'
            elif share_variable.fault_status == 'inv3':
                #print('f6')
                self.ser.write(self.massage_A5_Inv.encode())
                self.logging.print_the_logging(share_variable.Device_CID2,'逆变故障记录请求,send:',self.massage_A5_Inv)
                share_variable.Device_CID2 = 'A6'
                share_variable.fault_status = 'rec4'
                share_variable.fault_file_status = 'Inv3'
            elif share_variable.fault_status == 'rec4':
                #print('f7')
                self.ser.write(self.massage_A6_Rec.encode())
                self.logging.print_the_logging(share_variable.Device_CID2,'整流故障记录请求,send:',self.massage_A6_Rec)
                share_variable.fault_status = 'inv4'
                share_variable.fault_file_status = 'Rec4'
            elif share_variable.fault_status == 'inv4':
                #print('f8')
                self.ser.write(self.massage_A6_Inv.encode())
                self.logging.print_the_logging(share_variable.Device_CID2,'逆变故障记录请求,send:',self.massage_A6_Inv)
                share_variable.Device_CID2 = ''
                share_variable.fault_status = ''
                share_variable.fault_file_status = 'Inv4'
            '''设置量下发命令区'''   
        elif massage_list_1[0] != '0' and self.status == '1':
            share_variable.Device_CID2 = '97'
            print('command:',massage_list_1[0])
            self.ser.write(massage_list_1[0].encode())
            self.logging.print_the_logging(share_variable.Device_CID2,'系统调试参数命令下发,send:',massage_list_1[0])
        elif massage_list_1[1] != '0' and self.status == '1':
            share_variable.Device_CID2 = '98' 
            self.ser.write(massage_list_1[1].encode())
            self.logging.print_the_logging(share_variable.Device_CID2,'整流调试参数命令下发,send:',massage_list_1[1])
        elif massage_list_1[2] != '0' and self.status == '1':
            share_variable.Device_CID2 = '99' 
            self.ser.write(massage_list_1[2].encode())
            self.logging.print_the_logging(share_variable.Device_CID2,'逆变调试参数命令下发,send:',massage_list_1[2])
        elif massage_list_1[3] != '0' and self.status == '1':
            share_variable.Device_CID2 = '9A' 
            self.ser.write(massage_list_1[3].encode())
            self.logging.print_the_logging(share_variable.Device_CID2,'电池调试参数命令下发,send:',massage_list_1[3])
        elif massage_list_1[4] != '0' and self.status == '1':
            share_variable.Device_CID2 = '84'
            self.ser.write(massage_list_1[4].encode())
            self.logging.print_the_logging(share_variable.Device_CID2,'密码命令下发,send:',massage_list_1[4])
            '''历史记录读取命令下发区'''
    '''
    函数名称：read_history_event(self,history_queue)
    功能描述：读历史记录。
    参数意义：history_queue：历史记录接收数据队列
    函数调用：Output_csv_for_history_event
    '''    
    def read_history_event(self,history_queue):
        '''特殊情况：历史记录(历史记录的格式不符合标准电总协议的数据构成方式，所以需要单独接收判断)'''
        self.data = ''
        self.output_csv_for_history = output_csv()
        while share_variable.history_output_status == '':
            self.data = self.ser.readline().decode()
            history_queue.put(self.data.replace('\n','').replace('\r','').replace('~',''))
            self.output_csv_for_history.Output_csv_for_history_event(history_queue.get())
            if self.data[-6:-4] == '~~': 
                share_variable.Device_CID2 = ''
                share_variable.history_output_status = '1'
                share_variable.polling_status = '0'
                tk.messagebox.showinfo('导出结果','导出成功！')
                self.ser.flushInput()
    '''
    函数名称：read_fault_event(self,fault_queue)
    功能描述：读故障记录。
    参数意义：fault_queue：故障点记录接收数据队列
    函数调用：Output_csv_for_history_event
    '''    
    def read_fault_event(self,fault_queue):
        '''读取故障点数据'''
        self.output_csv_for_fault = output_csv()
        while self.ser.inWaiting():
            share_variable.response_data_str += self.ser.read(1).decode()
        fault_queue.put(share_variable.response_data_str)
        fault_get = fault_queue.get()
        if len(fault_get) == 556:
            fault_data_list = protocol_fault.protocol_analyse(fault_get)
            #print('reclistx:',fault_data_list[1])
            if share_variable.fault_file_status == 'Rec1' or share_variable.fault_file_status == 'Rec2' or share_variable.fault_file_status == 'Rec3' or share_variable.fault_file_status == 'Rec4': 
                self.output_csv_for_fault.Output_csv_for_fault_event(1,fault_data_list[0],share_variable.fault_namelist_for_rec,fault_data_list[1],fault_data_list[2],fault_data_list[3],fault_data_list[4])
            else:
                self.output_csv_for_fault.Output_csv_for_fault_event(2,fault_data_list[0],share_variable.fault_namelist_for_inv,fault_data_list[1],fault_data_list[2],fault_data_list[3],fault_data_list[4])
        if share_variable.fault_file_status == 'Inv4':
            share_variable.polling_status = '0'
            
            
            
    '''while循环读取接收到的数据(读取方式有很多,但一个一个的读确实比一次性全部读完要快。)''' 
    '''
    函数名称：read_the_response_data_str(self,queue)
    功能描述：读其他串口数据，并进行初步解析
    参数意义：queue：模拟量数据队列
    函数调用：
    '''
    def read_the_response_data_str(self,queue):
        '''读取串口中等待的数据,self.data为每次读取的缓存值'''
        self.queue = queue
        self.data = ''
        while self.ser.inWaiting():
            try:
                share_variable.response_data_str += self.ser.read(1).decode()
            except(UnicodeDecodeError):
                break
        '''判断数据是否符合标准'''
        if share_variable.response_data_str[-1] == '\r' and share_variable.response_data_str[0] == '~':
            share_variable.Device_VER = data_split(share_variable.response_data_str,'VER')   #抽出响应中的VER
            share_variable.Device_ADR = data_split(share_variable.response_data_str,'ADR')   #抽出响应中的ADR
            share_variable.Device_RTN = data_split(share_variable.response_data_str,'CID2')  #抽出响应中的CID2
            share_variable.Device_DATAFLAG = data_split(share_variable.response_data_str,'DATAFLAG')
            '''返回值不符合要求的情况'''

            if share_variable.Device_RTN != '00':
                if share_variable.Device_RTN == '80':
                    print("无权限")
                    tk.messagebox.showerror(title = '无权限或密码错误',message = '请进入<设置>菜单下的<密码设置>中输入正确密码解锁')
                    self.logging.print_the_logging(share_variable.Device_RTN,'receive:',share_variable.response_data_str)
                    share_variable.polling_status = '0'  #轮询状态恢复
                    self.clear_the_value('1234')
                self.parent.title('串口助手-通讯异常')
                print("返回值RTN为:%s"%share_variable.Device_RTN)
                self.logging.print_the_logging(share_variable.Device_RTN,'receive:',share_variable.response_data_str)
                share_variable.polling_status = '0' #轮询状态恢复
                self.clear_the_value('1234') #系统设置清零
                share_variable.Device_CID2 = ''#CID2重新置空，方便发送请求指令
                
            
                '''RTN符合要求，进入下一步程序,开始解析数据'''   
            else:
                 print('当前请求CID2',share_variable.Device_CID2)
                 '''接收到数据,去掉结束位,方便解析函数解析'''
                 share_variable.response_data_str = share_variable.response_data_str.split('\r')[0]#去掉结束位
                 '''开关量\告警量\设置量数据接收'''
                 if share_variable.Device_CID2 == '43':
                     share_variable.receive_switch_data_str = share_variable.response_data_str
                     self.logging.print_the_logging(share_variable.Device_CID2,'receive:',share_variable.response_data_str)
                     return
                 elif share_variable.Device_CID2 == '44':
                     share_variable.receive_warning_data_str = share_variable.response_data_str
                     self.logging.print_the_logging(share_variable.Device_CID2,'receive:',share_variable.response_data_str)
                     return
                 
                 elif share_variable.Device_CID2 == '80' and share_variable.polling_status == '2' :
                     #print('CID2=80时的response_data_str',share_variable.response_data_str)
                     share_variable.receive_sysdata_str = share_variable.response_data_str
                     self.logging.print_the_logging(share_variable.Device_CID2,'receive:',share_variable.response_data_str)
                     share_variable.polling_status = '0'
                     share_variable.Device_CID2 = ''
                     return
                 elif share_variable.Device_CID2 == '91':
                     share_variable.receive_recdata_str = share_variable.response_data_str
                     self.logging.print_the_logging(share_variable.Device_CID2,'receive:',share_variable.response_data_str)
                     share_variable.polling_status = '0'
                     share_variable.Device_CID2 = ''
                     return
                 elif share_variable.Device_CID2 == '92':
                     share_variable.receive_invdata_str = share_variable.response_data_str
                     self.logging.print_the_logging(share_variable.Device_CID2,'receive:',share_variable.response_data_str)
                     share_variable.polling_status = '0'
                     share_variable.Device_CID2 = ''
                     return
                 elif share_variable.Device_CID2 == '93':
                     share_variable.receive_batdata_str = share_variable.response_data_str
                     self.logging.print_the_logging(share_variable.Device_CID2,'receive:',share_variable.response_data_str)
                     share_variable.polling_status = '0'
                     share_variable.Device_CID2 = ''
                     return

                     '''用户设置状态'''
                 elif share_variable.Device_CID2 == '97': 
                     self.logging.print_the_logging(share_variable.Device_CID2,'receive:',share_variable.response_data_str)
                     self.clear_the_value('1') #系统设置清零
                     #tk.messagebox.showinfo(title = '设置状态',message = '系统设置成功')
                     share_variable.polling_status = '2'
                     share_variable.setting_window_name = 'sys'
                 elif share_variable.Device_CID2 == '98':
                     self.logging.print_the_logging(share_variable.Device_CID2,'receive:',share_variable.response_data_str)
                     self.clear_the_value('2') #整流清零
                     #tk.messagebox.showinfo(title = '设置状态',message = '整流设置成功')
                     share_variable.polling_status = '2'
                     share_variable.setting_window_name = 'rec'
                     share_variable.Device_CID2 = '' 
                 elif share_variable.Device_CID2 == '99':
                     self.logging.print_the_logging(share_variable.Device_CID2,'receive:',share_variable.response_data_str)
                     self.clear_the_value('3') #整流清零
                     #tk.messagebox.showinfo(title = '设置状态',message = '逆变设置成功')
                     share_variable.polling_status = '2'
                     share_variable.setting_window_name = 'inv'
                 elif share_variable.Device_CID2 == '9A':
                     self.logging.print_the_logging(share_variable.Device_CID2,'receive:',share_variable.response_data_str)
                     self.clear_the_value('4') #整流清零
                     #tk.messagebox.showinfo(title = '设置状态',message = '电池设置成功')
                     share_variable.polling_status = '2'
                     share_variable.setting_window_name = 'bat'
                 #密码接收
                 elif share_variable.Device_CID2 == '84':
                     print('share_variable.Device_RTN',share_variable.Device_RTN)
                     if share_variable.Device_RTN == '00':
                         #tk.messagebox.showinfo("密码","密码输入成功，可以进行设置操作")
                         self.logging.print_the_logging(share_variable.Device_CID2,'receive:',share_variable.response_data_str)
                         share_variable.polling_status = '0'
                         share_variable.receive_password = ''
                         share_variable.Device_CID2 = ''
                     else:
                         tk.messagebox.showinfo("密码","密码错误")
                         self.logging.print_the_logging(share_variable.Device_CID2,'receive:',share_variable.response_data_str)
                         share_variable.polling_status = '0'
                         share_variable.Device_CID2 = ''
                         '''开始模拟量分析'''
                 else:
                     self.protocol_list = protocol.analysis_protocol(share_variable.response_data_str)
                     
                 if  share_variable.Device_CID2 == '41':
                     common_label_dict_for_41 = [
                         #0：A相输入线电压，1：B相输入线电压，2：C相输入线电压
                         #3：输出相电压 6：输出电流 9：电池电压
                         #10：输出频率:11：电池容量 12：电池温度 
                         #9个
                         self.protocol_list[0],self.protocol_list[1],self.protocol_list[2], 
                         self.protocol_list[3],self.protocol_list[6],self.protocol_list[10],
                         self.protocol_list[9],self.protocol_list[12],self.protocol_list[11] 
                                                 ]
                     self.queue.put(common_label_dict_for_41)
                     self.logging.print_the_logging(share_variable.Device_CID2,'receive:',share_variable.response_data_str)
                 elif share_variable.Device_CID2 == '90':
                     common_label_dict_for_90 = [
                        #22个
                        self.protocol_list[22],self.protocol_list[23],self.protocol_list[24],
                        self.protocol_list[15],self.protocol_list[16],self.protocol_list[17],
                        self.protocol_list[18],self.protocol_list[19],self.protocol_list[20],
                        self.protocol_list[0],self.protocol_list[3],self.protocol_list[28],
                        self.protocol_list[25],self.protocol_list[17],self.protocol_list[7],
                        self.protocol_list[8],self.protocol_list[9],self.protocol_list[10],
                        self.protocol_list[14],self.protocol_list[6],self.protocol_list[13],
                        self.protocol_list[35]
                                                ]
                     common_label_dict_for_ups_serial_num = [
                        self.protocol_list[32],self.protocol_list[33],
                        self.protocol_list[34],self.protocol_list[35],
                                                            ]
                     print('common_label_dict_for_ups_serial_num',common_label_dict_for_ups_serial_num)
                     self.queue.put(common_label_dict_for_90)
                     self.logging.print_the_logging(share_variable.Device_CID2,'receive:',share_variable.response_data_str)
                 elif share_variable.Device_CID2 == '81':
                     common_label_dict_for_81 = [
                         #12个
                         self.protocol_list[0],self.protocol_list[1],self.protocol_list[2],
                         self.protocol_list[3],self.protocol_list[4],self.protocol_list[7],
                         self.protocol_list[10],self.protocol_list[11],self.protocol_list[14],
                         self.protocol_list[20],self.protocol_list[23],self.protocol_list[26],
                                                 ]
                     self.queue.put(common_label_dict_for_81)
                     self.logging.print_the_logging(share_variable.Device_CID2,'receive:',share_variable.response_data_str)
                 elif share_variable.Device_CID2 == '82':
                     #if share_variable.Device_DATAFLAG == 'A3':
                         common_label_dict_for_82 = [
                             #5
                             self.protocol_list[0],self.protocol_list[3],self.protocol_list[6],
                             self.protocol_list[10],self.protocol_list[9]                             
                                                     ]
                         print('系统输出视在功率',self.protocol_list[6])
                         self.queue.put(common_label_dict_for_82)
                         self.logging.print_the_logging(share_variable.Device_CID2,'receive:',share_variable.response_data_str)
                 elif share_variable.Device_CID2 == '83':
                     common_label_dict_for_83 = [
                         #6个
                         self.protocol_list[3],self.protocol_list[1],self.protocol_list[2],
                         self.protocol_list[0],self.protocol_list[9],self.protocol_list[10]
                                                  ] 
                     self.queue.put(common_label_dict_for_83)
                     self.logging.print_the_logging(share_variable.Device_CID2,'receive:',share_variable.response_data_str)
                 else:
                     print("Device_CID2无对应:",share_variable.Device_CID2)
                     print('RTN：',share_variable.Device_RTN)
                     print('返回命令:',share_variable.response_data_str)
                     self.logging.print_the_logging(share_variable.Device_CID2,'receive:',share_variable.response_data_str)
                 self.parent.title('串口助手-通讯正常')
                 #清除输入
                 self.ser.flushInput() 
    
    '''快速变量清零函数'''
    
    '''
    函数名称：clear_the_value(self,condition)
    功能描述：读取完成后需要对临时数据库的部分值和状态进行清零。
    参数意义：condition：需要清零的情况
    函数调用：
    '''    
    def clear_the_value(self,condition):
        self.condition = condition
        '''系统清零'''
        if '1' in self.condition:           
            share_variable.res = ''
            share_variable.Sysdata_0 = ''
            '''整流清零'''
        if '2' in self.condition:         
            share_variable.res_rec = '' 
            share_variable.Recdata_0 = ''
            '''逆变清零'''
        if '3' in self.condition:
            share_variable.res_inv= '' 
            share_variable.Invdata_0 = ''
            '''电池清零'''
        if '4' in self.condition:
            share_variable.res_bat= '' 
            share_variable.Batdata_0 = ''

            '''其他清零(密码，protocol字符串)'''
        if '5' in self.condition:
            share_variable.receive_password = ''
            share_variable.receive_sysdata_str = ''
            share_variable.receive_recdata_str = ''
            share_variable.receive_switch_data_str = ''
            share_variable.receive_warning_data_str = ''
            
            
'''
辅助类
'''  
'''计算chksm'''          
class calc_chksum():
    def __init__(self):
        self.res = simpledialog.askstring('请输入协议字符串','请输入无开始位(~)\无chksum协议字符串：\n 例如：完整协议：~~10012A4F0000FD91,则输入10012A4F0000')
        self.return_chksum = get_chksum(self.res)
        tk.messagebox.showinfo(title = '返回的CHKSUM值',message = self.return_chksum)
'''计算单精度浮点数'''
class calc_Single_float():
    def __init__(self):
        self.res = simpledialog.askstring('请输入浮点数','请输入浮点数字符串：\n 例如输入：2.0')
        self.return_float = float_2_hex_2_com(float(self.res))
        tk.messagebox.showinfo(title = '返回的float值',message = self.return_float)        
        
    
    
    
    
    
    
    
    