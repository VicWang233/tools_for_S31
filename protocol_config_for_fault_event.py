# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 14:08:16 2018

@author: VicWang
"""


def protocol_analyse(data):
    year = int(data[15:19],16)
    month = int(data[19:23],16)
    day = int(data[23:27],16)
    hour = int(data[27:31],16)
    minute = int(data[31:35],16)
    second = int(data[35:39],16)
    time = '%d-%d-%d,%d-%d-%d'%(year,month,day,hour,minute,second)
    return_list_single = []
    return_list_dict = [time]        #0：时间 1：第一点 2：第二点 3：第三点 4：第四点       #4个点
    for j in range(0,512,4):  #每个点对应长度为4的数据（16位）
            return_list_single.append(data[39+j:39+j+4])
    return_list_dict.append(return_list_single[:32])
    return_list_dict.append(return_list_single[32:64])
    return_list_dict.append(return_list_single[64:96])
    return_list_dict.append(return_list_single[96:128])
    return return_list_dict



        
#a = input('请输入指令:')

#protocol_analyse(a)

