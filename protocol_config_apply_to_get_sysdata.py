# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 21:32:16 2018

@author: VicWang
"""

import func_def as func


def analysis_protocol(protocol_str):
    protocol_info = func.data_split(protocol_str,'DATA_INFO_for_Sysdata')
    protocol_num = func.data_split(protocol_str,'DATA_NUM_for_Sysdata')
    protocol_num = int(protocol_num,16)
    #print('protocol_info',protocol_info)
    #print('protocol_num',protocol_num)
    if func.data_verify(protocol_str) == 0:
        print("数据有错误")
        return 0
    elif func.data_verify(protocol_str) == 1:
        print('数据正常')
        pass

####################datainfo处理#########################
    if protocol_info == None:
        pass
    elif len(protocol_info)%8 != 0 or len(protocol_info)/8 != protocol_num:         #判断info长度
        print("DATAINFO长度有误")
        return 0
    elif len(protocol_info)%8 == 0:          #如果是8的倍数，则分割开始计算数值
        #print("info长度",len(protocol_info))
        protocol_info_list = []
        for i in range(0,len(protocol_info),8):
            protocol_info_list.append(protocol_info[i:i+8])
        #print(protocol_info_list)
        protocol_dataf_list = []
        for i in range(0,len(protocol_info_list)):
            protocol_dataf_list.append(func.calc_float((protocol_info_list[i])))
            #print("第%d个数为："%(i+1),func.calc_float((protocol_info_list[i])))
    else:
        print("DATAINFO长度为None")


####################拆出chksum并验证######################
    #print('protocol_dataf_list',protocol_dataf_list)
    return protocol_dataf_list


    
    
#pro = input("请输入指令：")

#pro_1 = pro  #使用encode来模拟串口传来的bytes数据
#analysis_protocol(pro_1)





