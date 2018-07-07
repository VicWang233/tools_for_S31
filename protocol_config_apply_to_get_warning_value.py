# -*- coding: utf-8 -*-
"""
Created on Wed May  2 20:13:51 2018

@author: Administrator
"""

import func_def as func


def analysis_protocol(protocol_str):


    protocol_info = func.data_split(protocol_str,'DATA_INFO_for_switch')  #DATA_INFO_for_switch同样适用于warning
    if func.data_verify(protocol_str) == 0:
        print("数据有错误")
        return 0
    elif func.data_verify(protocol_str) == 1:
        print('44数据正常')
        pass

    protocol_warning_value_word1_dict = {                     #告警量状态字典
            '15':['正常','故障'],
            '14':['正常','掉电'],
            '13':['正常','故障'],
            '12':['正常','故障(故障)'],
            '11':['正常','故障(故障)'],
            '10':['正常','故障(故障)'],
            '9':['正常','超限'],
            '8':['\\'],
            '7':['\\'],
            '5-6':['正常','电池未接','电池低压与告警','电池接反'],
            '4':['正常','超限'],
            '3':['正常','异常'],
            '2':['正常','故障'],
            '1':['正常','故障'],
            '0':['正常','不同步']
                                    }
 
    protocol_warning_value_word2_dict = {
            '15':['正常','异常'],
            '14':['正常','过载超时'],
            '13':['正常','过载'],
            '12':['正常','过载'],
            '11':['正常','错误'],
            '10':['正常','故障'],
            '9':['正常','故障'],
            '8':['正常','故障'],
            '7':['正常','过温'],
            '6':['正常','故障'],
            '5':['正常','故障'],
            '4':['正常','故障'],
            '3':['正常','超限'],
            '2':['正常','故障'],
            '1':['正常','过温'],
            '0':['正常','故障']
                                            }
    protocol_warning_value_word3_dict = {
            '15':['正常','过温'],
            '14':['正常','过温'],
            '12-13':['未激活','激活','故障'],
            '11':['正常','故障'],
            '10':['正常','故障'],
            '9':['正常','故障'],
            '8':['正常','故障'],
            '7':['正常','故障'],
            '6':['正常','故障'],
            '5':['正常','故障'],
            '4':['正常','超限'],
            '3':['正常','故障'],
            '2':['正常','故障'],
            '1':['正常','故障'],
            '0':['正常','故障']
                                            }
    protocol_warning_value_word4_dict = {
            '15':['正常','过压'],
            '14':['正常','过压'],
            '13':['正常','断'],
            '11-12':['闭合','断开','未接入'],
            '10':['正常','故障'],
            '9':['正常','故障'],
            '8':['正常','过高'],
            '6-7':['正常','电池需维护','电池寿命终结'],
            '5':['正常','告警'],
            '4':['正常','紧急关机'],
            '3':['正常','故障','无效'],
            '2':['正常','故障'],
            '1':['正常','故障'],
            '0':['正常','故障']
                                            }
    protocol_warning_value_word5_dict = {
            '7-15':['\\'],
            '6':['正常','告警'],
            '5':['正常','告警'],
            '4':['正常','告警'],
            '3':['正常','告警'],
            '2':['正常','告警'],
            '1':['正常','告警'],
            '0':['正常','短路']
                                            }
    

#-----------------------------

    protocol_dataf_list = []
    if protocol_info == None:
        pass
    elif len(protocol_info) != 20:         #判断info长度
        print("DATAINFO长度有误")
        return 0
    else:
        word1 = protocol_info[:4]
        word2 = protocol_info[4:8]
        word3 = protocol_info[8:12]
        word4 = protocol_info[12:16]
        word5 = protocol_info[16:]
        word1_to_bin  = bin(int(word1,16)).lstrip('0b').zfill(16)    #2进制word1
        word2_to_bin  = bin(int(word2,16)).lstrip('0b').zfill(16)    #2进制word2
        word3_to_bin  = bin(int(word3,16)).lstrip('0b').zfill(16)
        word4_to_bin  = bin(int(word4,16)).lstrip('0b').zfill(16)
        word5_to_bin  = bin(int(word5,16)).lstrip('0b').zfill(16)

        #print('word3_to_bin转后',word3_to_bin)
        word1_list = []
        word2_list = []
        word3_list = []
        word4_list = []
        word5_list = []
        
        for i in range(len(word1_to_bin)):               #把datainfo分割成数组，方便与前面的字典组合来选择数据
            if i == 6:
                word1_list.append(word1_to_bin[i-1:i+1])
            elif i== 5:
                continue
            else:
                word1_list.append(word1_to_bin[i])        
        for i in range(len(word2_to_bin)):                        
            word2_list.append(word2_to_bin[i])
        
        for i in range(len(word3_to_bin)):               #把datainfo分割成数组，方便与前面的字典组合来选择数据
            if i == 13:
                word3_list.append(word3_to_bin[i-1:i+1])
            elif i== 12:
                continue
            else:
                word3_list.append(word3_to_bin[i])   
        for i in range(len(word4_to_bin)):               #把datainfo分割成数组，方便与前面的字典组合来选择数据
            if i == 12 or i == 7:
                word4_list.append(word4_to_bin[i-1:i+1])
            elif i == 6 or i == 11:
                continue
            else:
                word4_list.append(word4_to_bin[i]) 
        for i in range(len(word5_to_bin)):               #把datainfo分割成数组，方便与前面的字典组合来选择数据
            if i >= 8:
                continue
            else:
                word5_list.append(word5_to_bin[i])         
            
        #print(word1_list)
        #print('word4_list',word4_list)
        protocol_warning_value_word_dict_list = [protocol_warning_value_word5_dict,protocol_warning_value_word4_dict,
                                                 protocol_warning_value_word3_dict,protocol_warning_value_word2_dict,
                                                 protocol_warning_value_word1_dict]
        word_list = [word5_list,word4_list,word3_list,word2_list,word1_list]
        for i in range(len(word_list)):
            #print('word_list[i]',word_list[i])
            for j in range(len(protocol_warning_value_word_dict_list[i])):
                dict_key = list(protocol_warning_value_word_dict_list[i].keys())[j]
                dict_value = protocol_warning_value_word_dict_list[i].get(dict_key)
                index_for_value = int(word_list[i][j],2)
                #print('%dindex_for_value:%d'%(j,index_for_value))
                protocol_dataf_list.append(dict_value[index_for_value])
                
        protocol_dataf_list = protocol_dataf_list[::-1]

        #print(protocol_dataf_list)
        #print('word1',protocol_dataf_list[:15])    #15
        #print('word2',protocol_dataf_list[15:31])  #16
        #print('word3',protocol_dataf_list[31:46])  #15
        #print('word4',protocol_dataf_list[46:60])  #14
        #print('word5',protocol_dataf_list[60:])    #8
        #print(len(protocol_dataf_list))

    #print(len(protocol_dataf_list))
    return protocol_dataf_list
    #拆出结束位OR（回车）
    
    
#pro = input("请输入指令：")

#pro_1 = pro  #使用encode来模拟串口传来的bytes数据

#analysis_protocol(pro_1)
   
    
    
    
    
    
    
    
    
    
    
    