# -*- coding: utf-8 -*-
"""
Created on Wed May  2 20:13:51 2018

@author: Administrator
"""

import func_def as func


def analysis_protocol(protocol_str):
    protocol_info = func.data_split(protocol_str,'DATA_INFO_for_switch')
    if func.data_verify(protocol_str) == 0:
        print("数据有错误")
        return 0
    elif func.data_verify(protocol_str) == 1:
        print('43数据正常')
        pass

    protocol_switching_value_word1_dict = {                     #开关量状态字典
            '15':['\\','\\','\\','\\','\\','\\','\\','\\','\\','\\','\\','\\','\\','\\','\\'],
            '14':['断开状态','闭合状态'],
            '13':['断开状态','闭合状态'],
            '12':['断开状态','闭合状态'],
            '11':['断开状态','闭合状态'],
            '10':['发电机未接入','发电机接入'],
            '9':['主路逆变供电','电池逆变供电','联合逆变供电','整流电池均不供电'],
            '7':['关机','开机'],
            '6':['非充电状态','浮充','均充'],
            '4':['没有自检','自检中'],
            '3':['\\','\\','\\','\\'],
            '1':['均不供电','逆变供电','旁路供电'],
                                    }
 
    protocol_switching_value_word2_dict = {
            '8':['\\'],
            '7':['非ECO模式','ECO模式'],
            '6':['非智能并机模式','智能并机模式'],
            '5':['未接入','接入'],
            '4':['正常模式','维修模式','步进模式','自老化模式','隔离模式'],
            '1':['主路逆变供电','电池逆变供电','旁路供电','均不供电'],
                                            }
    
#-----------------------------

    protocol_dataf_list = []
    if protocol_info == None:
        pass
    elif len(protocol_info) != 8:         #判断info长度
        print("DATAINFO长度有误")
        return 0
    else:
        word1 = protocol_info[:4]
        #print('word1',word1)
        word2 = protocol_info[4:]
        word1_to_bin  = bin(int(word1,16)).lstrip('0b').zfill(16)    #2进制word1
        word2_to_bin  = bin(int(word2,16)).lstrip('0b').zfill(16)     #2进制word2

        #word1_to_bin = word1_to_bin[::-1]            #搞反了，反转
        #word2_to_bin = word2_to_bin[::-1]  
        #print('word1_to_bin',word1_to_bin)
        #print('word2_to_bin',word2_to_bin)
        word1_list = []
        word2_list = []
        for i in range(len(word1_to_bin)):               #把datainfo分割成数组，方便与前面的字典组合来选择数据
            if i == 7 or i == 10 or i == 13 or i == 15:
                word1_list.append(word1_to_bin[i-1:i+1])
            elif i==6 or i == 9 or i == 12 or i ==14:
                continue
            else:
                word1_list.append(word1_to_bin[i])        
        for i in range(len(word2_to_bin)):                        
            if i == 11 or i == 12 or i == 14 or 1<=i<=7:   #此处应要反向遍历。详细见文档标记
                continue
            elif i == 15 or i == 13:
                word2_list.append(word2_to_bin[i-1:i+1])
            elif i == 0:
                word2_list.append(str(0))   #写死
            else:
                word2_list.append(word2_to_bin[i])
                
        #print(word1_list)
        #print(word2_list)
       
        for i in range(len(protocol_switching_value_word2_dict)):        #通过字典把word作为key，开关量的状态作为value进行配对。
            dict_key = list(protocol_switching_value_word2_dict.keys())[i]
            dict_value = protocol_switching_value_word2_dict.get(dict_key)
            protocol_dataf_list.append(dict_value[int(word2_list[i],2)])
        for i in range(len(protocol_switching_value_word1_dict)):
            dict_key = list(protocol_switching_value_word1_dict.keys())[i]
            dict_value = protocol_switching_value_word1_dict.get(dict_key) 
            protocol_dataf_list.append(dict_value[int(word1_list[i],2)])
        
        protocol_dataf_list = protocol_dataf_list[::-1]
        
        return protocol_dataf_list
        #print('protocol_dataf_list',protocol_dataf_list)
    #拆出结束位OR（回车）
    
    
#pro = input("请输入指令：")

#pro_1 = pro  #使用encode来模拟串口传来的bytes数据

#analysis_protocol(pro_1)
   
    
    
    
    
    
    
    
    
    
    
    